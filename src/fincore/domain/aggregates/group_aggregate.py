from typing import (
    Self,
    Sequence,
    Mapping,
    Any
)

from fincore.domain.base import DomainAggregate, DomainEntity
from fincore.domain.collections import EntityMap
from fincore.domain.entities.group import Group
from fincore.domain.mixins.mapping_navigable import MappingNavigableMixin
from fincore.domain.value_objects.group_name import GroupName


class GroupAggregate(DomainAggregate, MappingNavigableMixin):
    def __init__(self, groups: EntityMap[Group]) -> None:
        self._groups: EntityMap[Group] = groups
    
    
    def __repr__(self) -> str:
        return f"GroupAggregate(groups={self._groups})"
    
    
    @property
    def _children(self) -> EntityMap[Group]:
        return self._groups
    
    
    @property
    def groups(self) -> Mapping[str, Group]:
        return self._groups.view()
    
    
    def values(self) -> tuple[Group, ...]:
        return self._groups.values()
    
    
    def get_by_name(
            self,
            name: str,
            only_one: bool = False,
            default: Any | None = None
        ) -> Group:
        
        return self._groups.get_by_name(name, only_one, default)
    
    
    def add_child(self, child) -> None:
        self.add_group(child)
    
    
    def add_group(self, group: Group) -> None:
        self._groups[group.id] = group
    
    
    def resolve(
            self,
            segments: Sequence[str],
            current: DomainEntity | None = None
        ) -> Self | DomainEntity:
        
        current: GroupAggregate | DomainEntity = current or self 
        
        for segment in segments:
            if not isinstance(current, MappingNavigableMixin):
                raise KeyError("...")
            
            if segment not in current.names:
                raise KeyError(f"'{segment} not found")
            
            current = current.get(segment)
        
        return current
    
    
    def resolve_with_parent(
            self,
            segments: Sequence[str],
            current: DomainEntity | None = None
        ) -> tuple[Self | DomainEntity, DomainEntity]:
        
        parent: GroupAggregate | DomainEntity | None = None
        current: GroupAggregate | DomainEntity = current or self
        
        for segment in segments:
            if not isinstance(current, MappingNavigableMixin):
                raise KeyError("...")
            
            if segment not in current.names:
                raise KeyError(f"'{segment} not found")
            
            parent = current
            current = current.get(segment)
        
        return parent, current
    
    
    def rename_child(self, child_name: str, new_name: str) -> None:
        if child_name not in self._groups.names:
            raise KeyError(f"'{child_name}' does not exist")
        
        child: Group = self._groups.get_by_name(child_name)
        child = self._groups.pop(child.id)
        child.rename(GroupName(new_name))
        self._groups[child.id] = child