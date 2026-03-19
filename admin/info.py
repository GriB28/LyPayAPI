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


async def machine() -> dict[str, ...]:
    """
    Запрос данных о нагрузке на сервер ядра в следующем формате:

    | {
    | "cpu": float (процент занятости процессора),
    | "ram_p": float (процент занятости оперативки),
    | "ram_v": float (абсолютное значение занятости оперативки в гигабайтах),
    | "cpu_build": float (процент занятости процессора сборкой),
    | "ram_build_p": float (процент занятости оперативки сборкой),
    | "ram_build_v": float (абсолютное значение занятости оперативки сборкой в гигабайтах),
    | "cpu_cores": list[float] (процент занятости каждого ядра процессора (по порядку))
    | }

    :return: словарь с данными о машине
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(f"{host}:{port}/admin/machine") as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(machine, response, json)

            return json
