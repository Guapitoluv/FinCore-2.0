from fincore.application.dto.group_dto import MoneyDTO
from fincore.domain.value_objects.money import Money


class MoneyFactory:
    @staticmethod
    def create(dto: MoneyDTO) -> Money:
        return Money(
            reais=dto.reais,
            centavos=dto.centavos
        )