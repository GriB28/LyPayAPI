from ..config import CONFIGURATION
from ..exceptions import APIError, IDNotFound
from ..scripts.sender import create_session


async def check(ID: int, route: str) -> bool:
    """
    Быстрая проверка доступа

    :param ID: ID пользователя
    :param route: 'main', 'stores', 'admins' или 'high'
    :return: True, если доступ разрешён, False -- в противном случае
    """

    route = route.strip().lower()
    try:
        user_accesses = tuple(map(lambda r: r["access"], await entries(ID, route)))
        return all(user_accesses)
    except IDNotFound:
        if route == 'main':
            return True
        return False


async def entries(ID: int, route: str) -> list[dict[str, ...]]:
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
    :return: список словарей с данными пользователя из таблицы ``firewall.STORES``
    """

    route = route.strip().lower()
    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/fw/{route}",
                params={"ID": ID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(response.status, json)

            return json['result']
