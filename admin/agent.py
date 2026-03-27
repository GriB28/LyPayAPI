from aiohttp import ClientSession, TCPConnector
from ssl import create_default_context as ssl_create_default_context, CERT_NONE

from platform import system as get_platform_name

from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError

host = CONFIGURATION.HOST
port = CONFIGURATION.PORT
cache_path = CONFIGURATION.CACHEPATH

ssl_context = ssl_create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = CERT_NONE

platform_name = get_platform_name()


async def is_agent(userID: int) -> bool:
    """
    Проверяет, является ли пользователь агентом

    :param userID: ID пользователя
    :return: True, если является; False, если нет
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/admin/agent/check",
                params={"userID": userID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(is_agent, response.status, json)

            return json["result"]


async def deposit(userID: int, amount: int, agentID: int) -> None:
    """
    Функция агентского пополнения баланса пользователя

    :param userID: ID пользователя
    :param amount: сумма для зачисления
    :param agentID: ID исполнителя операции
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/admin/agent/deposit",
                params={"userID": userID, "amount": amount, "agentID": agentID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(deposit, response.status, await response.json())
