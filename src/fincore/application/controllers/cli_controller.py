from fincore.application.routing.base import CommandRouter
from fincore.application.session.session_state import SessionState
from fincore.domain.aggregates.group_aggregate import GroupAggregate
from fincore.shared.cli import is_cli_command
from fincore.shared.cli_formatting import (
    blank_line_print,
    cli_input,
    cli_print,
    fill_line_print
)


class CLIController:
    def __init__(
            self,
            session: SessionState,
            aggregate: GroupAggregate,
            router: CommandRouter
        ) -> None:
        
        self._session: SessionState = session
        self._aggregate: GroupAggregate = aggregate
        self._router: CommandRouter = router
    
    
    def run(self) -> None:
        while True:
            command: str = cli_input(">>> ").lower().strip()
            
            if not command:
                cli_print("<!> Invalid: Empty command")
                continue
            
            if not is_cli_command(command):
                cli_print(f"<!> Invalid syntax: '{command}' (missing '/')")
                continue
            
            self._router.route(command, self._session, self._aggregate)
            
            fill_line_print()
            blank_line_print()