from aiohttp import ClientSession, TCPConnector
from ssl import create_default_context as ssl_create_default_context, CERT_NONE

from ..scripts import j2
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


async def send_email(participant: str, code: str | int, keys: dict[str, ...] | None = None) -> None:
    """
    Отправляет письмо по эл. почте

    :param participant: почта получателя
    :param code: код доступа к магазину
    :param keys: словарь ключей для замены в итоговом письме (выставляется по умолчанию)
    :return: ничего (может вызвать ошибку выполнения)
    """

    payload = dict()
    if keys is not None:
        payload["keys"] = j2.to_(keys, string_mode=True)
    payload["route"] = "shopkeeper"
    payload["email"] = participant
    payload["code"] = code

    async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as session:
        async with session.get(
                f"{host}:{port}/reg/email/send",
                params=payload
        ) as response:
            if response.status >= 400:
                raise APIError.get(send_email, response, await response.json())
