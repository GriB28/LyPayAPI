from ..exceptions import APIError
from ..scripts.sender import create_session


async def add(name: str, price: int, auctionID: int, lotID: int | None = None) -> int:
    """
    Функция создания новой записи о лоте (без покупателя)

    :param name: название лота
    :param price: стоимость лота
    :param auctionID: auctionID из таблицы ``database.STORES``
    :param lotID: ID лота (если не задан, то создаётся следующий по порядку)
    :return: созданный ID лота
    """

    payload = {"name": name, "price": price, "auctionID": auctionID}
    if lotID is not None:
        payload["lotID"] = lotID

    async with create_session() as session:
        async with session.get(
                "/auc/lot/add",
                params=payload
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(response.status, json)

            return json['indexed']


async def confirm(lotID: int) -> None:
    """
    Функция подтверждения покупки лота по сохранённому ID

    :param lotID: ID лота для подтверждения
    :return: ничего (может вызвать ошибку выполнения)
    """

    async with create_session() as session:
        async with session.get(
                "/auc/lot/confirm",
                params={"lotID": lotID}
        ) as response:
            if response.status >= 400:
                raise APIError.get(response.status, await response.json())


async def all_lots(storeID: str) -> list[dict[str, ...]]:
    """
    Функция, возвращающая список лотов (словарей) определённого магазина в формате:

    | {
    | "lotID": int,
    | "name: str,
    | "price": int,
    | "auctionID": int,
    | "confirmed": bool
    | }

    :param storeID: ID магазина
    :return: список словарей в указанном формате
    """

    async with create_session() as session:
        async with session.get(
                "/auc/lot/list",
                params={"storeID": storeID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(response.status, json)

            return json['result']
