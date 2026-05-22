import asyncio
import os
import logging
import httpx

logger = logging.getLogger(__name__)

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


class PubMedError(Exception):
    pass


class PubMedClient:
    def __init__(self):
        self.api_key = os.getenv("NCBI_API_KEY")
        limit = 10 if self.api_key else 3
        self._sem = asyncio.Semaphore(limit)
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "PubMedClient":
        self._client = httpx.AsyncClient(timeout=30.0)
        return self

    async def __aexit__(self, *_):
        if self._client:
            await self._client.aclose()

    async def _get(self, url: str, params: dict) -> str:
        if self.api_key:
            params = {**params, "api_key": self.api_key}
        async with self._sem:
            try:
                resp = await self._client.get(url, params=params)
                resp.raise_for_status()
                return resp.text
            except httpx.TimeoutException:
                logger.warning("PubMed timeout, retrying in 2s...")
                await asyncio.sleep(2)
                resp = await self._client.get(url, params=params)
                resp.raise_for_status()
                return resp.text
            except httpx.HTTPStatusError as e:
                raise PubMedError(f"HTTP {e.response.status_code} from PubMed") from e

    async def search(self, query: str, retmax: int) -> list[str]:
        """Returns list of PMIDs. Returns [] on empty result."""
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": str(retmax),
            "retmode": "json",
            "usehistory": "n",
        }
        try:
            text = await self._get(ESEARCH_URL, params)
        except PubMedError as e:
            logger.warning(f"esearch failed: {e}")
            return []

        import json
        try:
            data = json.loads(text)
            return data.get("esearchresult", {}).get("idlist", [])
        except Exception as e:
            logger.warning(f"esearch JSON parse error: {e}")
            return []

    async def fetch(self, pmids: list[str]) -> str:
        """Returns raw XML string for a list of PMIDs."""
        if not pmids:
            return ""
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
            "rettype": "abstract",
        }
        try:
            return await self._get(EFETCH_URL, params)
        except PubMedError as e:
            logger.warning(f"efetch failed: {e}")
            return ""

    async def search_and_fetch(self, query_spec: dict) -> list[dict]:
        """Full round-trip: search → fetch → parse. Returns list of PaperRecord dicts."""
        from .xml_parser import parse_articles

        specialty = query_spec["specialty"]
        query = query_spec["query"]
        retmax = query_spec["retmax"]

        pmids = await self.search(query, retmax)
        if not pmids:
            return []

        xml = await self.fetch(pmids)
        if not xml:
            return []

        return parse_articles(xml, specialty)
