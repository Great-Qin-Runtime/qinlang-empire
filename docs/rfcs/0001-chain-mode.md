# RFC 0001: Chain Mode

- Author: @maintainers
- Status: Accepted
- Created: 2026-05-04
- Accepted: 2026-05-04
- Target Milestone: V0.4
- Related Issues: #51, #52

## Summary

Chain mode is a **court-owned orchestration mode** that sends a shared ceremonial payload through an ordered list of provinces and writes one deterministic artifact at the end.

The first implementation is intentionally conservative:

- It does **not** change `protocol_version = 2`;
- It does **not** require any province to implement a new stdin/stdout shape;
- It does **not** merge per-step `deltas` into `empire/state.json`;
- It records chain output as an artifact plus one court event.

In other words, chain mode is a replayable “multi-province ceremony” built on top of the existing v2 dispatch contract.

## Motivation

V0.3 froze the v2 single-province dispatch contract. V0.4 needs a visible collaboration primitive without reopening the protocol.

Chain mode supports:

- multi-language relay demos;
- ceremonial “书同文” artifacts;
- deterministic CI replay;
- future dashboard timeline/gallery views;
- a safe stepping stone toward richer graph modes in V0.5+.

## Scope

### In scope

- A deterministic court module (`court/chain.py`);
- Ordered province selection by explicit ids;
- Per-step dispatch through existing `dispatcher.run_province(manifest, dispatch)`;
- Artifact writing under `empire/chains/`;
- One court event with `type=chain` and `artifact=<relative path>`;
- Unit tests for order, failure policy, and artifact generation.

### Out of scope

- New `protocol_version`;
- New required schema fields;
- Parallel graph execution;
- Browser-only execution;
- Networked or remote provinces;
- Merging chain step resource deltas into treasury.

## Design

### 1. Public API

The MVP exposes a pure Python API:

```python
from court import chain

record = chain.run_chain(
    state=state,
    manifests=manifests,
    province_ids=["python", "c", "sql"],
    title="书同文小典",
    payload={"text": "秦法同文"},
    empire_dir=Path("empire"),
)
```

`run_chain` returns a record object:

```json
{
  "chain_id": "chain-000123-python-c-sql",
  "tick": 123,
  "title": "书同文小典",
  "province_ids": ["python", "c", "sql"],
  "status": "passed",
  "steps": [
    {
      "index": 0,
      "province_id": "python",
      "status": "passed",
      "ok": true,
      "event_count": 1,
      "error": null
    }
  ],
  "artifact": "chains/chain-000123-python-c-sql.json"
}
```

### 2. Dispatch shape

Each province still receives valid v2 input:

```json
{
  "protocol_version": 2,
  "dispatch": {
    "schema_version": 1,
    "dispatch_id": "chain-000123-00-python",
    "tick": 123,
    "dispatch_type": "ceremony",
    "context": {
      "chain": {
        "chain_id": "chain-000123-python-c-sql",
        "title": "书同文小典",
        "step_index": 0,
        "step_count": 3,
        "previous": []
      }
    }
  }
}
```

`dispatch.context.chain` is an **optional additive context object**. Existing provinces may ignore it. Because `context` already exists and unknown keys are tolerated, this remains v2-compatible.

### 3. Step semantics

For every province id:

1. Find manifest by id;
2. Skip missing/quarantined province as a failed step;
3. Build a normal dispatch with `ticker.build_dispatch`;
4. Override:
   - `dispatch_id` to `chain-<tick>-<index>-<province>`;
   - `dispatch_type` to `ceremony`;
   - `context.chain` to current chain metadata;
   - `expects.max_event_count` to `2`;
5. Run `dispatcher.run_province`;
6. Store a summarized step result;
7. Append successful province events into the chain artifact only.

### 4. Failure policy

The MVP uses **fail-soft** policy:

- Continue after failed steps;
- Mark final `status` as `partial` if at least one step passed and one failed;
- Mark final `status` as `failed` if all steps failed;
- Mark final `status` as `passed` if all steps passed.

The court does **not** call `state.merge_delta` for chain steps. Therefore chain mode does not affect treasury, province loyalty, fail streak, cooldown, or quarantine. This avoids surprising side effects and keeps chain deterministic.

### 5. Artifact path

Artifacts are written under:

```text
empire/chains/<chain_id>.json
```

The JSON artifact contains:

- chain metadata;
- original payload;
- step summaries;
- province event texts;
- elapsed time;
- final status.

`empire/chains/*.json` is a runtime artifact and should be ignored by git.

### 6. Court event

After the chain completes, `run_chain` inserts one event at the head of `state.events`:

```json
{
  "type": "chain",
  "from_province": null,
  "text": "书同文小典：3 郡接力，status=passed",
  "severity": "epic",
  "artifact": "chains/chain-000123-python-c-sql.json"
}
```

If artifact writing fails, the chain still returns a record with `artifact=null` and emits a warning-severity event.

## Compatibility

- Protocol version impact: **none** (`protocol_version` remains `2`);
- Schema impact: additive optional `dispatch.context.chain`;
- Existing province impact: none;
- Existing tick behavior: unchanged unless chain mode is explicitly called.

This is compatible with the V0.3 freeze declaration because it adds optional context and court-only artifacts; it does not remove, rename, or retype any frozen field.

## Security Considerations

Chain mode multiplies subprocess invocations, so it must respect:

- each province’s existing `timeout_ms`;
- stderr truncation and stdout strict JSON checks;
- `manifest.permissions` env behavior;
- maximum step count, default 8;
- maximum total elapsed time, default 30 seconds;
- no network beyond per-manifest permissions.

The MVP should not introduce new runner types or shell interpolation.

## Migration Plan

No migration is required.

Existing provinces do not need to change. Provinces that want richer chain-specific behavior may optionally inspect `dispatch.context.chain` later.

## Testing Plan

- Unit-test deterministic `chain_id`;
- Unit-test missing province failure;
- Unit-test fail-soft status calculation;
- Unit-test artifact writing;
- Unit-test court event insertion;
- Integration-test a small mock chain without mutating treasury;
- Verify `python -m pytest tests/` and `python tools/validate_all.py`.

## Alternatives Considered

### New protocol v3

Rejected for V0.4 MVP. It would be more expressive, but V0.3 intentionally froze v2. Chain mode can be implemented as additive optional context.

### Merge every step delta

Rejected for MVP. It creates ambiguity around partial failure and resource conservation. Chain artifacts should be ceremonial/read-only first.

### Parallel DAG execution

Deferred to V0.5+. It requires a separate scheduler and artifact model.

## Drawbacks

- More subprocess work when chain mode is invoked;
- Chain-specific behavior is optional, so many provinces will initially return generic events;
- Artifact-only semantics may feel less “gameplay-rich” than treasury mutation.

## Open Questions

- Should V0.5 add dashboard chain artifact rendering?
- Should V0.5 allow chain recipes declared in manifest or state?
- Should successful chain participation grant a small loyalty/title bonus?

## Decision Log

- 2026-05-04: Draft placeholder created during V0.4 governance setup.
- 2026-05-04: Accepted MVP direction: court-owned, v2-compatible, fail-soft, artifact-only.
