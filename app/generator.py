import asyncio
from typing import Iterable

from openai import AsyncOpenAI
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.config import settings
from app.models import CopyRequest, GeneratedCopy
from app.prompts import compile_prompt
from app.validators import build_result


class CopyGenerator:

    def __init__(self) -> None:

        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Check your .env file."
            )

        # Google Gemini OpenAI-compatible API
        self.client = AsyncOpenAI(
            api_key=settings.gemini_api_key,
            base_url=(
                "https://generativelanguage.googleapis.com/"
                "v1beta/openai/"
            ),
            timeout=settings.request_timeout,
        )

        self.semaphore = asyncio.Semaphore(
            settings.max_concurrency
        )

    @retry(
        stop=stop_after_attempt(settings.retry_attempts),
        wait=wait_exponential(
            multiplier=1,
            min=1,
            max=20,
        ),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    async def _call_model(
        self,
        request: CopyRequest,
    ) -> str:

        # Create the dynamic prompt
        prompt = compile_prompt(
            request.product_name,
            request.description,
            request.platform,
            request.tone,
        )

        # Send request to Google Gemini
        response = await self.client.chat.completions.create(
            model=request.model or settings.gemini_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=request.temperature,
            top_p=request.top_p,
        )

        # Get generated text
        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return content.strip()

    async def generate_one(
        self,
        request: CopyRequest,
    ) -> GeneratedCopy:

        # Limit the number of simultaneous API requests
        async with self.semaphore:

            content = await self._call_model(request)

        model_name = (
            request.model
            or settings.gemini_model
        )

        # Validate and build final result
        return build_result(
            product_name=request.product_name,
            platform=request.platform,
            tone=request.tone,
            content=content,
            model=model_name,
            temperature=request.temperature,
            top_p=request.top_p,
        )

    async def generate_many(
        self,
        requests: Iterable[CopyRequest],
    ) -> list[GeneratedCopy]:

        # Create tasks for multiple requests
        tasks = [
            asyncio.create_task(
                self.generate_one(item)
            )
            for item in requests
        ]

        # Run tasks asynchronously
        return await asyncio.gather(*tasks)

    async def close(self) -> None:

        await self.client.close()