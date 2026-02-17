from fincore.application.session.session_state import SessionState
from fincore.domain.aggregates.group_aggregate import GroupAggregate
from fincore.domain.entities.group import Group
from fincore.shared.cli_formatting import (
    blank_line_print,
    cli_input,
    cli_print,
    fill_line_print
)


class GroupSelectionController:
    
    def __init__(self, session: SessionState) -> None:
        self._session: SessionState = session
    
    
    def run(self, aggregate: GroupAggregate) -> None:
        groups: tuple[Group, ...] = aggregate.values()
        
        if not groups:
            cli_print("Groups is empty.")
            return
        
        while True:
            blank_line_print()
            self._print_groups(groups)
            
            cli_print("Select group by index or name:")
            raw: str = cli_input(">>> ")
            
            if raw == "/cancel":
                cli_print("Group selection canceled.")
                return
            
            if raw in aggregate.names:
                if self._confirm(aggregate.get_by_name(raw)):
                    return
            
            if not raw.isnumeric():
                continue
            
            index: int = int(raw)
            group: Group = self._get_by_index(groups, index)
            
            if group is None:
                continue
            
            if self._confirm(group):
                return
    
    
    def _print_groups(self, groups: tuple[Group, ...]) -> None:
        cli_print("> - - - - - < Groups >")
        
        for n, group in enumerate(groups, 1):
            cli_print(
                f"{n}. {group.name.value}",
                end=("." if len(groups) == n else ";") + "\n"
            )
        
        fill_line_print()
    
    
    def _get_by_index(self, groups: tuple[Group, ...], index: int) -> None:
        if not 1 <= index <= len(groups):
            cli_print("Out of range.")
            return
        
        return groups[index - 1]
    
    
    def _confirm(self, group: Group) -> bool:
        while True:
            confirmation: str = cli_input("confirm[y/n]: ")
            
            if confirmation == "y":
                self._session.update_current_group(group)
                cli_print(f"Selected group: {group.name.value}")
                return True
            
            if confirmation == "n":
                return False
            
            cli_print(f"Invalid value: {confirmation}")
            blank_line_print()