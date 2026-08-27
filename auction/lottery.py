from ..exceptions import APIError
from ..config import CONFIGURATION
from ..scripts.sender import create_session


async def lottery(ID: str) -> None:
    """
    Функция покупки тикета беспроигрышной лотереи. Проверяет, был ли он уже куплен и может вызвать ошибку.

    :param ID: ID покупателя (магазин)
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/auc/lottery",
                params={"ID": ID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(response.status, await response.json())
