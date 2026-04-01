from aiohttp import ClientSession, TCPConnector

from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError


async def add(name: str, price: int, auctionID: int) -> int:
    """
    Функция создания новой записи о лоте (без покупателя)

    :param name: название лота
    :param price: стоимость лота
    :param auctionID: auctionID из таблицы ``database.STORES``
    :return: созданный ID лота
    """

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/auc/lot/add",
                params={"name": name, "price": price, "auctionID": auctionID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(add, response.status, json)

            return json['generated']


async def confirm(lotID: int) -> None:
    """
    Функция подтверждения покупки лота по сохранённому ID

    :param lotID: ID лота для подтверждения
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/auc/lot/confirm",
                params={"lotID": lotID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(add, response.status, await response.json())
