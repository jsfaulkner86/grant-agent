import httpx

SBIR_API = "https://www.sbir.gov/api/solicitations.json"

def search_sbir_solicitations(keyword: str, agency: str = None) -> list[dict]:
    """
    Search SBIR.gov for open solicitations.
    Optionally filter by agency: HHS, NIH, NSF, DOD, etc.
    """
    params = {
        "keyword": keyword,
        "open": 1,
        "rows": 25,
    }
    if agency:
        params["agency"] = agency

    response = httpx.get(SBIR_API, params=params, timeout=20)
    response.raise_for_status()
    return response.json().get("results", [])
