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


async def get_list(storeID: str) -> list[int]:
    """
    Запрос данных о доступе пользователей к магазину

    :param storeID: ID магазина
    :return: список userID тех пользователей, которые имеют доступ к магазину (из таблицы``database.SHOPKEEPERS``)
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/store/access/list",
                params={"storeID": storeID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_list, response, json)

            return json["result"]


async def add(storeID: str, userID: int) -> None:
    """
    Запрос данных о доступе пользователей к магазину

    :param storeID: ID магазина
    :param userID: ID пользователя
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/store/access/add",
                params={"storeID": storeID, "userID": userID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(get_list, response, await response.json())


async def remove(storeID: str, userID: int) -> None:
    """
    Функция удаления доступа пользователя к магазину

    :param storeID: ID магазина
    :param userID: ID пользователя
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/store/access/rem",
                params={"storeID": storeID, "userID": userID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(get_list, response, await response.json())

