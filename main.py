import asyncio
import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

from context.physician import PROFILE
from pipeline.stage1_discovery import run_discovery
from pipeline.stage2_evidence_grader import grade_all
from pipeline.stage3_relevance_filter import filter_papers
from pipeline.stage4_voices import run_all_voices
from pipeline.stage5_synthesizer import synthesize_all
from pipeline.stage6_formatter import assign_tier, format_newsletter, save_newsletter


async def run_pipeline(days: int, specialty_override: str | None, dry_run: bool) -> None:
    today = date.today()
    start = today - timedelta(days=days)
    date_range = f"{start.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}"

    print(f"\nmed-research-digest | {today} | last {days} days")
    if specialty_override:
        print(f"  Specialty override: {specialty_override}")
    print()

    # Stage 1: Discovery
    print("Stage 1: Discovery (PubMed)...")
    papers = await run_discovery(PROFILE, days, specialty_override, dry_run)
    if dry_run:
        return

    n_found = len(papers)
    if not papers:
        print("\nNo papers found. Try --days 30 or add specialties to context/physician.py.")
        return

    # Stage 2: Evidence grading
    print(f"\nStage 2: Grading evidence levels for {n_found} papers...")
    papers = await grade_all(papers)
    print(f"  Graded: {len(papers)} papers")

    # Stage 3: Relevance filter
    print(f"\nStage 3: Relevance filtering...")
    papers = await filter_papers(papers, PROFILE)

    if not papers:
        print(
            "\nAll papers filtered out. Try --days 30, --specialty <name>, or "
            "lower min_evidence_level in context/physician.py."
        )
        return

    # Stage 4: Voices
    print(f"\nStage 4: Running voices ({len(papers)} papers, voices run in parallel per paper)...")
    papers = await run_all_voices(papers, PROFILE)
    print(f"  Voices complete for {len(papers)} papers")

    # Stage 5: Synthesis
    print(f"\nStage 5: Synthesizing narratives...")
    papers = await synthesize_all(papers)
    print(f"  Synthesized: {len(papers)} papers")

    # Stage 6: Format and save
    print("\nStage 6: Formatting newsletter...")
    content = format_newsletter(papers, PROFILE, date_range)
    output_dir = str(Path(__file__).parent / "outputs")
    output_path = save_newsletter(content, output_dir)

    # Console summary
    tiers = [assign_tier(p) for p in papers]
    n_red = tiers.count("🔴")
    n_yellow = tiers.count("🟡")
    n_blue = tiers.count("🔵")

    print(f"\n{'=' * 50}")
    print(f"med-research-digest complete")
    print(f"  Papers found:    {n_found}")
    print(f"  Papers included: {len(papers)}")
    print(f"  🔴 High:         {n_red}")
    print(f"  🟡 Moderate:     {n_yellow}")
    print(f"  🔵 Watching:     {n_blue}")
    print(f"  Saved to:        {output_path}")
    print(f"{'=' * 50}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Medical research newsletter generator powered by PubMed + Claude",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # last 7 days, all profile specialties
  python main.py --days 30               # last 30 days
  python main.py --specialty cardiology  # override to cardiology only
  python main.py --dry-run               # show PubMed queries, don't fetch
        """,
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Lookback window in days (default: 7)",
    )
    parser.add_argument(
        "--specialty",
        type=str,
        default=None,
        metavar="SPECIALTY",
        help="Override specialty filter (e.g. cardiology, oncology)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show PubMed queries without fetching or calling Claude",
    )
    args = parser.parse_args()

    if not PROFILE.get("specialties") and not args.specialty:
        print(
            "Warning: No specialties configured in context/physician.py.\n"
            "Add specialties or use --specialty <name> to override.\n"
        )

    asyncio.run(run_pipeline(args.days, args.specialty, args.dry_run))


if __name__ == "__main__":
    main()
