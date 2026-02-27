import os
import re
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


async def enrich_from_linkedin(linkedin_url: str) -> dict:
    """
    Enrich contact data from a LinkedIn URL.
    Uses OpenAI if API key is set, otherwise falls back to mock data.
    Returns: {success: bool, data: {...}, error: str|None}
    """
    if OPENAI_API_KEY:
        return await _openai_enrich(linkedin_url)
    return _mock_enrich(linkedin_url)


def _mock_enrich(linkedin_url: str) -> dict:
    """Return deterministic mock data based on the LinkedIn URL."""
    match = re.search(r"linkedin\.com/in/([a-zA-Z0-9-]+)", linkedin_url)
    if not match:
        return {
            "success": False,
            "data": None,
            "error": "Invalid LinkedIn URL format. Expected: linkedin.com/in/username",
        }

    slug = match.group(1)
    parts = slug.split("-")
    first_name = parts[0].capitalize() if parts else "Unknown"
    last_name = parts[1].capitalize() if len(parts) > 1 else "User"

    titles = [
        "Senior Software Engineer",
        "VP of Sales",
        "Product Manager",
        "Marketing Director",
        "CTO",
        "Account Executive",
        "Data Scientist",
    ]
    companies = [
        "TechCorp Inc.",
        "Salesforce",
        "Acme Corp",
        "DataVision",
        "CloudScale",
        "InnovateCo",
        "GlobalTech",
    ]

    idx = sum(ord(c) for c in slug)
    job_title = titles[idx % len(titles)]
    company_name = companies[idx % len(companies)]

    industries = ["TECHNOLOGY", "SERVICES", "FINANCE", "RETAIL", "HEALTHCARE", "MANUFACTURING", "OTHER"]
    industry = industries[idx % len(industries)]

    return {
        "success": True,
        "data": {
            "first_name": first_name,
            "last_name": last_name,
            "job_title": job_title,
            "company_name": company_name,
            "industry": industry,
            "profile_picture_url": f"https://ui-avatars.com/api/?name={first_name}+{last_name}&background=5a3d91&color=fff&size=200",
        },
        "error": None,
    }


async def _openai_enrich(linkedin_url: str) -> dict:
    """Enrich contact data using OpenAI based on the LinkedIn URL."""
    from openai import AsyncOpenAI

    match = re.search(r"linkedin\.com/in/([a-zA-Z0-9-]+)", linkedin_url)
    if not match:
        return {
            "success": False,
            "data": None,
            "error": "Invalid LinkedIn URL format. Expected: linkedin.com/in/username",
        }

    slug = match.group(1)

    client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    prompt = (
        f"Based on this LinkedIn profile URL slug: '{slug}', generate realistic professional contact information. "
        f"The slug usually contains the person's name (e.g., 'john-doe' means John Doe).\n\n"
        f"Return valid JSON with exactly these keys:\n"
        f'{{"first_name": "...", "last_name": "...", "job_title": "...", "company_name": "...", "industry": "..."}}\n\n'
        f"industry must be one of: TECHNOLOGY, SERVICES, FINANCE, RETAIL, HEALTHCARE, MANUFACTURING, OTHER.\n"
        f"Make the job title and company realistic and professional. Do not use generic placeholders."
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            max_tokens=200,
            messages=[
                {"role": "system", "content": "You are a data enrichment assistant. Return only valid JSON, no markdown fences."},
                {"role": "user", "content": prompt},
            ],
        )

        text = response.choices[0].message.content.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3].strip()

        data = json.loads(text)
        first_name = data.get("first_name", slug.split("-")[0].capitalize())
        last_name = data.get("last_name", slug.split("-")[-1].capitalize() if "-" in slug else "")

        return {
            "success": True,
            "data": {
                "first_name": first_name,
                "last_name": last_name,
                "job_title": data.get("job_title", ""),
                "company_name": data.get("company_name", ""),
                "industry": data.get("industry", "OTHER"),
                "profile_picture_url": f"https://ui-avatars.com/api/?name={first_name}+{last_name}&background=5a3d91&color=fff&size=200",
            },
            "error": None,
        }
    except Exception as e:
        # Fall back to mock if OpenAI fails
        return _mock_enrich(linkedin_url)
