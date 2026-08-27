from ..exceptions import APIError
from ..scripts.sender import create_session


async def is_agent(userID: int) -> bool:
    """
    Проверяет, является ли пользователь агентом

    :param userID: ID пользователя
    :return: True, если является; False, если нет
    """

    async with create_session() as session:
        async with session.get(
                "/admin/agent/check",
                params={"userID": userID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(response.status, json)

            return json["result"]


async def deposit(userID: int, amount: int, agentID: int) -> None:
    """
    Функция пополнения баланса. Создаёт новую валюту в системе.

    Формально разрешено "отрицательное" зачисление, поэтому этой функции следует избегать при работе с любыми
    переводами во избежание излишних проверок; для переводов есть `user.transfer()`

    :param userID: ID пользователя
    :param amount: сумма для зачисления
    :param agentID: ID агента (необязательный аргумент, но необходимо указывать везде, где это возможно)
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with create_session() as session:
        async with session.get(
                "/admin/agent/deposit",
                params={"userID": userID, "amount": amount, "agentID": agentID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(response.status, await response.json())


async def deposit_store(auctionID: int, amount: int, agentID: int) -> None:
    """
    Функция пополнения баланса для пересчёта перед аукционом

    :param auctionID: ID аукциона
    :param amount: сумма для зачисления
    :param agentID: ID агента (необязательный аргумент, но необходимо указывать везде, где это возможно)
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with create_session() as session:
        async with session.get(
                "/admin/agent/deposit_auc",
                params={"auctionID": auctionID, "amount": amount, "agentID": agentID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(response.status, await response.json())
