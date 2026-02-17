from typing import Mapping, Self

from fincore.domain.base import DomainEntity
from fincore.domain.collections import EntityMap
from fincore.domain.entities.person import Person
from fincore.domain.mixins.mapping_navigable import MappingNavigableMixin
from fincore.domain.value_objects.entity_id import EntityId
from fincore.domain.value_objects.group_name import GroupName


class Group(DomainEntity, MappingNavigableMixin):
    
    def __init__(
            self,
            id: EntityId,
            name: GroupName,
            members: EntityMap[Person] | None = None
        ) -> None:
        
        self._validate(id, name, members)
        
        self._id: EntityId = id
        self._name: GroupName = name
        self._members: EntityMap[Person] = members or EntityMap()
    
    
    def __repr__(self) -> str:
        return (
            f"Group(id={self._id}, "
            f"name={self._name}, "
            f"members={self._members})"
        )
    
    
    @classmethod
    def create_with_name(cls, name: GroupName) -> Self:
        return cls(EntityId.new(), name)
    
    
    @property
    def _children(self) -> EntityMap[Person]:
        return self._members
    
    
    @property
    def members(self) -> Mapping[EntityId, Person]:
        return self._members.view()
    
    
    @property
    def id(self) -> EntityId:
        return self._id
    
    
    @property
    def name(self) -> GroupName:
        return self._name
    
    
    def _validate(
            self,
            id: EntityId,
            name: str,
            members: EntityMap[Person] | None
        ) -> None:
        
        if not isinstance(id, EntityId):
            raise TypeError(f"Invalid value: {type(id).__name__!r}")
        
        if not isinstance(name, GroupName):
            raise TypeError(f"Invalid value: {type(name).__name__!r}")
        
        if not isinstance(members, EntityMap) and members is not None:
            raise TypeError(f"Invalid value: {type(members).__name__!r}")
    
    
    def add_member(self, member: Person) -> None:
        member_id: EntityId = member.id
        
        if member_id in self._members:
            raise ValueError(f"Member already exists")
        
        self._members.add(member)
    
    
    def rename(self, new_name: GroupName) -> None:
        self._name = new_name