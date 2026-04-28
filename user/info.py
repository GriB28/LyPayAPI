from aiohttp import ClientSession, TCPConnector

from os.path import getmtime, exists, join
from os import remove

from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError
from ..scripts.mem import save_iterative


async def get(ID: int) -> dict[str, ...]:
    """
    Запрос данных о пользователе в следующем формате:

    | {
    | "ID": int,
    | "name": str,
    | "login": str | None,
    | "password": str | None,
    | "group": str,
    | "email": str,
    | "tag": str | None,
    | "balance": int,
    | "owner": int
    | }

    :param ID: ID пользователя
    :return: словарь с данными пользователя из таблицы ``database.USERS``
    """

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/user/get",
                params={"ID": ID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get, response.status, json)

            return json


async def get_by_email(email: str) -> dict[str, ...]:
    """
    Запрос данных о пользователе в следующем формате:

    | {
    | "ID": int,
    | "name": str,
    | "login": str | None,
    | "password": str | None,
    | "group": str,
    | "email": str,
    | "tag": str | None,
    | "balance": int,
    | "owner": int
    | }

    :param email: email пользователя
    :return: словарь с данными пользователя из таблицы ``database.USERS``
    """

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/user/get",
                params={"email": email}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_by_email, response.status, json)

            return json


async def get_by_login(login: str) -> dict[str, ...]:
    """
    Запрос данных о пользователе в следующем формате:

    | {
    | "ID": int,
    | "name": str,
    | "login": str | None,
    | "password": str | None,
    | "group": str,
    | "email": str,
    | "tag": str | None,
    | "balance": int,
    | "owner": int
    | }

    :param login: login пользователя
    :return: словарь с данными пользователя из таблицы ``database.USERS``
    """

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/user/get",
                params={"login": login}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_by_login, response.status, json)

            return json


async def get_all() -> list[int]:
    """
    Запрос всех существующих ID пользователей

    :return: список с ID из таблицы ``database.USERS``
    """

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/user/all") as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_all, response.status, json)

            return json['ids']


async def _request_qr(ID: int, path: str) -> None:
    """
    Внутренняя функция, не рекомендуется использовать без обёртки `qr()`
    """

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/user/qr/get",
                params={"ID": ID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(_request_qr, response.status, await response.json())

            await save_iterative(response, path, CONFIGURATION.CHUNK_SIZE)


async def qr(ID: int) -> str:
    """
    Проверяет актуальность QR с ID пользователя, в случае необходимости запрашивает новые данные с сервера и сохраняет их локально

    :param ID: ID пользователя
    :return: абсолютный путь до файла (независимо от того, было обновление или нет)
    """

    path = join(CONFIGURATION.CACHEPATH, "users_qr", f"{ID}.png")
    if exists(path):
        async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
            async with session.get(
                    f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/user/qr/check",
                    params={"ID": ID, "unix": getmtime(path)}
            ) as response:
                json = await response.json()
                if response.status >= 400:
                    raise APIError.get(qr, response.status, json)

                if not json["actual"]:
                    remove(path)
                if not json["exists"] or not json["actual"]:
                    await _request_qr(ID, path)
                return path

    else:
        await _request_qr(ID, path)
        return path
