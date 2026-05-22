import asyncio
import logging
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from utils.json_helpers import parse_json_response
from config import MODEL_FAST as MODEL

logger = logging.getLogger(__name__)

_SYSTEM_TEMPLATE = """You are a medical relevance rater for a physician's personalized research digest.

Physician profile:
- Name: {name}
- Specialties: {specialties}
- Subspecialties: {subspecialties}
- Role: {role}
- Practice setting: {practice_setting}
- Country: {country}
- Patient population: {patient_population}
- Research interests: {research_interests}

Score this paper's relevance to this physician from 1 to 10:

10: Directly addresses their specialty AND research interests; high-evidence; immediately actionable
8-9: Highly relevant to specialty or subspecialty; well-designed study
6-7: Relevant to general practice area; useful background knowledge
4-5: Tangentially related; general medicine without specialty focus
1-3: Outside their specialty; non-clinical (basic science only); irrelevant

Also rate clinical actionability:
- "high": directly changes practice (new drug, new protocol, guideline update)
- "moderate": informs practice without immediate change
- "low": background knowledge, basic science, conceptual

Consider their practice setting: academic physicians benefit more from methodological nuance;
community physicians value practical applicability over research implications.

Respond ONLY with valid JSON, no markdown, no preamble:
{{
  "relevance_score": 8,
  "relevance_reasoning": "Direct RCT on heart failure with reduced ejection fraction — core subspecialty.",
  "clinical_actionability": "high"
}}"""

_DEFAULTS = {
    "relevance_score": 5,
    "relevance_reasoning": "processing error",
    "clinical_actionability": "moderate",
}


def _build_system_prompt(profile: dict) -> str:
    prefs = profile.get("newsletter_preferences", {})
    return _SYSTEM_TEMPLATE.format(
        name=profile.get("name", ""),
        specialties=", ".join(profile.get("specialties", [])) or "not specified",
        subspecialties=", ".join(profile.get("subspecialties", [])) or "none",
        role=", ".join(profile.get("role", [])) or "not specified",
        practice_setting=profile.get("practice_setting", "not specified"),
        country=profile.get("country", "not specified"),
        patient_population=profile.get("patient_population", "not specified"),
        research_interests=", ".join(profile.get("research_interests", [])) or "none",
    )


async def score_paper(paper: dict, system_prompt: str) -> dict:
    """Scores a single paper. Never raises — returns defaults on any failure."""
    prompt = (
        f"Title: {paper.get('title', '')}\n"
        f"Journal: {paper.get('journal', '')}\n"
        f"Study design: {paper.get('study_design', 'unknown')}\n"
        f"Evidence level: {paper.get('evidence_level', 'C')}\n"
        f"Source specialty search: {paper.get('source_specialty', '')}\n"
        f"Abstract:\n{paper.get('abstract', '')}\n\n"
        f"Score this paper's relevance."
    )

    options = ClaudeAgentOptions(system_prompt=system_prompt, max_turns=1, model=MODEL)
    result_parts = []
    try:
        async for msg in query(prompt=prompt, options=options):
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        result_parts.append(block.text)
    except Exception as e:
        logger.warning(f"Relevance scorer failed for PMID {paper.get('pmid', '?')}: {e}")
        return {**paper, **_DEFAULTS}

    raw = "\n".join(result_parts)
    try:
        scored = parse_json_response(raw)
    except ValueError as e:
        logger.warning(f"JSON parse failed for PMID {paper.get('pmid', '?')}: {e}")
        return {**paper, **_DEFAULTS}

    return {
        **paper,
        "relevance_score": int(scored.get("relevance_score", _DEFAULTS["relevance_score"])),
        "relevance_reasoning": scored.get("relevance_reasoning", ""),
        "clinical_actionability": scored.get("clinical_actionability", _DEFAULTS["clinical_actionability"]),
    }


async def filter_papers(papers: list[dict], profile: dict) -> list[dict]:
    """
    Scores all papers, discards those with relevance_score < 5,
    sorts descending, caps at max_papers.
    """
    system_prompt = _build_system_prompt(profile)
    max_papers = profile.get("newsletter_preferences", {}).get("max_papers", 10)

    scored = await asyncio.gather(
        *[score_paper(p, system_prompt) for p in papers],
        return_exceptions=True,
    )

    result = []
    for paper, s in zip(papers, scored):
        if isinstance(s, Exception):
            logger.warning(f"Unexpected scoring error for PMID {paper.get('pmid', '?')}: {s}")
            result.append({**paper, **_DEFAULTS})
        else:
            result.append(s)

    kept = [p for p in result if p.get("relevance_score", 0) >= 5]
    kept.sort(key=lambda p: p.get("relevance_score", 0), reverse=True)
    kept = kept[:max_papers]

    print(f"  Relevance filter: {len(papers)} → {len(kept)} papers (discarded {len(papers) - len(kept)})")
    return kept
