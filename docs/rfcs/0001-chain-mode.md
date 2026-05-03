# RFC 0001: Chain Mode

- Author: @maintainers
- Status: Draft
- Created: 2026-05-04
- Target Milestone: V0.4
- Related Issues: TBD

## Summary

Chain mode lets the court send one shared dispatch through multiple provinces in a deterministic order. Each province appends a stamp-like contribution, and the court records the ordered chain as one epic event or artifact.

This RFC is a placeholder draft to reserve the first V0.4 protocol-design slot. It does not implement chain mode yet.

## Motivation

V0.3 froze the v2 single-province dispatch contract. V0.4 needs a way to express collaborative multi-province work without breaking existing province stdout/output semantics.

Chain mode should support:

- ceremonial relay events;
- multi-language transformation demos;
- future “书同文” public artifacts;
- deterministic replay in CI.

## Scope

### In scope

- A court-owned orchestration mode that calls existing provinces one by one;
- v2-compatible output from each province;
- explicit failure policy for partial chains;
- history/event representation.

### Out of scope

- Requiring provinces to implement a new protocol version;
- Networked provinces;
- Parallel graph execution;
- Browser-only execution.

## Design

Draft direction:

1. `court.chain` builds a list of province ids and an initial payload.
2. Each step calls existing `dispatcher.run_province(manifest, dispatch)`.
3. The court stores intermediate outputs in memory only.
4. The final chain record is emitted as a court event.

Open design choice: whether chain payload is carried inside `dispatch.context.chain` or as a separate court-only wrapper that never reaches province schemas.

## Compatibility

- Protocol version impact: v2-compatible if province stdin/stdout stay unchanged.
- Schema impact: ideally additive optional fields only.
- Existing province impact: none for non-chain ticks.

## Security Considerations

Chain mode multiplies subprocess invocations, so it must respect:

- per-province timeout;
- stderr/stdout limits;
- `manifest.permissions` environment behavior;
- total chain step limit;
- total chain elapsed-time limit.

## Migration Plan

No migration for existing provinces. Chain mode starts as an opt-in court command or scheduled ceremonial event.

## Testing Plan

- Unit-test deterministic province order;
- Unit-test failure policies;
- Integration-test a small chain using Python/C/SQL or mock manifests;
- Verify `python tools/validate_all.py` unchanged.

## Alternatives Considered

- New protocol v3 with chain-native input/output: more powerful but unnecessary for the first V0.4 version.
- Parallel DAG execution: deferred to V0.5+.

## Drawbacks

- More court complexity;
- More runtime cost per tick;
- Ambiguous resource semantics if chain steps mutate treasury.

## Open Questions

- Should chain steps be allowed to mutate treasury, or only produce ceremonial artifacts?
- Should partial success create an event or fail the whole chain?
- Where should chain artifacts live: `empire/artifacts/`, `empire/seals/`, or a new directory?

## Decision Log

- 2026-05-04: Draft placeholder created during V0.4 governance setup.
