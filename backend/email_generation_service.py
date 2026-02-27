import os
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


async def generate_email(
    contact: dict,
    interactions: list,
    template: dict = None,
    custom_instructions: str = "",
) -> dict:
    """
    Generate a personalized email for a contact.
    Uses OpenAI API if OPENAI_API_KEY is set, otherwise falls back to template.
    Returns: {subject: str, body: str}
    """
    if OPENAI_API_KEY:
        return await _llm_generate(contact, interactions, template, custom_instructions)
    return _template_generate(contact, template, custom_instructions)


def _template_generate(contact: dict, template: dict = None, custom_instructions: str = "") -> dict:
    """Simple template-based fallback when no API key is set."""
    first = contact.get("first_name", "there")
    last = contact.get("last_name", "")
    company = contact.get("company_name", "your company")
    job_title = contact.get("job_title", "")

    if template:
        subject = template.get("subject_template", "Following up")
        body = template.get("body_template", "")
        # Simple placeholder replacement
        for key, val in [("{first_name}", first), ("{last_name}", last),
                         ("{company}", company), ("{job_title}", job_title)]:
            subject = subject.replace(key, val)
            body = body.replace(key, val)
    else:
        subject = f"Following up - {first} {last}"
        body = (
            f"Hi {first},\n\n"
            f"I hope this message finds you well"
            f"{f' at {company}' if company and company != 'your company' else ''}. "
            f"I wanted to reach out regarding a potential collaboration.\n\n"
            f"{custom_instructions + chr(10) + chr(10) if custom_instructions else ''}"
            f"Would you be available for a quick call this week?\n\n"
            f"Best regards"
        )

    return {"subject": subject, "body": body}


async def _llm_generate(
    contact: dict,
    interactions: list,
    template: dict = None,
    custom_instructions: str = "",
) -> dict:
    """Generate email using OpenAI API."""
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    # Build interaction context
    interaction_lines = []
    for ix in interactions[:10]:
        ix_type = ix.get("type", "")
        ix_date = ix.get("occurred_at", "")
        ix_subject = ix.get("subject", "")
        ix_content = ix.get("content", "")[:200]
        interaction_lines.append(f"- [{ix_type}] {ix_date}: {ix_subject} — {ix_content}")
    context = "\n".join(interaction_lines) if interaction_lines else "No previous interactions."

    system_prompt = (
        "You are a professional sales email writer for NexaCRM. "
        "Write personalized, concise emails that are warm but professional. "
        "Always respond with valid JSON containing exactly two keys: \"subject\" and \"body\"."
    )

    user_prompt = (
        f"Generate a sales email for this contact:\n\n"
        f"Name: {contact.get('first_name', '')} {contact.get('last_name', '')}\n"
        f"Job Title: {contact.get('job_title', 'N/A')}\n"
        f"Company: {contact.get('company_name', 'N/A')}\n"
        f"Lead Score Level: {contact.get('lead_score_level', 'N/A')}\n\n"
        f"Recent interactions:\n{context}\n\n"
    )
    if template:
        user_prompt += f"Template guidance:\nSubject: {template.get('subject_template', '')}\nBody: {template.get('body_template', '')}\n\n"
    if custom_instructions:
        user_prompt += f"Additional instructions: {custom_instructions}\n\n"
    user_prompt += 'Respond with JSON: {"subject": "...", "body": "..."}'

    response = await client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    try:
        text = response.choices[0].message.content.strip()
        # Strip markdown code fences that GPT often wraps JSON in
        if text.startswith("```"):
            # Remove opening fence (```json or ```)
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            # Remove closing fence
            if text.endswith("```"):
                text = text[:-3].strip()
        result = json.loads(text)
        return {"subject": result["subject"], "body": result["body"]}
    except (json.JSONDecodeError, KeyError, IndexError):
        # Fallback: try to extract from raw text
        raw = response.choices[0].message.content
        return {"subject": "Follow-up", "body": raw}
