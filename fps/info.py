from ..exceptions import APIError
from ..scripts.sender import create_session


async def status(ID: str) -> dict[str, ...]:
    """
    Запрос данных об FPS-линке в следующем формате:

    | {
    | "ID": str,                -- ID FPS-линка
    | "author": str | int       -- ID автора, int для пользователя, str для магазина
    | "description": str,       -- описание FPS-линка
    | "amount": int,            -- стоимость
    | "payed": int,             -- ID оплатившего пользователя (если не оплачен -- None)
    | "cheque": str,            -- ID привязанного чека (если не оплачен или автор -- не магазин, то None)
    | "unix_creation": float,   -- UNIX-timestamp создания FPS-линка
    | "unix_payment": float     -- UNIX-timestamp оплаты FPS-линка (если не оплачен -- None)
    | }

    :param ID: ID FPS-линка
    :return: словарь с данными FPS-линка из таблицы ``database.FPS``
    """

    async with create_session() as session:
        async with session.get(
                "/fps/status",
                params={"ID": ID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(response.status, json)

            return json
