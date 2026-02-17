from typing import Any

from fincore.application.dto.group_dto import GroupAggregateDTO
from fincore.application.mappers.group_aggregate_mapper import parse_group_aggregate
from fincore.application.ports.group_aggregate_loader import GroupAggregateLoader
from fincore.domain.aggregates import GroupAggregate
from fincore.application.factories.group_aggregate_factory import GroupAggregateFactory
from fincore.infrastructure.persistence.schemas.group_schema import GroupAggregateData


class LoadGroupsUseCase:
    def __init__(self, loader: GroupAggregateLoader) -> None:
        self._loader: GroupAggregateLoader = loader

    def execute(self) -> GroupAggregate:
        raw_data: GroupAggregateData = self._loader.load()
        group_aggregate_dto: GroupAggregateDTO = parse_group_aggregate(raw_data)
        group_aggregate: GroupAggregate = GroupAggregateFactory.create(group_aggregate_dto)
        return group_aggregate