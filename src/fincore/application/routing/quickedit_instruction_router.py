from fincore.application.cli.instruction_dtos import AnalyzedInstruction, OperationKind
from fincore.application.context.operation_context import OperationContext
from fincore.application.handlers.operation_handler import OperationHandler
from fincore.application.routing.base import InstructionRouter

# 88 characteres bellow (max per line)
# ----------------------------------------------------------------------------------------

class QuickEditInstructionRouter(InstructionRouter):
    def __init__(self, handlers: dict[OperationKind, OperationHandler]) -> None:
        self._handlers: dict[OperationKind, OperationHandler] = handlers
    
    
    def route(
            self,
            instruction: AnalyzedInstruction,
            context: OperationContext
        ) -> None:
        
        handler: OperationHandler | None = self._handlers.get(
            instruction.operation.kind
        )
        
        if handler is None:
            raise ValueError(f"No handler for {instruction.operation.kind}")
        
        handler.handle(instruction, context)