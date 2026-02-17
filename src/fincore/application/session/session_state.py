from dataclasses import dataclass
from typing import Optional
from fincore.domain.entities.group import Group
from fincore.domain.entities.person import Person


@dataclass
class SessionState:
    _current_group: Optional[Group] = None
    
    @property
    def current_group(self) -> Optional[Group]:
        return self._current_group
    
    
    def update_current_group(self, new_group: Group) -> None:
        self._current_group = new_group