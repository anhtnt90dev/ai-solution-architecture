# Architecture Review Exam

Timebox: 90 minutes

Scenario: You are designing an Enterprise Knowledge Copilot for architecture review. It must answer with citations from internal standards, support approved tool calls, trace every interaction, and provide a production readiness summary.

## Section 1: Layering

1. Draw the six major layers of the system and state the responsibility of each layer.
2. Explain why the model runtime should not own retrieval policy.
3. Explain why the agent/workflow layer should not own long-term experiment lineage.

## Section 2: Runtime Decision

You have three candidate serving options: hosted API, vLLM, and llama.cpp.

4. Create a decision matrix with at least six criteria.
5. Pick one runtime for the first production release and justify the choice.
6. Define the metrics that would force a runtime change.

## Section 3: RAG Data Contract

7. Define the required document, chunk, metadata, and query fields.
8. Explain how access control should be enforced.
9. Define a retrieval evaluation plan.

## Section 4: LLMOps And Evaluation

10. Define the trace schema.
11. Define a promotion gate for prompt, retrieval, and model changes.
12. Explain how MLflow-style lineage differs from LLM trace observability.

## Section 5: Security And Governance

13. Identify five security risks specific to this copilot.
14. Define the tool governance policy.
15. Define what must be logged for auditability.

## Section 6: Production Readiness

16. Create a release checklist.
17. Define rollback behavior.
18. Define three failure rehearsal scenarios.

## Scoring Rubric

| Area | Points |
| --- | --- |
| Layering and boundaries | 15 |
| Runtime decision quality | 15 |
| RAG data contract | 15 |
| Evaluation and LLMOps | 20 |
| Security and governance | 20 |
| Production readiness | 15 |
