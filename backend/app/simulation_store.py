from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from threading import RLock
from typing import Any

BASE_TIMESTAMP = datetime(2026, 1, 1, tzinfo=timezone.utc)


@dataclass
class InMemorySimulationStore:
    """Process-local, non-persistent Simulation Desk record store."""

    paper_orders: dict[str, dict[str, Any]] = field(default_factory=dict)
    audit_events: dict[str, dict[str, Any]] = field(default_factory=dict)
    portfolio_orders: dict[str, list[str]] = field(default_factory=dict)
    sequence: int = 0
    _lock: RLock = field(default_factory=RLock, repr=False)

    def reset(self) -> None:
        with self._lock:
            self.paper_orders.clear()
            self.audit_events.clear()
            self.portfolio_orders.clear()
            self.sequence = 0

    def next_sequence(self) -> int:
        with self._lock:
            self.sequence += 1
            return self.sequence

    @staticmethod
    def timestamp_for(sequence: int) -> str:
        return (BASE_TIMESTAMP + timedelta(seconds=sequence)).isoformat()

    def create_paper_order(self, record: dict[str, Any], audit_event: dict[str, Any]) -> dict[str, Any]:
        order_copy = deepcopy(record)
        audit_copy = deepcopy(audit_event)
        with self._lock:
            self.paper_orders[order_copy["paper_order_id"]] = order_copy
            self.audit_events[audit_copy["audit_event_id"]] = audit_copy
            self.portfolio_orders.setdefault(order_copy["portfolio_id"], []).append(order_copy["paper_order_id"])
            return deepcopy(order_copy)

    def get_portfolio_snapshot_records(self, portfolio_id: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]] | None:
        with self._lock:
            order_ids = self.portfolio_orders.get(portfolio_id)
            if not order_ids:
                return None

            orders = [deepcopy(self.paper_orders[order_id]) for order_id in order_ids]
            order_id_set = {order["paper_order_id"] for order in orders}
            audits = [
                deepcopy(event)
                for event in self.audit_events.values()
                if event.get("entity_id") in order_id_set
            ]
            return orders, audits


simulation_store = InMemorySimulationStore()
