from ...exceptions import APIError
from ...scripts.sender import create_session


async def get(ID: str) -> str:
    """
    Запрос данных об описании магазина

    :param ID: ID магазина
    :return: описание
    """

    async with create_session() as session:
        async with session.get(
                "/store/settings/desc/get",
                params={"ID": ID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(response.status, json)

            return json['result']


async def update(ID: str, new: str):
    """
    Обновление описания магазина

    :param ID: ID магазина
    :param new: новое описание
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with create_session() as session:
        async with session.get(
                "/store/settings/desc/upd",
                params={"ID": ID, "new": new}
        ) as response:
            if response.status >= 400:
                raise APIError.get(response.status, await response.json())
