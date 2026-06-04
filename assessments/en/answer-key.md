# Answer Key

This answer key is not a single correct architecture. It defines what strong answers should include.

## Strong Answer Characteristics

- Separates product workflow, agent/workflow control, model runtime, retrieval data plane, LLMOps/evaluation, and governance.
- Explains boundaries using operational ownership, not library preference.
- Makes decisions with measurable evidence.
- Includes failure modes and rollback.
- Treats tool calls and retrieval as security-sensitive surfaces.

## Expected Points

### Layering

Strong answers identify at least six layers and avoid assigning all responsibility to the LLM. The runtime executes model calls; the retrieval layer owns data contracts and access control; the LLMOps layer owns traces, scores, datasets, and lineage.

### Runtime

Strong decision matrices include latency, throughput, cost, data policy, model compatibility, streaming, observability, rollback, and operational burden. Hosted API may be acceptable for v1 if security/data policy allows it. vLLM is stronger for high-throughput self-hosted GPU serving. llama.cpp is stronger for local/edge/quantized constraints.

### RAG

Strong data contracts include document ID, chunk ID, source URI, owner, ACL/tenant metadata, embedding model/version, chunk order, retention/deletion policy, query filters, top-k, reranker policy, and citation format.

### Evaluation

Strong answers include traces for user input, retrieval spans, tool spans, model spans, final output, scores, feedback, cost, latency, prompt version, model version, and retrieval config. Promotion gates compare baseline vs candidate and include human review for high-risk cases.

### Security

Strong answers include prompt injection, indirect injection from documents, over-permissioned tools, secret exposure in traces, provider data policy, model artifact trust, tenant isolation, and admin UI risk.

### Production Readiness

Strong release checklists include ownership, capacity, health checks, alerts, rollback, incident runbook, data deletion, evaluation pass, security signoff, and audit logging.
