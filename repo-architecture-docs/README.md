# AI Repository Architecture Documentation

This folder contains bilingual deep-dive architecture notes for 17 AI repositories checked out under `github-repos/`.

Mỗi repository có hai tài liệu Markdown:

- `README.en.md`: English deep-dive architecture document.
- `README.vi.md`: Tài liệu kiến trúc chuyên sâu bằng tiếng Việt.

The docs are written for senior developers and solution architects. They use clear language, repository-grounded source maps, and Mermaid diagrams for architecture, flows, operations, production readiness, and decision points.

## Documentation Standard

- [Documentation standard](DOCUMENTATION_STANDARD.md)
- [Validation script](validate-docs.ps1)

## Synthesized Knowledge System

- [Learn AI Solution Architecture](../learn-ai-solution-architecture/README.md): bilingual English/Vietnamese course-style knowledge system synthesized from these repository deep dives.

## Group 1: AI App / Agent Architecture

| Repository | English | Vietnamese |
| --- | --- | --- |
| openai/openai-agents-python | [README.en.md](01-ai-app-agent-architecture/openai-agents-python/README.en.md) | [README.vi.md](01-ai-app-agent-architecture/openai-agents-python/README.vi.md) |
| langchain-ai/langchain | [README.en.md](01-ai-app-agent-architecture/langchain/README.en.md) | [README.vi.md](01-ai-app-agent-architecture/langchain/README.vi.md) |
| microsoft/autogen | [README.en.md](01-ai-app-agent-architecture/autogen/README.en.md) | [README.vi.md](01-ai-app-agent-architecture/autogen/README.vi.md) |
| run-llama/llama_index | [README.en.md](01-ai-app-agent-architecture/llama_index/README.en.md) | [README.vi.md](01-ai-app-agent-architecture/llama_index/README.vi.md) |

## Group 2: Model Serving / Inference

| Repository | English | Vietnamese |
| --- | --- | --- |
| vllm-project/vllm | [README.en.md](02-model-serving-inference/vllm/README.en.md) | [README.vi.md](02-model-serving-inference/vllm/README.vi.md) |
| ggml-org/llama.cpp | [README.en.md](02-model-serving-inference/llama.cpp/README.en.md) | [README.vi.md](02-model-serving-inference/llama.cpp/README.vi.md) |
| huggingface/transformers | [README.en.md](02-model-serving-inference/transformers/README.en.md) | [README.vi.md](02-model-serving-inference/transformers/README.vi.md) |

## Group 3: Fine-tuning / Training

| Repository | English | Vietnamese |
| --- | --- | --- |
| huggingface/peft | [README.en.md](03-fine-tuning-training/peft/README.en.md) | [README.vi.md](03-fine-tuning-training/peft/README.vi.md) |
| deepspeedai/DeepSpeed | [README.en.md](03-fine-tuning-training/DeepSpeed/README.en.md) | [README.vi.md](03-fine-tuning-training/DeepSpeed/README.vi.md) |

## Group 4: RAG / Vector Database

| Repository | English | Vietnamese |
| --- | --- | --- |
| qdrant/qdrant | [README.en.md](04-rag-vector-database/qdrant/README.en.md) | [README.vi.md](04-rag-vector-database/qdrant/README.vi.md) |
| chroma-core/chroma | [README.en.md](04-rag-vector-database/chroma/README.en.md) | [README.vi.md](04-rag-vector-database/chroma/README.vi.md) |

## Group 5: Observability / Evaluation / LLMOps

| Repository | English | Vietnamese |
| --- | --- | --- |
| langfuse/langfuse | [README.en.md](05-observability-evaluation-llmops/langfuse/README.en.md) | [README.vi.md](05-observability-evaluation-llmops/langfuse/README.vi.md) |
| Arize-ai/phoenix | [README.en.md](05-observability-evaluation-llmops/phoenix/README.en.md) | [README.vi.md](05-observability-evaluation-llmops/phoenix/README.vi.md) |
| mlflow/mlflow | [README.en.md](05-observability-evaluation-llmops/mlflow/README.en.md) | [README.vi.md](05-observability-evaluation-llmops/mlflow/README.vi.md) |
| truera/trulens | [README.en.md](05-observability-evaluation-llmops/trulens/README.en.md) | [README.vi.md](05-observability-evaluation-llmops/trulens/README.vi.md) |

## Group 6: Tooling / MCP / AI Platform

| Repository | English | Vietnamese |
| --- | --- | --- |
| modelcontextprotocol/servers | [README.en.md](06-tooling-mcp-ai-platform/servers/README.en.md) | [README.vi.md](06-tooling-mcp-ai-platform/servers/README.vi.md) |
| open-webui/open-webui | [README.en.md](06-tooling-mcp-ai-platform/open-webui/README.en.md) | [README.vi.md](06-tooling-mcp-ai-platform/open-webui/README.vi.md) |

## Validation

Run from workspace root:

```powershell
powershell -ExecutionPolicy Bypass -File repo-architecture-docs\validate-docs.ps1
```

The script verifies that all expected bilingual docs exist, each has at least six Mermaid diagrams, obvious placeholder text is absent, and each document passes a stronger depth sanity check.
