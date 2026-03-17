from aiohttp import ClientSession, TCPConnector
from ssl import create_default_context as ssl_create_default_context, CERT_NONE

from jwt import encode as jwt_encode

from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError

host = CONFIGURATION.HOST
port = CONFIGURATION.PORT
cache_path = CONFIGURATION.CACHEPATH

ssl_context = ssl_create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = CERT_NONE



async def check_link(link: str) -> str:
    """
    Проверяет код регистрации магазина

    :param link: код для проверки
    :return: эл. почту, на которую был прислан этот код. При этом никакие записи не удаляются,
    происходит только проверка
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/store/info/link",
                params={"link": link}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(check_link, response, json)

            return json["email"]


async def get_ID():
    """
    Запрашивает свободный ID магазина

    :return: незанятый ID магазина
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(f"{host}:{port}/reg/store_id") as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_ID, response, json)

            return json["ID"]


async def send_email(participant: str, keys: dict[str, ...] | None = None) -> None:
    """
    Отправляет письмо по эл. почте

    :param participant: почта получателя
    :param keys: словарь ключей для замены в итоговом письме (выставляется по умолчанию)
    :return: ничего (может вызвать ошибку выполнения)
    """

    payload = dict()
    if keys is not None:
        payload["keys"] = jwt_encode(keys, CONFIGURATION.JWT_KEY, algorithm="HS256")
    payload["route"] = "shopkeeper"
    payload["email"] = participant

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/reg/email/send",
                params=payload
        ) as response:
            if response.status >= 400:
                raise APIError.get(send_email, response, await response.json())


async def new(*, storeID: int, name: str, hostID: int, email: str) -> None:
    """
    Регистрация нового магазина (описание по умолчанию -- ``""``)

    :param storeID: ID магазина
    :param name: название магазина
    :param hostID: ID владельца магазина
    :param email: эл. почта владельца магазина
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/reg/store",
                params={
                    "storeID": storeID,
                    "name": name,
                    "hostID": hostID,
                    "email": email
                }
        ) as response:
            if response.status >= 400:
                raise APIError.get(new, response, await response.json())
