# 05 Data and Storage Plan (Canonical v1)

## Canonical Primary Tables (Required Names)

1. `reference_securities`
2. `research_artifacts`
3. `strategy_records`
4. `simulation_records`
5. `governance_logs`

## Storage Principles

- Keep raw inputs and generated outputs distinguishable.
- Preserve timestamps and authorship/agent attribution.
- Favor append-only event logs for auditable workflows.

## Access & Safety Considerations

- Role-based access controls for sensitive notes.
- Clear labels for simulated vs real-world records.
- Backup and retention policy to be defined in implementation phase.

## Contract Alignment

- API contracts must use the exact MVP endpoint set in `docs/09-api-and-agent-contracts.md`.
- All endpoint responses must use the required response envelope in `docs/09-api-and-agent-contracts.md`.
