from aiohttp import ClientSession, TCPConnector

from hashlib import sha256

from .scripts import random_data
from ..config import CONFIGURATION
from ..exceptions import APIError


async def main() -> tuple[str, str]:
    """
    Запускает 1 итерацию теста с пакетом на 10 мегабайт

    :return: две строки, первая -- полученный хэш, вторая -- исходный
    """

    data = random_data(10 * 1024)
    data_hash = sha256(data).hexdigest()

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.post(
                "/mst/test1",
                data=data
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(response.status, json)

            return json["hash"], data_hash
