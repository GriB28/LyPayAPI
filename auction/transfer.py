from aiohttp import ClientSession, TCPConnector
from ssl import create_default_context as ssl_create_default_context, CERT_NONE

from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError

host = CONFIGURATION.HOST
port = CONFIGURATION.PORT
cache_path = CONFIGURATION.CACHEPATH

ssl_context = ssl_create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = CERT_NONE


async def transfer(ID_out: str, ID_in: str, amount: int) -> None:
    """
    Функция переводов между двумя магазинами. Копирует функционал ``user.balance.transfer`` (без выбора рута отправки)

    :param ID_out: ID отправителя (только магазин)
    :param ID_in: ID получателя (только магазин)
    :param amount: сумма для перевода
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/auc/transfer",
                params={"ID_out": ID_out, "ID_in": ID_in, "amount": amount}
        ) as response:
            if response.status >= 400:
                raise APIError.get(transfer, response.status, await response.json())
