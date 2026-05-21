# 05 Data and Storage Plan (Initial)

## Data Domains

1. **Reference Data**: tickers, sectors, metadata.
2. **Research Artifacts**: theses, memos, assumptions.
3. **Strategy Records**: recommendation packets and revisions.
4. **Simulation Records**: paper trades, PnL snapshots, review notes.
5. **Governance Logs**: decisions, progress, lessons learned.

## Storage Principles

- Keep raw inputs and generated outputs distinguishable.
- Preserve timestamps and authorship/agent attribution.
- Favor append-only event logs for auditable workflows.

## Access & Safety Considerations

- Role-based access controls for sensitive notes.
- Clear labels for simulated vs real-world records.
- Backup and retention policy to be defined in implementation phase.

## Next Step

Detailed schema design is tracked in:
- `codex-tasks/002-design-supabase-schema.md`
