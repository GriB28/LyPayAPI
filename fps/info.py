from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError
from ..scripts.sender import create_session


async def check_status(ID: str) -> dict[str, ...]:
    """
    Запрос данных об FPS-<> в следующем формате:

    | {
    | "ID": str,
    | "author": str,
    | "author_type": str,
    | "description": str,
    | "amount": int,
    | "active": bool,
    | "unix": float
    | }

    :param ID: ID FPS-<>
    :return: словарь с данными FPS из таблицы ``database.FPS``
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/fps/info/status",
                params={"ID": ID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(check_status, response.status, json)

            return json
