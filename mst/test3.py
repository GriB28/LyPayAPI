from aiohttp import ClientSession, TCPConnector

from os import urandom
from hashlib import sha256

from ..config import CONFIGURATION
from ..exceptions import APIError

local_counter = dict()


async def main(ID: int):
    """
    Запускает 1 итерацию теста с увеличением значения в ячейке на единицу + обновляет локальный счётчик

    :param ID: ID пользователя
    """

    if ID not in local_counter.keys():
        local_counter[ID] = 0

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/mst/test3",
                params={"ID": ID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(response.status, await response.json())
            local_counter[ID] += 1


async def end(ID: int) -> tuple[int, int]:
    """
    Завершает тест

    :param ID: ID пользователя
    :return: значение локального счётчика и значение из БД
    """

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/mst/test3_end",
                params={"ID": ID}
        ) as response:
            json = await response.json()

            if response.status >= 400:
                raise APIError.get(response.status, json)

            return local_counter[ID] if ID in local_counter.keys() else 0, json["value"]
