import httpx
from config.settings import settings

PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"

def search_grants(query: str) -> str:
    """
    Use Perplexity Sonar to research private foundation grants,
    prize competitions, and state programs for women's health.
    """
    headers = {
        "Authorization": f"Bearer {settings.perplexity_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a grant research specialist for women's health tech startups. "
                    "Surface non-dilutive funding opportunities including: private foundation grants, "
                    "prize competitions, accelerator funding, state SBIR match programs, and "
                    "federal programs beyond NIH. Return opportunity name, funder, award range, "
                    "deadline if known, eligibility criteria, and application URL."
                ),
            },
            {"role": "user", "content": query},
        ],
    }
    response = httpx.post(PERPLEXITY_URL, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
