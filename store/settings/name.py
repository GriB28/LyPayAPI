from ...__exceptions__ import APIError
from ...__config__ import CONFIGURATION
from ...scripts.sender import create_session


async def get(ID: str) -> str:
    """
    Запрос данных о названии магазина

    :param ID: ID магазина
    :return: название
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/settings/name/get",
                params={"ID": ID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get, response.status, json)

            return json['result']


async def update(ID: str, new: str):
    """
    Обновление названия магазина

    :param ID: ID магазина
    :param new: новое название
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/settings/name/upd",
                params={"ID": ID, "new": new}
        ) as response:
            if response.status >= 400:
                raise APIError.get(update, response.status, await response.json())
