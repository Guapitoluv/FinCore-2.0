from fincore.application.dto.group_dto import GroupDTO
from fincore.application.factories.person_factory import PersonFactory
from fincore.domain.entities.group import Group
from fincore.domain.entities.person import Person
from fincore.domain.value_objects.entity_id import EntityId
from fincore.domain.value_objects.group_name import GroupName
from fincore.application.parsers.entity_id_parser import parse_entity_id

class GroupFactory:
    @staticmethod
    def create(dto: GroupDTO) -> Group:
        group: Group = Group(
            id=parse_entity_id(dto.id),
            name=GroupName(dto.name)
        )
        
        for person_dto in dto.members.values():
            person: Person = PersonFactory.create(person_dto)
            group.add_member(person)
        
        return group
    
    
    @staticmethod
    def create_with_name(name: str) -> Group:
        return Group.create_with_name(name)