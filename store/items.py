from aiohttp import ClientSession, TCPConnector

from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError


async def get(ID: str) -> dict[str, ...]:
    """
    Запрос данных об айтеме в следующем формате:

    | {
    | "itemID": str,
    | "storeID: str,
    | "name": str,
    | "price": int,
    | "active: bool
    | }

    :param ID: ID айтема
    :return: словарь с данными об айтеме из таблицы ``database.ITEMS``
    """

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/items/get",
                params={"itemID": ID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get, response.status, json)

            return json


async def get_all(storeID: str, active_filter: bool = True) -> list[str]:
    """
    Запрос данных обо всех айтемах конкретного магазина

    :param storeID: ID магазина
    :param active_filter: фильтр, показывающий только активные айтемы (по умолчанию включён)
    :return: список ID айтемов из таблицы ``database.ITEMS``
    """

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/items/all",
                params={"storeID": storeID, "active_filter": int(active_filter)}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_all, response.status, json)

            return json["result"]


async def add(storeID: str, name: str, price: int) -> str:
    """
    Функция создания нового айтема

    :param storeID: ID магазина
    :param name: название айтема
    :param price: цена айтема
    :return: ID созданного айтема
    """

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/items/add",
                params={"storeID": storeID, "name": name, "price": price}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(add, response.status, json)

            return json["generated"]


async def remove(itemID: str) -> None:
    """
    Функция удаления (деактивации) айтема

    :param itemID: ID айтема
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/items/rem",
                params={"itemID": itemID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(remove, response.status, await response.json())


async def edit(itemID: str, name: str | None = None, price: int | None = None) -> str:
    """
    Функция зименения данных об айтеме. Фактически при изменении любого параметра создаётся новая запись.
    Обязателен хотя бы один аргумент кроме ID

    :param itemID: ID магазина
    :param name: новое название айтема
    :param price: новая цена айтема
    :return: ID изменённого айтема
    """

    payload = dict()
    if name is not None:
        payload["name"] = name
    if price is not None:
        payload["price"] = price
    if len(payload) == 0:
        raise ValueError("В вызове функции promo.edit должен присутствовать хотя бы один аргумент кроме ID.")
    payload["itemID"] = itemID

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/items/edit",
                params=payload
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(edit, response.status, json)

            return json["updated"]
