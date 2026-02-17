from dataclasses import dataclass

from fincore.domain.aggregates.group_aggregate import GroupAggregate
from fincore.application.session.session_state import SessionState


@dataclass(slots=True)
class OperationContext:
    aggregate: GroupAggregate
    session: SessionState