# Founder profiles drive grant matching.
# Add one entry per advisory client. Stage, indication, and product_type
# are used by the matching agent to score relevance.

FOUNDER_PROFILES = [
    {
        "client_id": "client_001",
        "company": "Example Women's Health Co.",
        "founder_name": "Founder Name",
        "email": "founder@example.com",
        "stage": "Seed",  # Pre-Seed | Seed | Series A | Series B
        "indication": "maternal health",  # e.g. maternal health, menopause, endometriosis, fertility
        "product_type": "digital therapeutic",  # device | diagnostic | digital therapeutic | drug | platform
        "geography": "US",
        "has_sbir_before": False,
        "nonprofit_eligible": False,
        "target_award_min": 50000,
        "target_award_max": 2000000,
    },
    # Add additional client profiles here
]
