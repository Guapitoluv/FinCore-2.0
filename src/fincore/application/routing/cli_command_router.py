from fincore.application.controllers.base import CLIControllerABC
from fincore.application.routing.base import CommandRouter
from fincore.application.session.session_state import SessionState
from fincore.domain.aggregates.group_aggregate import GroupAggregate
from fincore.shared.cli_formatting import cli_print

# 88 characteres bellow (max per line)
# ----------------------------------------------------------------------------------------

class CLICommandRouter(CommandRouter):
    def __init__(
            self,
            quickedit_controller,
            group_selection_controller
        ) -> None:
        
        self._quickedit_controller = quickedit_controller
        self._group_selection_controller = group_selection_controller
    
    
    def route(
            self,
            command: str,
            session: SessionState,
            aggregate: GroupAggregate,
        ) -> None:
        
        if command in ["/quickedit", "/qe"]:
            self._quickedit_controller.run()
            return
        
        if command == "/current_group":
            cli_print(f"Current group: {session.current_group.name.value}")
            return
        
        if command == "/change_group":
            self._group_selection_controller.run(aggregate)
            return
        
        if command == "/exit":
            cli_print("Exiting")
            exit()
        
        cli_print(f"<!> Invalid command: '{command}'")