from ..__exceptions__ import APIError
from ..__config__ import CONFIGURATION
from ..scripts.sender import create_session


async def get_list(storeID: str) -> list[int]:
    """
    Запрос данных о доступе пользователей к магазину

    :param storeID: ID магазина
    :return: список userID тех пользователей, которые имеют доступ к магазину (из таблицы``database.SHOPKEEPERS``)
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/access/list",
                params={"storeID": storeID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_list, response.status, json)

            return json["result"]


async def add(storeID: str, userID: int) -> None:
    """
    Запрос данных о доступе пользователей к магазину

    :param storeID: ID магазина
    :param userID: ID пользователя
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/access/add",
                params={"storeID": storeID, "userID": userID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(add, response.status, await response.json())


async def remove(storeID: str, userID: int) -> None:
    """
    Функция удаления доступа пользователя к магазину

    :param storeID: ID магазина
    :param userID: ID пользователя
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/access/rem",
                params={"storeID": storeID, "userID": userID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(remove, response.status, await response.json())
