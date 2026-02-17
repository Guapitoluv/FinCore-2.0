from fincore.application.cli.protocols import (
    InstructionAnalyzerProtocol,
    InstructionRouterProtocol
)
from fincore.application.cli.raw_instruction import RawInstruction
from fincore.application.context.operation_context import OperationContext
from fincore.application.routing.base import InstructionRouter
from fincore.application.session.session_state import SessionState
from fincore.domain.aggregates import GroupAggregate
from fincore.shared.cli_formatting import (
    blank_line_print,
    cli_input,
    cli_print,
    fill_line_print
)
from fincore.exhibition import exhibition


def print_tag(text1: str, text2: str) -> None:
    line: str = "- " * int((26 - len(text1) - len(text2)) / 2)
    blank_line_print()
    cli_print(f"< {text1} > {line}< {text2} >")


def print_padded_number(n: int) -> None:
    cli_print(f"{'- ' * 14}< {n:03d} >")


class QuickEditController:
    def __init__(
            self,
            session: SessionState,
            aggregate: GroupAggregate,
            router: InstructionRouterProtocol,
            analyzer: InstructionAnalyzerProtocol
        ) -> None:
        
        self._session: SessionState = session
        self._aggregate: GroupAggregate = aggregate
        self._router: InstructionRouterProtocol = router
        self._analyzer: InstructionAnalyzerProtocol = analyzer
    
    
    def run(self) -> None:
        context: OperationContext = OperationContext(
            self._aggregate,
            self._session
        )
        
        n: int = 0
        print_tag("quickedit", "init")
        
        while True:
            raw: str = cli_input("< quickedit >>> ").strip()
            raw_instruction: RawInstruction = RawInstruction(raw)
            
            if raw_instruction.is_exit():
                return
            
            ast: AnalyzedInstruction = self._analyzer.analyze(raw_instruction)
            self._router.route(ast, context)
            exhibition(self._aggregate)
            
            n += 1
            print_padded_number(n)
            blank_line_print()
        
        print_tag("quickedit", "end")