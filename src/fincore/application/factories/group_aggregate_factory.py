from typing import Any

from fincore.application.dto.group_dto import GroupAggregateDTO
from fincore.domain.aggregates import GroupAggregate
from fincore.domain.collections import EntityMap
from fincore.domain.entities.group import Group
from fincore.application.factories.group_factory import GroupFactory
from fincore.application.parsers.entity_id_parser import parse_entity_id

class GroupAggregateFactory:
    @staticmethod
    def create(dto: GroupAggregateDTO) -> GroupAggregate:
        aggregate: GroupAggregate = GroupAggregate()
        
        for group_dto in dto.groups.values():
            group: Group = GroupFactory.create(group_dto)
            aggregate.add_group(group)
        
        return aggregate