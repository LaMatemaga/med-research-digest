import asyncio
import logging
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from config import MODEL_SMART as MODEL

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a medical research synthesizer for a physician's personal digest.

You receive multiple expert perspectives on a single research paper and write one cohesive paragraph that integrates all of them.

Rules:
- One paragraph, 200-280 words
- Start with the key clinical finding (what it means for patients, in plain terms)
- Weave in the methodological quality honestly (without dismissing or over-trusting)
- Include specialist nuance where it adds something non-obvious
- If evidence is preliminary, end with an open question rather than a false take-home
- If evidence is strong, end with a clear practical take-home point
- Write for a busy physician who reads this between patients — precise, honest, no hype
- Do not use section headers or bullet points
- Do not use filler phrases like "according to the paper", "the authors found", "it is important to note"
- Blend the perspectives naturally — do not credit each voice separately"""


def _build_synthesis_prompt(paper: dict) -> str:
    voice_outputs: dict = paper.get("voice_outputs", {})

    voice_sections = []
    voice_labels = {
        "clinician_voice": "CLINICIAN VIEW",
        "researcher_voice": "RESEARCHER VIEW",
        "educator_voice": "EDUCATOR VIEW",
        "methodologist_voice": "METHODOLOGIST VIEW",
        "gremial_voice": "PROFESSIONAL LANDSCAPE",
    }

    for key, label in voice_labels.items():
        text = voice_outputs.get(key)
        if text:
            voice_sections.append(f"{label}:\n{text}")

    for key, text in voice_outputs.items():
        if key.startswith("specialist_voice_") and text:
            specialty = key.replace("specialist_voice_", "").replace("_", " ").title()
            voice_sections.append(f"{specialty.upper()} SPECIALIST VIEW:\n{text}")

    flags = paper.get("methodology_flags", [])
    flags_line = f"Methodology flags: {', '.join(flags)}" if flags else "No major methodology flags."

    return (
        f"Title: {paper.get('title', '')}\n"
        f"Journal: {paper.get('journal', '')} ({paper.get('pub_date', '')})\n"
        f"Evidence Level: {paper.get('evidence_level', 'C')} ({paper.get('study_design', 'unknown')})\n"
        f"{flags_line}\n\n"
        "Expert perspectives:\n\n"
        + "\n\n".join(voice_sections)
        + "\n\nWrite a single cohesive paragraph integrating all perspectives above."
    )


async def synthesize_paper(paper: dict) -> dict:
    """Synthesizes all voice outputs into one paragraph. Falls back to abstract on failure."""
    prompt = _build_synthesis_prompt(paper)
    options = ClaudeAgentOptions(system_prompt=SYSTEM_PROMPT, max_turns=1, model=MODEL)
    result_parts = []
    try:
        async for msg in query(prompt=prompt, options=options):
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        result_parts.append(block.text)
    except Exception as e:
        logger.warning(f"Synthesizer failed for PMID {paper.get('pmid', '?')}: {e}")
        return {**paper, "synthesis": paper.get("abstract", "Synthesis unavailable.")}

    synthesis = "\n".join(result_parts).strip()
    if not synthesis:
        synthesis = paper.get("abstract", "Synthesis unavailable.")

    return {**paper, "synthesis": synthesis}


async def synthesize_all(papers: list[dict]) -> list[dict]:
    """Synthesizes all papers concurrently."""
    results = await asyncio.gather(*[synthesize_paper(p) for p in papers], return_exceptions=True)
    synthesized = []
    for paper, result in zip(papers, results):
        if isinstance(result, Exception):
            logger.warning(f"Unexpected synthesis error for PMID {paper.get('pmid', '?')}: {result}")
            synthesized.append({**paper, "synthesis": paper.get("abstract", "Synthesis unavailable.")})
        else:
            synthesized.append(result)
    return synthesized
