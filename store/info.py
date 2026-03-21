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

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/store/info/get",
                params={"ID": ID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get, response.status, json)

            return json


async def get_all_ids() -> list[str]:
    """
    Запрос всех существующих ID магазинов

    :return: список с ID из таблицы ``database.STORES``
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(f"{host}:{port}/store/info/all/stores") as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_all_ids, response.status, json)

            return json['ids']


async def get_all_shopkeepers() -> list[int]:
    """
    Запрос всех userID пользователей, имеющих доступ к любому магазину

    :return: список с userID из таблицы ``database.SHOPKEEPERS``
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(f"{host}:{port}/store/info/all/shopkeepers") as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_all_shopkeepers, response.status, json)

            return json['ids']
