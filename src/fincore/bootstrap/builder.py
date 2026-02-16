from fincore.application.cli.instruction_analyzer import InstructionAnalyzer
from fincore.application.cli.instruction_dtos import OperationKind
from fincore.application.context.operation_context import OperationContext
from fincore.application.controllers import CLIController
from fincore.application.controllers import QuickEditController
from fincore.application.controllers import GroupSelectionController
from fincore.application.factories.child_factory import ChildFactory
from fincore.application.factories.person_factory import PersonFactory
from fincore.application.factories.resolvers.vault_child_resolver import VaultChildResolver
from fincore.application.factories.vault_factory import VaultFactory
from fincore.application.handlers.group_create_handler import GroupCreateHandler
from fincore.application.handlers.assign_handler import AssignHandler
from fincore.application.handlers.rekey_handler import RekeyHandler
from fincore.application.parsers.base import VaultValueParser
from fincore.application.parsers.money_parser import parse_money_from_literal
from fincore.application.parsers.scaled_money_parser import parse_scaled_money_from_literal
from fincore.application.parsers.vault_value_parser import DefaultVaultValueParser
from fincore.application.ports.persistence_handler import PersistenceHandler
from fincore.application.routing.base import InstructionRouter, CommandRouter
from fincore.application.routing.cli_command_router import CLICommandRouter
from fincore.application.routing.quickedit_instruction_router import QuickEditInstructionRouter
from fincore.application.session.session_state import SessionState
from fincore.application.use_cases import LoadGroupsUseCase
from fincore.domain.aggregates.group_aggregate import GroupAggregate
from fincore.domain.entities.group import Group
from fincore.domain.entities.person import Person
from fincore.domain.entities.vault import Vault
from fincore.infrastructure.persistence.json_groups_loader import JsonGroupAggregateLoader
from fincore.infrastructure.persistence import JsonHandler
from fincore.paths import MAINJSON


class ApplicationBuilder:

    def _build_handler(self) -> PersistenceHandler:
        return JsonHandler(MAINJSON)
    
    
    def _build_loader(self, handler: PersistenceHandler) -> JsonGroupAggregateLoader:
        return JsonGroupAggregateLoader(handler)
    
    
    def _build_use_case(self, loader: JsonGroupAggregateLoader) -> LoadGroupsUseCase:
        return LoadGroupsUseCase(loader)
    
    
    def _build_aggregate(self, use_case: LoadGroupsUseCase) -> GroupAggregate:
        return use_case.execute()
    
    
    def _build_parser(self) -> VaultValueParser:
        return DefaultVaultValueParser(
            strategies=[
                parse_money_from_literal,
                parse_scaled_money_from_literal,
            ]
        )
    
    
    def _build_factory(self, parser: VaultValueParser) -> ChildFactory:
        return ChildFactory(
            registry={
                Group: Person,
                Person: Vault
            },
            resolvers=[
                VaultChildResolver(parser)
            ]
        )
    
    
    def _build_instruction_router(self, factory: ChildFactory) -> InstructionRouter:
        return QuickEditInstructionRouter(
            handlers={
                OperationKind.GROUP_CREATE: GroupCreateHandler(),
                OperationKind.ASSIGN: AssignHandler(factory),
                OperationKind.REKEY: RekeyHandler()
            }
        )
    
    
    def _build_quickedit_controller(
            self,
            session: SessionState,
            aggregate: GroupAggregate,
            quickedit_router: InstructionRouter
        ) -> QuickEditController:
        
        return QuickEditController(
            session=session,
            aggregate=aggregate,
            router=quickedit_router,
            analyzer=InstructionAnalyzer()
        )
    
    
    def _build_group_selection_controller(
            self,
            session: SessionState
        ) -> GroupSelectionController:
        
        return GroupSelectionController(session)
    
    
    def _build_router(
            self,
            quickedit_controller: QuickEditController,
            group_selection_controller: GroupSelectionController
        ) -> CommandRouter:
        
        return CLICommandRouter(
            quickedit_controller,
            group_selection_controller
        )
    
    
    def _build_context(
            self,
            aggregate: GroupAggregate,
            session: SessionState
        ) -> OperationContext:
        
        return OperationContext(
            aggregate,
            session
        )
    
    
    def _build_controller(
            self,
            session: SessionState,
            aggregate: GroupAggregate,
            router: CommandRouter
        ) -> CLIController:
        
        return CLIController(session, aggregate, router)
    
    
    def build(self) -> CLIController:
        handler = self._build_handler()
        loader = self._build_loader(handler)
        use_case = self._build_use_case(loader)
        aggregate = self._build_aggregate(use_case)
        parser = self._build_parser()
        factory = self._build_factory(parser)
        quickedit_router = self._build_instruction_router(factory)
        
        session = SessionState(aggregate.get_by_name("main_group", only_one=True))
        
        quickedit_controller = self._build_quickedit_controller(
            session,
            aggregate,
            quickedit_router
        )
        
        group_selection_controller = self._build_group_selection_controller(session)
        
        router = self._build_router(
            quickedit_controller, 
            group_selection_controller
        )
        
        return self._build_controller(session, aggregate, router)