from app.models import GeneratedCopy


PLATFORM_LIMITS = {
    "LinkedIn": 1300,
    "Instagram": 500,
    "Email": 1500,
}


def validate_generated_text(content: str, platform: str) -> tuple[int, bool]:
    count = len(content)
    return count, count <= PLATFORM_LIMITS[platform]


def build_result(
    *,
    product_name: str,
    platform: str,
    tone: str,
    content: str,
    model: str,
    temperature: float,
    top_p: float,
) -> GeneratedCopy:
    count, within_target = validate_generated_text(content, platform)
    return GeneratedCopy(
        product_name=product_name,
        platform=platform,
        tone=tone,
        content=content,
        character_count=count,
        within_target=within_target,
        model=model,
        temperature=temperature,
        top_p=top_p,
    )
