from ..__exceptions__ import APIError
from ..__config__ import CONFIGURATION
from ..scripts.sender import create_session


async def is_agent(userID: int) -> bool:
    """
    Проверяет, является ли пользователь агентом

    :param userID: ID пользователя
    :return: True, если является; False, если нет
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/admin/agent/check",
                params={"userID": userID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(is_agent, response.status, json)

            return json["result"]


async def deposit(userID: int, value: int, agent_id: int | None = None) -> None:
    """
    Функция пополнения баланса. Создаёт новую валюту в системе.

    Формально разрешено "отрицательное" зачисление, поэтому этой функции следует избегать при работе с любыми
    переводами во избежание излишних проверок; для переводов есть `user.transfer()`

    :param userID: ID пользователя
    :param value: сумма для зачисления
    :param agent_id: ID агента (необязательный аргумент, но необходимо указывать везде, где это возможно)
    :return: ничего (может вызвать ошибку выполнения)
    """

    payload = dict()
    if agent_id is not None:
        payload['agent_id'] = agent_id
    payload['userID'] = userID
    payload['value'] = value

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/admin/agent/deposit",
                params=payload
        ) as response:
            if response.status >= 400:
                raise APIError.get(deposit, response.status, await response.json())
