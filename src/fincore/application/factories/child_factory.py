from typing import Callable

from fincore.application.factories.resolvers.base import ChildResolver
from fincore.domain.base import DomainEntity, ValueObject
from fincore.domain.entities.group import Group
from fincore.domain.entities.person import Person
from fincore.domain.entities.vault import Vault


class ChildFactory:
    def __init__(
            self,
            registry: dict[type, Callable[[str], ValueObject | Vault]],
            resolvers: list[ChildResolver]
        ) -> None:
        
        self._registry: dict[type, type] = registry
        self._resolvers: list[ChildResolver] = resolvers
    
    
    def create_for(self, parent: object, literal: str) -> DomainEntity | ValueObject:
        for resolver in self._resolvers:
            if resolver.supports(parent):
                return parent.create_with_name(literal)
        
        creator: Callable[[str], Group | Person]
        
        for type_parent, creator in self._registry.items():
            if isinstance(parent, type_parent):
                return creator(literal)
        
        raise TypeError("Unsupported parent type")