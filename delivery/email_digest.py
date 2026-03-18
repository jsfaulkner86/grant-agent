import resend
from config.settings import settings

resend.api_key = settings.resend_api_key

def build_grant_row(grant: dict, match: dict) -> str:
    score_color = "#2e7d32" if match.get("match_score", 0) >= 70 else "#e65100"
    return f"""
    <tr style='border-bottom:1px solid #eee'>
      <td style='padding:14px'>
        <strong>{grant.get('name', 'Unknown Grant')}</strong><br/>
        <em>{grant.get('funder', '')} &mdash; {grant.get('type', '')}</em><br/>
        <span style='color:{score_color}'><strong>Match Score: {match.get('match_score', 'N/A')}/100</strong></span><br/>
        💰 Award: {grant.get('award_range', 'Unknown')} &nbsp;|&nbsp;
        📅 Deadline: {grant.get('deadline', 'See link')}<br/>
        <small>{match.get('match_rationale', '')}</small><br/>
        <a href='{grant.get('url', '#')}'>View Opportunity →</a>
      </td>
    </tr>
    """

def send_grant_digest(recipient_email: str, founder_name: str, grants_with_matches: list[tuple]):
    if not grants_with_matches:
        print(f"No grants above threshold for {founder_name} — skipping.")
        return

    rows = "".join(build_grant_row(g, m) for g, m in grants_with_matches[:8])
    html_body = f"""
    <html><body style='font-family:sans-serif;max-width:700px;margin:auto'>
      <h2 style='color:#1a237e'>💰 Non-Dilutive Funding Opportunities</h2>
      <p style='color:#555'>Hi {founder_name}, here are your matched grant opportunities from <strong>The Faulkner Group</strong>.</p>
      <table width='100%' cellpadding='0' cellspacing='0'>
        {rows}
      </table>
      <p style='color:#555;margin-top:20px'>Full application outlines are available in your Notion dashboard.</p>
      <hr/>
      <p style='font-size:12px;color:#999'>Powered by Grant Agent — The Faulkner Group Advisors</p>
    </body></html>
    """
    resend.Emails.send({
        "from": settings.digest_from_email,
        "to": recipient_email,
        "subject": f"Your Non-Dilutive Funding Opportunities — {founder_name}",
        "html": html_body,
    })
    print(f"Grant digest sent to {recipient_email}")
