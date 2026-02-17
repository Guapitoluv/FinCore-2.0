from typing import Mapping, Self

from fincore.domain.base import DomainEntity
from fincore.domain.collections import EntityMap
from fincore.domain.entities.vault import Vault
from fincore.domain.errors import VaultAlreadyExists
from fincore.domain.mixins.mapping_navigable import MappingNavigableMixin
from fincore.domain.value_objects.entity_id import EntityId
from fincore.domain.value_objects.person_name import PersonName


class Person(DomainEntity, MappingNavigableMixin):
    def __init__(
            self,
            id: EntityId,
            name: PersonName,
            vaults: EntityMap[Vault] | None = None
        ) -> None:
        
        self._validate(id, name, vaults)
        
        self._id: EntityId = id
        self._name: PersonName = name
        self._vaults: EntityMap[Vault] = vaults or EntityMap()
    
    
    def __repr__(self) -> str:
        return (
            f"Person(id={self._id}, "
            f"name={self._name}, "
            f"vaults={self._vaults})"
        )
    
    
    @classmethod
    def create_with_name(cls, name: PersonName) -> Self:
        return cls(EntityId.new(), name)
    
    
    @property
    def _children(self) -> EntityMap[Vault]:
        return self._vaults
    
    
    @property
    def id(self) -> EntityId:
        return self._id
    
    
    @property
    def name(self) -> PersonName:
        return self._name
    
    
    @property
    def vaults(self) -> Mapping[EntityId, Vault]:
        return self._vaults.view()
    
    
    def _validate(
            self,
            id: EntityId,
            name: PersonName,
            vaults: EntityMap[Vault] | None
        ) -> None:
        
        if not isinstance(id, EntityId):
            raise TypeError(f"Invalid value: {type(id).__name__!r}")
        
        if not isinstance(name, PersonName):
            raise TypeError(f"Invalid value: {type(name).__name__!r}")
        
        if not isinstance(vaults, EntityMap) and vaults is not None:
            raise TypeError(f"Invalid value: {type(vaults).__name__!r}")
    
    
    def add_vault(self, vault: Vault) -> None:
        if vault.name in self._vaults.names():
            raise VaultAlreadyExists(self._name, vault.name)
        
        self._vaults.add(vault)
    
    
    def rename(self, new_name: PersonName) -> None:
        self._name = new_name