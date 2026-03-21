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


async def add(name: str, price: int, auctionID: int) -> int:
    """
    Функция создания новой записи о лоте (без покупателя)

    :param name: название лота
    :param price: стоимость лота
    :param auctionID: auctionID из таблицы ``database.STORES``
    :return: созданный ID лота
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/auc/lot/add",
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

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/auc/lot/confirm",
                params={"lotID": lotID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(add, response.status, await response.json())
