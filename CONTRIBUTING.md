# Contributing

This repository is a bilingual AI solution architecture knowledge system. Contributions should make the material more useful for engineers and architects who need to design production AI systems.

## Good Contributions

- Add a concrete architecture template.
- Improve a diagram so the boundary is clearer.
- Add a case study or failure mode from a real production scenario.
- Improve English/Vietnamese parity.
- Add a repository deep dive for a relevant AI system.
- Add assessment questions with defensible answer keys.
- Fix broken links, Mermaid syntax, or unclear wording.

## Contribution Standards

- Prefer practical artifacts over broad commentary.
- Ground technical claims in source repositories, standards, or clear operational reasoning.
- Keep English and Vietnamese versions aligned when changing course material.
- Avoid hype language. Explain trade-offs, failure modes, and production implications.
- Do not include secrets, private customer data, private architecture diagrams, or proprietary code.

## Suggested Workflow

1. Open an issue describing the improvement.
2. Keep the change scoped to one topic.
3. Update or add validation if the new content has a repeatable quality gate.
4. Run:

```powershell
powershell -ExecutionPolicy Bypass -File learn-ai-solution-architecture\validate-knowledge-system.ps1
powershell -ExecutionPolicy Bypass -File repo-architecture-docs\validate-docs.ps1
```

5. Open a pull request using the PR template.

## Style Guide

- Use clear headings and short paragraphs.
- Use Mermaid diagrams when they clarify boundaries, flows, or decisions.
- For templates, include: purpose, when to use, fields, example, and review checklist.
- For Vietnamese content, use full Vietnamese with accents.
- For architecture claims, include the operational reason.

## Bilingual Notes

English and Vietnamese pages do not need to be word-for-word translations, but they should be equivalent in learning value. If you update one language substantially, note whether the other language still needs alignment.
