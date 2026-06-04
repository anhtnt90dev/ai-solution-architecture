# Bài Kiểm Tra Kiến Trúc

Thời lượng: 90 phút

Bối cảnh: Bạn đang thiết kế một Enterprise Knowledge Copilot hỗ trợ review kiến trúc. Hệ thống phải trả lời có citation từ tài liệu nội bộ, hỗ trợ tool call đã được phê duyệt, trace toàn bộ interaction và tạo production readiness summary.

## Phần 1: Layering

1. Vẽ sáu lớp chính của hệ thống và nêu trách nhiệm của từng lớp.
2. Giải thích vì sao model runtime không nên sở hữu retrieval policy.
3. Giải thích vì sao agent/workflow layer không nên sở hữu long-term experiment lineage.

## Phần 2: Quyết Định Runtime

Bạn có ba lựa chọn serving: hosted API, vLLM và llama.cpp.

4. Tạo decision matrix với ít nhất sáu tiêu chí.
5. Chọn một runtime cho bản production đầu tiên và giải thích.
6. Định nghĩa metric nào sẽ buộc team đổi runtime.

## Phần 3: RAG Data Contract

7. Định nghĩa các field bắt buộc cho document, chunk, metadata và query.
8. Giải thích access control nên được enforce ở đâu.
9. Định nghĩa retrieval evaluation plan.

## Phần 4: LLMOps Và Evaluation

10. Định nghĩa trace schema.
11. Định nghĩa promotion gate cho prompt, retrieval và model change.
12. Giải thích lineage kiểu MLflow khác gì observability trace của LLM.

## Phần 5: Security Và Governance

13. Chỉ ra năm rủi ro bảo mật riêng của copilot này.
14. Định nghĩa tool governance policy.
15. Định nghĩa những gì phải log để audit được.

## Phần 6: Production Readiness

16. Tạo release checklist.
17. Định nghĩa rollback behavior.
18. Định nghĩa ba kịch bản failure rehearsal.

## Rubric

| Khu vực | Điểm |
| --- | --- |
| Layering và boundary | 15 |
| Chất lượng quyết định runtime | 15 |
| RAG data contract | 15 |
| Evaluation và LLMOps | 20 |
| Security và governance | 20 |
| Production readiness | 15 |
