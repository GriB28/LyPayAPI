from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError
from ..scripts.sender import create_session


async def new(*, description: str | None = None, amount: int, author: str | int) -> str:
    """
    Создание нового FPS-линка

    :param description: описание FPS-линка (опционально)
    :param amount: сумма перевода
    :param author: ID создателя перевода
    :return: ID созданного FPS-линка
    """

    payload = dict()
    if description is not None:
        payload['description'] = description
    payload['amount'] = amount
    payload['author'] = author

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/fps/new",
                params=payload,
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(new, response.status, json)

            return json['ID']


async def cancel(ID: str) -> None:
    """
    Отмена (деактивация) созданного FPS-линка.
    Можно деактивировать только тот FPS-линк, что ещё не был оплачен.

    :param ID: ID FPS-линка
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/fps/cancel",
                params={'ID': ID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(cancel, response.status, await response.json())
