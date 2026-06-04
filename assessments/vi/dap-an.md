# Đáp Án Tham Khảo

Đáp án này không ép một kiến trúc duy nhất. Nó mô tả tiêu chí của một câu trả lời mạnh.

## Đặc Điểm Của Câu Trả Lời Tốt

- Tách rõ product workflow, agent/workflow control, model runtime, retrieval data plane, LLMOps/evaluation và governance.
- Giải thích boundary bằng ownership vận hành, không chỉ bằng sở thích thư viện.
- Ra quyết định bằng bằng chứng đo được.
- Có failure mode và rollback.
- Xem tool call và retrieval là surface nhạy cảm về bảo mật.

## Điểm Cần Có

### Layering

Câu trả lời mạnh xác định ít nhất sáu lớp và không đẩy mọi trách nhiệm cho LLM. Runtime thực thi model call; retrieval layer sở hữu data contract và access control; LLMOps layer sở hữu trace, score, dataset và lineage.

### Runtime

Decision matrix tốt gồm latency, throughput, cost, data policy, model compatibility, streaming, observability, rollback và operational burden. Hosted API có thể phù hợp cho v1 nếu data policy cho phép. vLLM phù hợp hơn cho self-hosted GPU serving throughput cao. llama.cpp phù hợp hơn cho local/edge/quantized constraint.

### RAG

Data contract tốt có document ID, chunk ID, source URI, owner, ACL/tenant metadata, embedding model/version, chunk order, retention/deletion policy, query filter, top-k, reranker policy và citation format.

### Evaluation

Câu trả lời mạnh có trace cho user input, retrieval span, tool span, model span, final output, score, feedback, cost, latency, prompt version, model version và retrieval config. Promotion gate so sánh baseline với candidate và có human review cho case rủi ro cao.

### Security

Câu trả lời mạnh gồm prompt injection, indirect injection từ document, tool quá quyền, lộ secret trong trace, provider data policy, model artifact trust, tenant isolation và admin UI risk.

### Production Readiness

Checklist release tốt gồm ownership, capacity, health check, alert, rollback, incident runbook, data deletion, evaluation pass, security signoff và audit logging.
