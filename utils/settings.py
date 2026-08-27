from ..exceptions import APIError
from ..scripts.sender import create_session


async def get(key: str):
    """
    Запрос значения флага лаунчера по ключу

    :param key: ключ настройки
    :return: значение, храящееся по заданному ключу
    """

    async with create_session() as session:
        async with session.get(
                "/fw/setting",
                params={"key": key}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(response.status, json)

            return json['result']
