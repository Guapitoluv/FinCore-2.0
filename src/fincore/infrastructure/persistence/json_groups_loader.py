from typing import Any, cast

from fincore.application.ports.group_aggregate_loader import GroupAggregateLoader
from fincore.application.ports.persistence_handler import PersistenceHandler
from fincore.infrastructure.persistence.schemas.group_schema import GroupAggregateData


class JsonGroupAggregateLoader(GroupAggregateLoader):
    def __init__(self, handler: PersistenceHandler) -> None:
        self._handler: PersistenceHandler = handler

    def load(self) -> GroupAggregateData:
        data: dict[str, Any] = self._handler.load()
        return cast(GroupAggregateData, data)