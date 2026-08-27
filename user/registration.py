from jwt import encode as jwt_encode

from ..exceptions import APIError
from ..config import CONFIGURATION
from ..scripts.sender import create_session


async def check_email_record(email: str) -> dict[str, ...]:
    """
    Запрос данных в таком формате:

    | {
    | "name": str,
    | "email": str,
    | "group": str
    | }

    :param email: эл. почта пользователя
    :return: словарь с данными пользователя из таблицы ``database.CORPORATION``
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/reg/email/corp_record",
                params={"email": email}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(response.status, json)

            return json


async def send_email(route: str, participant: str, code: str | None = None, keys: dict[str, ...] | None = None) -> None:
    """
    Отправляет письмо по эл. почте

    :param route: 'main' или 'guest' -- два разных шаблона письма для лицеистов/сотрудников и гостей Ярмарки
    :param participant: почта получателя
    :param code: код верификации пользователя (по умолчанию генерируется рандомно)
    :param keys: словарь ключей для замены в итоговом письме (выставляется по умолчанию)
    :return: ничего (может вызвать ошибку выполнения)
    """

    payload = dict()
    if keys is not None:
        payload["keys"] = jwt_encode(keys, CONFIGURATION.JWT_KEY, algorithm="HS256")
    if code is not None:
        payload["code"] = code
    payload["route"] = route
    payload["email"] = participant

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/reg/email/send",
                params=payload
        ) as response:
            if response.status >= 400:
                raise APIError.get(response.status, await response.json())


async def check_code(email: str, code: str, route: str = 'main') -> bool:
    """
    Проверяет код регистрации пользователя

    :param email: почта для проверки
    :param code: код для проверки
    :param route: 'main' или 'guest' -- вариант регистрации
    :return: статус проверки (True/False)
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/user/code",
                params={"code": code, "route": route}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(response.status, json)

            return json["email"] == email

async def new(*, name: str, login: str | None, password: str | None, group: str, email: str, tag: str | None = None, owner_flag: str) -> int:
    """
    Регистрация нового пользователя

    :param name: имя (по таблцие ``database.CORPORATION``)
    :param login: логин
    :param password: пароль
    :param group: группа (по таблице ``database.CORPORATION``)
    :param email: эл. почта
    :param tag: telegram tag (по умолчанию пропущен)
    :param owner_flag: 'tg_owner', 'tg_guest', 'web_owner', 'web_guest' или 'integration' (для каждой платформы клиент должен сам контролировать этот аргумент)
    :return: ID новой записи
    """

    payload = dict()
    payload["name"] = name
    payload["group"] = group
    payload["email"] = email
    payload["owner_flag"] = owner_flag
    if tag is not None:
        payload["tag"] = tag
    if login is not None and password is not None:
        payload["login"] = login
        payload["password"] = password

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/reg/user",
                params=payload
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(response.status, json)

            return json['ID']
