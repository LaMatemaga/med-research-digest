from datetime import date, timedelta
from .mesh_terms import get_mesh_terms, get_pubtype_filter, SPECIALTY_MESH


def build_esearch_queries(
    profile: dict,
    days: int,
    specialty_override: str | None = None,
) -> list[dict]:
    """
    Returns one query dict per specialty/subspecialty/research_interest:
      {"specialty": str, "query": str, "retmax": int}
    """
    max_papers = profile.get("newsletter_preferences", {}).get("max_papers", 10)
    retmax = max_papers * 3

    date_filter = _build_date_filter(days)
    pubtype_clause = get_pubtype_filter(profile.get("role", []))

    if specialty_override:
        groups = _groups_for_override(specialty_override)
    else:
        groups = get_mesh_terms(
            profile.get("specialties", []),
            profile.get("subspecialties", []),
        )
        for interest in profile.get("research_interests", []):
            key = interest.lower().strip()
            if key not in SPECIALTY_MESH:
                groups.append((interest, [f"{interest}[TIAB]"]))

    queries = []
    for label, mesh_list in groups:
        mesh_clause = "(" + " OR ".join(mesh_list) + ")"
        parts = [mesh_clause]
        if pubtype_clause:
            parts.append(pubtype_clause)
        parts.append(date_filter)
        query = " AND ".join(parts)
        queries.append({"specialty": label, "query": query, "retmax": retmax})

    return queries


def _build_date_filter(days: int) -> str:
    today = date.today()
    start = today - timedelta(days=days)
    return f"({start.strftime('%Y/%m/%d')}:{today.strftime('%Y/%m/%d')}[PDAT])"


def _groups_for_override(specialty: str) -> list[tuple[str, list[str]]]:
    key = specialty.lower().strip()
    if key in SPECIALTY_MESH:
        return [(specialty, SPECIALTY_MESH[key])]
    return [(specialty, [f"{specialty}[TIAB]"])]
