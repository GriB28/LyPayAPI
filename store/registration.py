from ..__exceptions__ import APIError
from ..__config__ import CONFIGURATION
from ..scripts.sender import create_session

from jwt import encode as jwt_encode


async def check_link(email: str, link: str) -> bool:
    """
    Проверяет код регистрации магазина

    :param email: почта для проверки
    :param link: код для проверки
    :return: статус проверки (True/False)
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/store/info/link",
                params={"link": link}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(check_link, response.status, json)

            return json["email"] == email


async def get_ID() -> str:
    """
    Запрашивает свободный ID магазина

    :return: незанятый ID магазина
    """

    async with create_session() as session:
        async with session.get(f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/reg/store_id") as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(get_ID, response.status, json)

            return json["ID"]


async def send_email(participant: str, code: str | None = None, keys: dict[str, ...] | None = None) -> None:
    """
    Отправляет письмо по эл. почте

    :param participant: почта получателя
    :param code: код доступа (по умолчанию генерируется рандомный)
    :param keys: словарь ключей для замены в итоговом письме (выставляется по умолчанию)
    :return: ничего (может вызвать ошибку выполнения)
    """

    payload = dict()
    if keys is not None:
        payload["keys"] = jwt_encode(keys, CONFIGURATION.JWT_KEY, algorithm="HS256")
    if code is not None:
        payload["code"] = code
    payload["route"] = "shopkeeper"
    payload["email"] = participant

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/reg/email/send",
                params=payload
        ) as response:
            if response.status >= 400:
                raise APIError.get(send_email, response.status, await response.json())


async def new(*, storeID: str, name: str, hostID: int, email: str) -> None:
    """
    Регистрация нового магазина (описание по умолчанию -- ``""``)

    :param storeID: ID магазина
    :param name: название магазина
    :param hostID: ID владельца магазина
    :param email: эл. почта владельца магазина
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/reg/store",
                params={
                    "storeID": storeID,
                    "name": name,
                    "hostID": hostID,
                    "email": email
                }
        ) as response:
            if response.status >= 400:
                raise APIError.get(new, response.status, await response.json())
