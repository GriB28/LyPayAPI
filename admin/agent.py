from aiohttp import ClientSession, TCPConnector

from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError


async def is_agent(userID: int) -> bool:
    """
    Проверяет, является ли пользователь агентом

    :param userID: ID пользователя
    :return: True, если является; False, если нет
    """

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/admin/agent/check",
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

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/admin/agent/deposit",
                params={"userID": userID, "amount": amount, "agentID": agentID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(deposit, response.status, await response.json())
