from aiohttp import ClientSession, TCPConnector
from ssl import create_default_context as ssl_create_default_context, CERT_NONE

from jwt import encode as jwt_encode

from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError
from ..scripts import j2

host = CONFIGURATION.HOST
port = CONFIGURATION.PORT
cache_path = CONFIGURATION.CACHEPATH

ssl_context = ssl_create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = CERT_NONE


async def get(chequeID: str) -> dict[str, ...]:
    """
    Запрос данных о чеке в следующем формате:
    | {
    | "chequeID": str,
    | "storeID": str,
    | "customer": int,
    | "unix": float,
    | "items": dict[itemID : multiplier],
    | "active": bool
    | }

    :param chequeID: ID чека
    :return: словарь с данными чека из таблицы ``database.CHEQUES``
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/store/cheques/get",
                params={"chequeID": chequeID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get, response.status, json)

            json["items"] = j2.from_('{' + json["items"] + '}')
            return json


async def get_all(storeID: str, active_filter: bool = True) -> list[str]:
    """
    Запрос данных обо всех чеках конкретного магазина.

    :param storeID: ID магазина
    :param active_filter: фильтр, показывающий только активные чеки (по умолчанию включён)
    :return: список ID чеков из таблицы ``database.CHEQUES``
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/store/cheques/all",
                params={"storeID": storeID, "active_filter": int(active_filter)}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_all, response.status, json)

            return json["result"]


async def create(storeID: str, customer: int, items: dict[str, int]) -> str:
    """
    Функция создания нового чека по введённым параметрам

    :param storeID: ID магазина
    :param customer: ID покупателя
    :param items: словарь с корзиной: {itemID : multiplier}
    :return: ID новго чека
    """

    payload = dict()
    payload["storeID"] = storeID
    payload["customer"] = customer
    payload["items"] = jwt_encode(items, CONFIGURATION.JWT_KEY, algorithm="HS256")

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/store/cheques/add",
                params=payload
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_all, response.status, json)

            return json["generated"]


async def cancel(chequeID: str) -> None:
    """
    Функция отмены чека

    :param chequeID: ID чека
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/store/cheques/de",
                params={"chequeID": chequeID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(cancel, response.status, await response.json())
