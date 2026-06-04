# Security Policy

This repository is documentation and educational material, not a deployed AI service. Security issues are still relevant because the repository discusses tools, agents, retrieval, model artifacts, and production governance.

## Please Report

- Secrets accidentally committed to the repository.
- Links that point to malicious or compromised content.
- Guidance that would create unsafe tool execution, data exfiltration, or credential exposure if followed.
- Incorrect security advice in templates, checklists, or deep dives.
- XSS or unsafe browser behavior in the GitHub Pages landing page.

## Do Not Report As Security Issues

- General architecture disagreements.
- Missing lessons or template requests.
- Library preference debates.

Use normal GitHub Issues for those.

## Disclosure

If you find a security issue, open a GitHub issue with a minimal description and avoid posting secrets or exploit payloads. If the issue contains sensitive material, contact the repository owner directly through GitHub before sharing details.

## Production Reminder

Any AI system built from these materials should still perform its own threat model, secrets review, dependency review, data retention review, and tool execution governance review.

## Security Review Scope

Security feedback is especially valuable when it improves the architecture templates or corrects guidance that could be copied into a real system. Examples include missing tenant isolation in a retrieval design, unsafe tool permission advice, weak prompt-injection handling, unclear audit logging, insufficient model artifact provenance, or guidance that might place secrets in prompts, traces, or vector metadata.

When reporting, include the affected file, the specific section, the risk, and the safer recommendation. If the issue is conceptual, describe the scenario where the guidance fails. For example, "retrieval filters are applied after vector search, so a cross-tenant chunk could influence ranking" is more actionable than "RAG security is incomplete."

## Handling Sensitive Material

Do not paste real secrets, private customer data, proprietary diagrams, internal endpoints, or exploit payloads into public issues. Replace sensitive values with minimal redacted examples. If the report requires private context, contact the repository owner first and share only the amount needed to reproduce the concern. The goal is to improve public guidance without creating a new exposure.

## Maintainer Response

Security-related issues should be triaged by impact. Critical issues include exposed credentials, malicious links, unsafe browser behavior on the Pages site, or advice that could directly enable data exfiltration or unauthorized tool execution. Lower-severity issues include ambiguous wording, missing caveats, or incomplete checklist coverage. Accepted fixes should update the relevant document and, when appropriate, add a validation or checklist item so the issue does not return.
