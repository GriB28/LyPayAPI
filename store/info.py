from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError
from ..scripts.sender import create_session


async def get(ID: str) -> dict[str, ...]:
    """
    Запрос данных о магазине в следующем формате:

    | {
    | "ID": str,
    | "name": str,
    | "hostID": int,
    | "description": str,
    | "logo": bool,
    | "balance": int,
    | "hostEmail": str,
    | "auctionID": int,
    | "placeID": str
    | }

    :param ID: ID магазина
    :return: словарь с данными магазина из таблицы ``database.STORES``
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/info/get/base",
                params={"ID": ID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get, response.status, json)

            return json


async def get_by_shopkeeper(ID: int) -> str:
    """
    Запрос ID магазина по ID продавца

    :param ID: ID продавца
    :return: ID магазина по таблице ``database.SHOPKEEPERS``
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/info/get/shopkeeper",
                params={"ID": ID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_by_shopkeeper, response.status, json)

            return json['storeID']


async def get_all_ids() -> list[str]:
    """
    Запрос всех существующих ID магазинов

    :return: список с ID из таблицы ``database.STORES``
    """

    async with create_session() as session:
        async with session.get(f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/info/all/stores") as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_all_ids, response.status, json)

            return json['ids']


async def get_all_shopkeepers() -> list[int]:
    """
    Запрос всех userID пользователей, имеющих доступ к любому магазину

    :return: список с userID из таблицы ``database.SHOPKEEPERS``
    """

    async with create_session() as session:
        async with session.get(f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/info/all/shopkeepers") as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_all_shopkeepers, response.status, json)

            return json['ids']
