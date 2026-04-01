from aiohttp import ClientSession, TCPConnector

from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError, IDNotFound


async def check(ID: int, route: str) -> bool:
    """
    Быстрая проверка доступа

    :param ID: ID пользователя
    :param route: 'main', 'stores', 'admins' или 'high'
    :return: True, если доступ разрешён, False -- в противном случае
    """

    route = route.strip().lower()
    try:
        user = await entry(ID, route)
        return user['access']
    except IDNotFound:
        if route == 'main':
            return True
        return False


async def entry(ID: int, route: str) -> dict[str, ...]:
    """
    Запрос профиля пользователя в файерволле в формате:

    | {
    | "ID": int,
    | "unix": float,
    | "access": bool,
    | "comment": str | None
    | }

    :param ID: ID пользователя
    :param route: 'main', 'stores', 'admins' или 'high'
    :return: словарь с данными пользователя из таблицы ``firewall.STORES``
    """

    route = route.strip().lower()
    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/fw/{route}",
                params={"ID": ID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(entry, response.status, json)

            return json['result']
