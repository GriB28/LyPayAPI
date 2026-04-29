from aiohttp import ClientSession, TCPConnector

from os import urandom
from hashlib import sha256

from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError


async def main() -> tuple[str, str]:
    """
    Запускает 1 итерацию теста с пакетом на 10 мегабайт

    :return: две строки, первая -- полученный хэш, вторая -- исходный
    """

    data = _generate_random_data(10)
    data_hash = sha256(data).hexdigest()

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.post(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/mst/test1",
                data=data
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(main, response.status, json)

            return json["hash"], data_hash


def _generate_random_data(N: int) -> bytes:
    """
    Создаёт ``N`` мегабайт случайной информации

    :param N: размер данных
    :return: мусорные данные
    """

    return urandom(1024 * 1024 * N)
