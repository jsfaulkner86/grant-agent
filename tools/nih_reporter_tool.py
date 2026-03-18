import httpx

NIH_REPORTER_API = "https://api.reporter.nih.gov/v2/projects/search"

def search_nih_funding(
    terms: list[str],
    fiscal_years: list[int] = None,
    activity_codes: list[str] = None,
) -> list[dict]:
    """
    Search NIH Reporter for active funding programs.
    activity_codes: e.g. ['R01', 'R43', 'R44'] for SBIR phases
    """
    fiscal_years = fiscal_years or [2025, 2026]
    activity_codes = activity_codes or ["R43", "R44", "U44", "R41", "R42"]

    payload = {
        "criteria": {
            "advanced_text_search": {
                "operator": "and",
                "search_field": "all",
                "search_text": " ".join(terms),
            },
            "fiscal_years": fiscal_years,
            "activity_codes": activity_codes,
        },
        "limit": 25,
        "offset": 0,
        "sort_field": "project_start_date",
        "sort_order": "desc",
    }
    response = httpx.post(NIH_REPORTER_API, json=payload, timeout=20)
    response.raise_for_status()
    return response.json().get("results", [])
