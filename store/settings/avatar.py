from aiohttp import ClientSession, TCPConnector, FormData

from os.path import getmtime, exists, join
from os import remove
from aiofiles import open as a_open

from ...__config__ import CONFIGURATION
from ...__exceptions__ import APIError
from ...scripts.mem import save_iterative


async def get(ID: str) -> tuple[str, bool] | None:
    """
    Запрос данных об аватаре магазина

    :param ID: ID магазина
    :return: None, если аватара нет (или больше нет), в противном случае -- путь до файла с кэшем аватара и
    флаг обновления (True, если обновлён, False, если нет).
    """

    path = join(CONFIGURATION.CACHEPATH, "stores_media", f"{ID}.jpg")
    payload = dict()
    payload["ID"] = ID
    if exists(path):
        payload["unix"] = getmtime(path)

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/settings/avatar/get",
                params=payload
        ) as response:
            if "json" in response.content_type:
                json = await response.json()
            else:
                json = {"message": "unknown", "error": "unknown", "result": "got image content"}

            if response.status >= 400:
                raise APIError.get(get, response.status, json)

            if json['result'] == "no icon":
                if exists(path):
                    remove(path)
                return None

            flag = False
            if json['result'] != "avatar didn't change":
                await save_iterative(response, path, CONFIGURATION.CHUNK_SIZE)
                flag = True
            return path, flag


async def update(ID: str, media_path: str):
    """
    Обновление аватарки магазина

    :param ID: ID магазина
    :param media_path: путь (абсолютный) до файла с аватаром
    :return: ничего (может вызвать ошибку выполнения)
    """

    media_type = media_path.split(".")[-1]
    form = FormData()
    async with a_open(media_path, 'rb') as avatar:
        form.add_field(
            "avatar",
            await avatar.read(),
            content_type=f"image/{media_type}"
        )

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.post(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/settings/avatar/upd",
                params={"ID": ID},
                data=form
        ) as response:
            if response.status >= 400:
                raise APIError.get(update, response.status, await response.json())


async def delete(ID: str):
    """
    Удаление аватарки магазина

    :param ID: ID магазина
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with ClientSession(connector=TCPConnector(ssl=CONFIGURATION.SSL)) as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/settings/avatar/remove",
                params={"ID": ID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(delete, response.status, await response.json())
