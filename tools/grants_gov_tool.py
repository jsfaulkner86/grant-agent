import httpx
from typing import Optional

GRANTS_GOV_API = "https://apply07.grants.gov/grantsws/rest/opportunities/search"

def search_grants_gov(
    keyword: str,
    agency: Optional[str] = None,
    max_results: int = 25,
) -> list[dict]:
    """
    Search Grants.gov for open opportunities matching a keyword.
    Returns a list of opportunity dicts.
    """
    payload = {
        "keyword": keyword,
        "oppStatuses": "forecasted|posted",
        "rows": max_results,
        "sortBy": "openDate|desc",
    }
    if agency:
        payload["agencyCode"] = agency

    response = httpx.post(GRANTS_GOV_API, json=payload, timeout=20)
    response.raise_for_status()
    data = response.json()
    return data.get("oppHits", [])
