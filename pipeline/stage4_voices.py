import asyncio
import logging
from voices import select_voices

logger = logging.getLogger(__name__)


async def run_voices_for_paper(paper: dict, voices: dict) -> dict:
    """Runs all active voices concurrently for a single paper."""
    names = list(voices.keys())
    callables = list(voices.values())

    results = await asyncio.gather(*[v(paper) for v in callables], return_exceptions=True)

    voice_outputs: dict[str, str | None] = {}
    for name, result in zip(names, results):
        if isinstance(result, Exception):
            logger.warning(
                f"Voice '{name}' failed for PMID {paper.get('pmid', '?')}: {result}"
            )
            voice_outputs[name] = None
        else:
            voice_outputs[name] = result

    return {**paper, "voice_outputs": voice_outputs}


async def run_all_voices(papers: list[dict], profile: dict) -> list[dict]:
    """
    Processes papers sequentially; each paper's voices run in parallel.
    Sequential papers avoid 60+ simultaneous Claude calls for large digests.
    """
    voices = select_voices(profile)
    voiced_papers = []
    for i, paper in enumerate(papers, 1):
        logger.debug(f"  Running voices for paper {i}/{len(papers)}: {paper.get('pmid', '?')}")
        voiced = await run_voices_for_paper(paper, voices)
        voiced_papers.append(voiced)
    return voiced_papers
