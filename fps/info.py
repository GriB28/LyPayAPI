from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError
from ..scripts.sender import create_session


async def status(ID: str) -> dict[str, ...]:
    """
    Запрос данных об FPS-<=> в следующем формате:

    | {
    | "ID": str,                -- ID FPS-<=>
    | "author": str | int       -- ID автора, int для пользователя, str для магазина
    | "description": str,       -- описание FPS-<=>
    | "amount": int,            -- стоимость
    | "payed": int,             -- ID оплатившего пользователя (если не оплачен -- null)
    | "cheque": str,            -- ID привязанного чека (если не оплачен -- null)
    | "unix_creation": float,   -- UNIX-timestamp создания FPS-<=>
    | "unix_payment": float     -- UNIX-timestamp оплаты FPS-<=>
    | }

    :param ID: ID FPS-<=>
    :return: словарь с данными FPS-<=> из таблицы ``database.FPS``
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/fps/info/status",
                params={"ID": ID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(status, response.status, json)

            return json
