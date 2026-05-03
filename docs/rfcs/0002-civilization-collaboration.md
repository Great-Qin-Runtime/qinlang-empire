# RFC 0002: Civilization Collaboration Intake

- Author: @maintainers
- Status: Draft
- Created: 2026-05-04
- Target Milestone: V0.4
- Related Issues: #48

## Summary

Define how QinLang Empire can integrate external projects or “civilizations” without breaking protocol v2, CI determinism, or the security model.

This RFC is a draft intake wrapper for #48 and similar proposals.

## Motivation

External projects can enrich QinLang’s narrative and economy. But direct integration can introduce unclear licenses, network dependencies, secrets, non-deterministic CI, or protocol churn.

We need a safe path: document → static fixture → optional dashboard → optional RFC-backed runtime integration.

## Scope

### In scope

- External project metadata;
- License and attribution checks;
- Static offline data fixtures;
- Optional dashboard rendering;
- RFC triggers for deeper integration.

### Out of scope

- Mandatory network calls in CI;
- Secrets/API keys in repository;
- Breaking v2 schema changes;
- Running external daemons.

## Design

A civilization collaboration proposal must include:

1. External links and license;
2. Concept mapping to QinLang resources/events/provinces;
3. Offline fixture plan;
4. Security boundary;
5. Testing and rollback plan.

The default implementation path:

```text
issue -> RFC draft -> static JSON fixture -> dashboard optional view -> runtime integration only if later accepted
```

## Compatibility

- Protocol version impact: none by default.
- Schema impact: none unless a later RFC proposes additive optional fields.
- Existing province impact: none.

## Security Considerations

- Network must be opt-in and permission-gated;
- CI must not depend on third-party uptime;
- External data should be treated as untrusted input;
- License must be compatible before importing code/assets.

## Migration Plan

No migration. Existing issues such as #48 can be retitled or linked to this RFC and refined with the collaboration template.

## Testing Plan

- Validate fixture JSON if introduced;
- Dashboard renders without network;
- `python tools/validate_all.py` remains green.

## Alternatives Considered

- Directly vendor external project code: rejected until license/security review.
- Dashboard fetches external API live: rejected for baseline because it breaks offline availability.

## Drawbacks

- Slower path for creative integrations;
- More upfront documentation.

## Open Questions

- Should external civilizations become “foreign states” in state.json, or remain dashboard-only?
- Should market prices affect QinLang treasury, or be visual only?

## Decision Log

- 2026-05-04: Draft created to give #48 a safe intake route.
