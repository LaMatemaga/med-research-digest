import asyncio
import logging
from search.query_builder import build_esearch_queries
from search.pubmed_client import PubMedClient

logger = logging.getLogger(__name__)


async def run_discovery(
    profile: dict,
    days: int,
    specialty_override: str | None = None,
    dry_run: bool = False,
) -> list[dict]:
    """
    Runs all PubMed searches derived from the physician profile.
    Returns a deduplicated list of PaperRecord dicts.
    """
    query_specs = build_esearch_queries(profile, days, specialty_override)

    if not query_specs:
        print("  No specialties configured in profile. Add specialties to context/physician.py.")
        return []

    if dry_run:
        print("\n--- DRY RUN: PubMed queries that would be executed ---\n")
        for spec in query_specs:
            print(f"Specialty: {spec['specialty']}")
            print(f"  Query:  {spec['query']}")
            print(f"  retmax: {spec['retmax']}")
            print()
        return []

    async with PubMedClient() as client:
        tasks = [client.search_and_fetch(spec) for spec in query_specs]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    all_papers: list[dict] = []
    for spec, result in zip(query_specs, results):
        if isinstance(result, Exception):
            logger.warning(f"Search failed for '{spec['specialty']}': {result}")
            continue
        all_papers.extend(result)

    deduped = _dedup(all_papers)
    print(f"  Discovery: {len(deduped)} papers found across {len(query_specs)} specialty searches")
    return deduped


def _dedup(papers: list[dict]) -> list[dict]:
    """Keeps first occurrence per PMID. Preserves insertion order."""
    seen: set[str] = set()
    result = []
    for paper in papers:
        pmid = paper.get("pmid", "")
        if pmid and pmid not in seen:
            seen.add(pmid)
            result.append(paper)
    return result
