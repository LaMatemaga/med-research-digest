import logging
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


def parse_articles(xml_text: str, source_specialty: str) -> list[dict]:
    """Parses PubmedArticleSet XML into a list of PaperRecord dicts."""
    if not xml_text.strip():
        return []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        logger.warning(f"XML parse error for specialty '{source_specialty}': {e}")
        return []

    papers = []
    for article_el in root.findall(".//PubmedArticle"):
        try:
            paper = _parse_single(article_el, source_specialty)
            if paper:
                papers.append(paper)
        except Exception as e:
            pmid = _get_pmid(article_el)
            logger.warning(f"Skipping PMID {pmid}: {e}")
    return papers


def _parse_single(article_el: ET.Element, source_specialty: str) -> dict | None:
    pmid = _get_pmid(article_el)
    if not pmid:
        return None

    medline = article_el.find(".//MedlineCitation")
    article = article_el.find(".//Article")
    if medline is None or article is None:
        return None

    title_el = article.find(".//ArticleTitle")
    title = _extract_text(title_el) if title_el is not None else ""

    journal_el = article.find(".//Journal/Title")
    journal = journal_el.text.strip() if journal_el is not None and journal_el.text else ""

    pub_date_el = article.find(".//Journal/JournalIssue/PubDate")
    pub_date = _parse_pub_date(pub_date_el) if pub_date_el is not None else ""

    authors = _parse_authors(article)
    abstract = _parse_abstract(article)
    pub_types = [
        pt.text.strip()
        for pt in article.findall(".//PublicationTypeList/PublicationType")
        if pt.text
    ]
    mesh_terms = [
        dn.text.strip()
        for dn in medline.findall(".//MeshHeadingList/MeshHeading/DescriptorName")
        if dn.text
    ]

    return {
        "pmid": pmid,
        "title": title,
        "authors": authors,
        "journal": journal,
        "pub_date": pub_date,
        "abstract": abstract,
        "publication_types": pub_types,
        "mesh_terms": mesh_terms,
        "source_specialty": source_specialty,
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
    }


def _get_pmid(article_el: ET.Element) -> str:
    pmid_el = article_el.find(".//PMID")
    return pmid_el.text.strip() if pmid_el is not None and pmid_el.text else ""


def _extract_text(element: ET.Element) -> str:
    """Extracts all text including subelement tails (handles <i>, <b> in titles)."""
    parts = []
    if element.text:
        parts.append(element.text)
    for child in element:
        if child.text:
            parts.append(child.text)
        if child.tail:
            parts.append(child.tail)
    return "".join(parts).strip()


def _parse_authors(article_el: ET.Element) -> list[str]:
    authors = []
    for author in article_el.findall(".//AuthorList/Author"):
        last = author.findtext("LastName", "").strip()
        initials = author.findtext("Initials", "").strip()
        collective = author.findtext("CollectiveName", "").strip()
        if last:
            authors.append(f"{last} {initials}".strip())
        elif collective:
            authors.append(collective)
    return authors


def _parse_pub_date(pub_date_el: ET.Element) -> str:
    medline_date = pub_date_el.findtext("MedlineDate", "").strip()
    if medline_date:
        return medline_date

    year = pub_date_el.findtext("Year", "").strip()
    month = pub_date_el.findtext("Month", "").strip()
    day = pub_date_el.findtext("Day", "").strip()

    if year and month and day:
        return f"{year}-{month}-{day}"
    if year and month:
        return f"{year}-{month}"
    return year


def _parse_abstract(article_el: ET.Element) -> str:
    sections = []
    for abstract_text in article_el.findall(".//Abstract/AbstractText"):
        label = abstract_text.get("Label", "")
        text = _extract_text(abstract_text)
        if not text:
            continue
        if label:
            sections.append(f"{label}: {text}")
        else:
            sections.append(text)
    return " ".join(sections)
