import asyncio
import logging
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from utils.json_helpers import parse_json_response
from config import MODEL_FAST as MODEL

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a medical evidence grader. You receive a research paper's metadata and abstract.

Your job is to classify the study design, assign an evidence level, and flag methodological concerns.

EVIDENCE LEVELS:

Level A (Strong):
- Systematic review or meta-analysis of RCTs
- Large multi-center RCT (n > 500, pre-registered)
- Well-designed cohort study with hard outcomes and long follow-up

Level B (Moderate):
- Single RCT of any size, especially pilot or single-center
- Prospective cohort study
- High-quality case-control study
- Systematic review of observational studies

Level C (Low / Early):
- Case series (< 30 patients) or case reports
- Cross-sectional study
- Expert opinion, editorial, commentary
- Pilot or feasibility study
- Animal or in vitro study
- Conference abstract or preprint without peer review

STUDY DESIGN classification (choose exactly one):
- "meta-analysis": publication type or title contains meta-analysis or systematic review
- "RCT": publication type = Randomized Controlled Trial, or title/abstract contains "randomized"
- "cohort": abstract contains cohort, prospective, retrospective + study
- "case-control": abstract contains case-control
- "case-series": abstract contains case series, or n < 30 patients described
- "pilot": abstract contains pilot, feasibility, proof of concept
- "opinion": publication type = Editorial, Comment, Letter, or Opinion
- "review": publication type = Review without meta-analysis
- "unknown": cannot determine from abstract alone

METHODOLOGY FLAGS (include all that apply):
- "small sample": n < 50 in intervention arm
- "no control group": no comparator described
- "industry funding": funded by pharmaceutical or device company
- "single center": only one institution
- "short follow-up": < 6 months for a chronic disease outcome
- "surrogate outcome": primary outcome is a biomarker, not a clinical endpoint
- "unregistered trial": RCT without a registration number
- "preprint": not yet peer-reviewed

Respond ONLY with valid JSON, no markdown, no preamble:
{
  "study_design": "RCT",
  "evidence_level": "B",
  "methodology_flags": ["small sample", "single center"],
  "grader_reasoning": "Single-center RCT with n=47. Evidence level B: RCT but limited by small sample size and single site."
}"""

_DEFAULTS = {
    "study_design": "unknown",
    "evidence_level": "C",
    "methodology_flags": [],
    "grader_reasoning": "processing error",
}


async def grade_paper(paper: dict) -> dict:
    """Grades a single paper. Never raises — returns defaults on any failure."""
    prompt = (
        f"Title: {paper.get('title', '')}\n"
        f"Journal: {paper.get('journal', '')}\n"
        f"Publication Date: {paper.get('pub_date', '')}\n"
        f"Publication Types: {', '.join(paper.get('publication_types', []))}\n"
        f"Abstract:\n{paper.get('abstract', '')}\n\n"
        f"Grade this paper."
    )

    options = ClaudeAgentOptions(system_prompt=SYSTEM_PROMPT, max_turns=1, model=MODEL)
    result_parts = []
    try:
        async for msg in query(prompt=prompt, options=options):
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        result_parts.append(block.text)
    except Exception as e:
        logger.warning(f"Claude grader failed for PMID {paper.get('pmid', '?')}: {e}")
        return {**paper, **_DEFAULTS}

    raw = "\n".join(result_parts)
    try:
        grade = parse_json_response(raw)
    except ValueError as e:
        logger.warning(f"JSON parse failed for PMID {paper.get('pmid', '?')}: {e}")
        return {**paper, **_DEFAULTS}

    return {
        **paper,
        "study_design": grade.get("study_design", _DEFAULTS["study_design"]),
        "evidence_level": grade.get("evidence_level", _DEFAULTS["evidence_level"]),
        "methodology_flags": grade.get("methodology_flags", []),
        "grader_reasoning": grade.get("grader_reasoning", ""),
    }


async def grade_all(papers: list[dict]) -> list[dict]:
    """Grades all papers concurrently. Returns list in same order."""
    results = await asyncio.gather(*[grade_paper(p) for p in papers], return_exceptions=True)
    graded = []
    for paper, result in zip(papers, results):
        if isinstance(result, Exception):
            logger.warning(f"Unexpected error grading PMID {paper.get('pmid', '?')}: {result}")
            graded.append({**paper, **_DEFAULTS})
        else:
            graded.append(result)
    return graded
