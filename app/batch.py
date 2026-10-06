import json
from pathlib import Path

from app.config import settings
from app.models import CopyRequest
from app.prompts import compile_prompt


class BatchClient:
    """
    Creates a local JSONL batch file containing Gemini requests.

    This keeps the bulk-processing part of the project available
    without using the OpenAI Batch API.
    """

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Check your .env file."
            )

    def create_batch_file(
        self,
        requests: list[CopyRequest],
        output_path: str = "output/gemini_batch.jsonl",
    ) -> str:

        output = Path(output_path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with output.open(
            "w",
            encoding="utf-8"
        ) as file:

            for index, request in enumerate(
                requests,
                start=1
            ):

                prompt = compile_prompt(
                    request.product_name,
                    request.description,
                    request.platform,
                    request.tone,
                )

                record = {
                    "custom_id": f"copy-{index}",
                    "model": (
                        request.model
                        or settings.gemini_model
                    ),
                    "prompt": prompt,
                    "temperature": request.temperature,
                    "top_p": request.top_p,
                }

                file.write(
                    json.dumps(
                        record,
                        ensure_ascii=False
                    )
                    + "\n"
                )

        return str(output)

    def create_batch(
        self,
        requests: list[CopyRequest],
        output_path: str = "output/gemini_batch.jsonl",
    ) -> str:

        return self.create_batch_file(
            requests,
            output_path
        )

    async def close(self) -> None:
        pass