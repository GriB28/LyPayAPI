from jwt import encode as jwt_encode

from ..config import CONFIGURATION
from ..exceptions import APIError
from ..scripts.sender import create_session
from ..scripts import j2



async def get(chequeID: str) -> dict[str, ...]:
    """
    Запрос данных о чеке в следующем формате:
    | {
    | "chequeID": str,
    | "storeID": str,
    | "customer": int,
    | "unix": float,
    | "items": dict[itemID (str) : multiplier (int)],
    | "active": bool
    | }

    :param chequeID: ID чека
    :return: словарь с данными чека из таблицы ``database.CHEQUES``
    """

    async with create_session() as session:
        async with session.get(
                "/store/cheques/get",
                params={"chequeID": chequeID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(response.status, json)

            json["items"] = j2.from_(json["items"])
            return json


async def get_all(storeID: str, active_filter: bool = True) -> list[str]:
    """
    Запрос данных обо всех чеках конкретного магазина.

    :param storeID: ID магазина
    :param active_filter: фильтр, показывающий только активные чеки (по умолчанию включён)
    :return: список ID чеков из таблицы ``database.CHEQUES``
    """

    async with create_session() as session:
        async with session.get(
                "/store/cheques/all",
                params={"storeID": storeID, "active_filter": int(active_filter)}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(response.status, json)

            return json["result"]


async def create(storeID: str, customer: int, items: dict[str, int]) -> str:
    """
    Функция создания нового чека по введённым параметрам (ПЕРЕВОДИТ тугрики автоматически)

    :param storeID: ID магазина
    :param customer: ID покупателя
    :param items: словарь с корзиной: {itemID : multiplier}
    :return: ID нового чека
    """

    payload = dict()
    payload["storeID"] = storeID
    payload["customer"] = customer
    payload["items"] = jwt_encode(items, CONFIGURATION.JWT_KEY, algorithm="HS256")

    async with create_session() as session:
        async with session.get(
                "/store/cheques/add",
                params=payload
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(response.status, json)

            return json["generated"]


async def cancel(chequeID: str) -> None:
    """
    Функция отмены чека (ВОЗВРАЩАЕТ тугрики автоматически)

    :param chequeID: ID чека
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with create_session() as session:
        async with session.get(
                "/store/cheques/de",
                params={"chequeID": chequeID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(response.status, await response.json())
