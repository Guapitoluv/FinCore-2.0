from typing import Self, Mapping, Sequence

from fincore.domain.base import DomainEntity, ValueObject
from fincore.domain.collections import EntityMap
from fincore.domain.mixins.mapping_navigable import MappingNavigableMixin
from fincore.domain.value_objects.money import Money
from fincore.domain.value_objects.scaled_money import ScaledMoney
from fincore.domain.value_objects.entity_id import EntityId
from fincore.domain.value_objects.vault_name import VaultName


class Vault(DomainEntity, MappingNavigableMixin):
    def __init__(
            self,
            id: EntityId,
            name: VaultName,
            vault: EntityMap[Self] | None = None,
            values: Sequence[Money | ScaledMoney]
                  | None = None 
        ) -> None:
        
        self._validate(id, name, content)
        
        self._id: EntityId = id
        self._name: VaultName = name
        self._vaults: EntityMap[Vault] = vaults or EntityMap()
        self._values: list[Money | ScaledMoney] = values or []
    
    
    def __repr__(self) -> str:
        return (
            f"Vault(id={self._id}, "
            f"name={self._name}, "
            f"vaults={self._vaults})"
            f"values={self._values}"
        )
    
    
    @classmethod
    def create_with_name(cls, name: VaultName) -> Self:
        return Vault(EntityId.new(), name)
    
    
    @property
    def _children(self) -> EntityMap[Self]:
        return self._vaults
    
    
    @property
    def id(self) -> EntityId:
        return self._id
    
    
    @property
    def name(self) -> VaultName:
        return self._name
    
    
    @property
    def vaults(self) -> Mapping[EntityId, Self]:
        return self._vaults.view()
    
    
    @property
    def values(self) -> Sequence[Money | ScaledMoney]:
        return tuple(self._values)
    
    
    def _validate(
            self,
            id: EntityId,
            name: str,
            content: list | None
        ) -> None:
        
        if not isinstance(id, EntityId):
            raise TypeError(f"Invalid type: {type(id).__name__!r}")
        
        if not isinstance(name, VaultName):
            raise TypeError(f"Invalid type: {type(name).__name__!r}")
        
        if not isinstance(vaults, EntityMap) and content is not None:
            raise TypeError(f"Invalid type: {type(content).__name__!r}")
        
        if not isinstance(values, list) and values_check and content is not None:
            raise TypeError(f"Invalid type: {type(content).__name__!r}")
    
    
    def add(self, vault_item: Money | ScaledMoney | Self) -> None:
        if isinstance(vault_item, Vault):
            self._vaults.add(vault_item)
            return
        
        self._values.append(vault_item)
    
    
    def add_value(self, value: ValueObject) -> None:
        self._values.append(value)
    
    
    def add_vault(self, vault: Self) -> None:
        self._vaults.add(vault)
    
    
    def rename(self, new_name: VaultName) -> None:
        self._name = new_name