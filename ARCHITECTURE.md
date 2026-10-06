# Architecture

```text
CLI / JSONL
    |
    v
Pydantic validation
    |
    v
Dynamic master prompt
    |
    +------------------------+
    |                        |
    v                        v
Real-time async         OpenAI Batch API
pipeline                for delayed bulk jobs
    |
    v
Semaphore -> Model -> Retry
    |
    v
Output validation -> JSON
```

The code is separated into configuration, schemas, prompt compilation,
generation, validation, batch processing and CLI orchestration.
