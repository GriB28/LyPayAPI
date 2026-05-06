from ..__exceptions__ import APIError
from ..__config__ import CONFIGURATION
from ..scripts.sender import create_session


async def transfer(ID_out: str, ID_in: str, amount: int) -> None:
    """
    Функция переводов между двумя магазинами. Копирует функционал ``user.balance.transfer`` (без выбора рута отправки)

    :param ID_out: ID отправителя (только магазин)
    :param ID_in: ID получателя (только магазин)
    :param amount: сумма для перевода
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/auc/transfer",
                params={"ID_out": ID_out, "ID_in": ID_in, "amount": amount}
        ) as response:
            if response.status >= 400:
                raise APIError.get(transfer, response.status, await response.json())
