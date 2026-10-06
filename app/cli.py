import argparse
import asyncio
import json
from pathlib import Path

from app.generator import CopyGenerator
from app.models import CopyRequest


def parse_args():
    parser = argparse.ArgumentParser(
        description="Automated Copywriting & Tone Transformer"
    )

    parser.add_argument("--product-name")
    parser.add_argument("--description")
    parser.add_argument(
        "--platform",
        choices=["LinkedIn", "Instagram", "Email"]
    )
    parser.add_argument("--tone")

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7
    )

    parser.add_argument(
        "--top-p",
        type=float,
        default=0.9
    )

    parser.add_argument("--model")

    parser.add_argument(
        "--input",
        help="Path to one JSON request"
    )

    parser.add_argument(
        "--bulk",
        help="Path to JSONL requests for bulk generation"
    )

    parser.add_argument(
        "--batch",
        help="Path to JSONL requests for batch-style local processing"
    )

    parser.add_argument(
        "--output",
        default="output/result.json"
    )

    return parser.parse_args()


def load_single(path: str) -> CopyRequest:
    data = json.loads(
        Path(path).read_text(encoding="utf-8")
    )

    return CopyRequest.model_validate(data)


def load_bulk(path: str) -> list[CopyRequest]:
    requests = []

    for line in Path(path).read_text(
        encoding="utf-8"
    ).splitlines():

        if line.strip():
            data = json.loads(line)
            requests.append(
                CopyRequest.model_validate(data)
            )

    return requests


def interactive_request() -> CopyRequest:
    print("\n=== Automated Copywriting & Tone Transformer ===\n")

    product_name = input("Product name: ").strip()

    description = input(
        "Product description: "
    ).strip()

    platform = input(
        "Platform (LinkedIn/Instagram/Email): "
    ).strip()

    tone = input(
        "Tone (e.g. Professional, Friendly, Witty): "
    ).strip()

    temperature = float(
        input("Temperature [0.7]: ") or "0.7"
    )

    top_p = float(
        input("Top-P [0.9]: ") or "0.9"
    )

    return CopyRequest(
        product_name=product_name,
        description=description,
        platform=platform,
        tone=tone,
        temperature=temperature,
        top_p=top_p,
    )


def save_json(data, path: str) -> None:
    destination = Path(path)

    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    destination.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


async def generate(
    requests: list[CopyRequest]
):
    generator = CopyGenerator()

    try:
        results = await generator.generate_many(
            requests
        )

        return [
            item.model_dump()
            for item in results
        ]

    finally:
        await generator.close()


async def process_batch(
    path: str,
    output_path: str
):
    """
    Gemini-compatible batch-style processing.

    Reads JSONL requests and processes them
    using the same Gemini generator.
    """

    requests = load_bulk(path)

    results = await generate(requests)

    save_json(
        results,
        output_path
    )

    return results


def run() -> None:

    args = parse_args()

    # -----------------------------------------
    # BATCH MODE
    # -----------------------------------------

    if args.batch:

        results = asyncio.run(
            process_batch(
                args.batch,
                args.output
            )
        )

        print(
            f"\nProcessed {len(results)} requests."
        )

        print(
            f"Saved to: {args.output}"
        )

        return

    # -----------------------------------------
    # INPUT / BULK / COMMAND-LINE MODE
    # -----------------------------------------

    if args.input:

        requests = [
            load_single(args.input)
        ]

    elif args.bulk:

        requests = load_bulk(args.bulk)

    elif all([
        args.product_name,
        args.description,
        args.platform,
        args.tone
    ]):

        requests = [
            CopyRequest(
                product_name=args.product_name,
                description=args.description,
                platform=args.platform,
                tone=args.tone,
                temperature=args.temperature,
                top_p=args.top_p,
                model=args.model,
            )
        ]

    else:

        requests = [
            interactive_request()
        ]

    # -----------------------------------------
    # GENERATE COPY
    # -----------------------------------------

    results = asyncio.run(
        generate(requests)
    )

    # -----------------------------------------
    # SAVE RESULTS
    # -----------------------------------------

    save_json(
        results,
        args.output
    )

    # -----------------------------------------
    # DISPLAY RESULTS
    # -----------------------------------------

    for result in results:

        print("\n--- GENERATED COPY ---")

        print(
            result["content"]
        )

        print(
            f"\nCharacters: "
            f"{result['character_count']}"
            f" | Within target: "
            f"{result['within_target']}"
        )

    print(
        f"\nSaved to: {args.output}"
    )


if __name__ == "__main__":
    run()