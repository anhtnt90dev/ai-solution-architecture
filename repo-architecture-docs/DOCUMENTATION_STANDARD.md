# Documentation Standard

This directory contains bilingual architecture documentation for the checked-out AI repositories.

Each repository must have:

- `README.en.md`: complete English architecture document.
- `README.vi.md`: complete Vietnamese architecture document.

Each language version should include:

- Executive summary.
- Problem and AI-stack role.
- Source tree map based on actual repository files.
- Core concepts and vocabulary.
- Internal architecture.
- Runtime, request, or data flow.
- Extension points and integration surfaces.
- Configuration, deployment, and operations.
- Observability, testing, evaluation, and failure modes.
- Security, governance, and production risks.
- Senior engineer / solution architect reading guide.
- Production readiness checklist.
- Practical learning path.
- Glossary.

Each document should be detailed enough for senior developers and solution
architects. English files should be complete deep dives, and Vietnamese files
must be full Vietnamese versions rather than summaries or translated outlines.
When a statement depends on repository structure, ground it in actual
directories or files under `github-repos/`.

Each document should include at least six Mermaid diagrams:

- System or component diagram.
- End-to-end flow diagram.
- Deployment or operational topology.
- Lifecycle, decision tree, or dependency map.
- Module dependency or package boundary map.
- Production readiness, risk, or failure-mode map.

The cloned repositories under `github-repos/` are source material and should remain read-only for this documentation pass.
