from fincore.application.context.operation_context import OperationContext
from fincore.application.factories.child_factory import ChildFactory
from fincore.application.handlers.operation_handler import OperationHandler
from fincore.domain.entities.group import Group
from fincore.domain.value_objects.group_name import GroupName


class GroupCreateHandler(OperationHandler):
    def handle(
            self,
            instruction: AnalyzedInstruction,
            context: OperationContext
        ) -> None:
        
        literal: str = instruction.operation.operands[0]
        name: GroupName = GroupName(literal)
        group: Group = Group.create_with_name(name)
        context.aggregate.add_group(group)