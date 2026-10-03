# Automated Copywriting & Tone Transformer

A Python Generative AI project that automatically transforms a raw product description into professional marketing copy tailored to different platforms and tones.

This project was developed based on the DecodeLabs Generative AI Project 2 requirements.

## Features

- Product name, description, platform and tone inputs
- Dynamic master prompt compilation
- Temperature and Top-P controls
- Pydantic input and output validation
- Async text generation using `asyncio`
- Concurrency control using `asyncio.Semaphore`
- Exponential-backoff retries using Tenacity
- Google Gemini integration
- LinkedIn, Instagram and Email platform rules
- JSON and JSONL input support
- Bulk processing
- Local JSONL batch request generation
- CLI mode
- Interactive mode
- Character-limit validation
- Generated output saved as JSON

## Supported Platforms

The project supports three marketing platforms:

### LinkedIn

- Professional marketing copy
- Clear hook
- Useful product value
- Professional call to action
- Target length of around 1300 characters

### Instagram

- Short and engaging marketing copy
- Easy-to-read format
- Emojis are allowed
- Limited relevant hashtags are allowed
- Target length of around 500 characters

### Email

- Clear subject line
- Professional email body
- Helpful call to action
- Target length of around 1500 characters

## Project Structure

```text
automated_copywriting_tone_transformer/

├── app/
│   ├── __init__.py
│   ├── batch.py
│   ├── cli.py
│   ├── config.py
│   ├── generator.py
│   ├── models.py
│   ├── prompts.py
│   └── validators.py
│
├── examples/
│   ├── sample_request.json
│   └── bulk_requests.jsonl
│
├── output/
│   └── .gitkeep
│
├── .env.example
├── .gitignore
├── ARCHITECTURE.md
├── main.py
├── requirements.txt
└── README.md