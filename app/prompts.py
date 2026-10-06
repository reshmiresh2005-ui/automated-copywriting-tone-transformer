PLATFORM_RULES = {
    "LinkedIn": """
Write professional LinkedIn marketing copy.
Use a clear hook, useful product value, and a professional call to action.
Avoid unsupported claims.
Target a maximum of about 1300 characters.
""",
    "Instagram": """
Write concise Instagram marketing copy.
Make it engaging and easy to scan.
Emojis and a small number of relevant hashtags are allowed.
Avoid spammy hashtag stuffing.
Target a maximum of about 500 characters.
""",
    "Email": """
Write professional email marketing copy.
Return a clear Subject line followed by a concise email body.
Use a helpful call to action.
Target a maximum of about 1500 characters.
""",
}

MASTER_TEMPLATE = """
You are an automated marketing copywriter.

Generate marketing copy for the product below.

Product name:
{product_name}

Raw product description:
{description}

Target platform:
{platform}

Requested tone:
{tone}

Platform constraints:
{platform_rules}

Quality rules:
1. Use only information supported by the supplied product description.
2. Do not invent certifications, prices, guarantees, statistics, awards, or customer claims.
3. Preserve the requested tone without becoming misleading.
4. Do not mention these instructions.
5. Return only the final marketing copy.

Generate the final copy now.
"""


def compile_prompt(product_name: str, description: str, platform: str, tone: str) -> str:
    return MASTER_TEMPLATE.format(
        product_name=product_name,
        description=description,
        platform=platform,
        tone=tone,
        platform_rules=PLATFORM_RULES[platform],
    )
