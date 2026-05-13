from ..__config__ import CONFIGURATION
from ..__exceptions__ import APIError
from ..scripts.sender import create_session


async def pay(fpsID: str, userID: int) -> str | None:
    """
    Оплата FPS-линка

    :param fpsID: ID FPS-линка
    :param userID: ID плательщика
    :return: ID созданного чека, если автором FPS-линка является магазин, иначе -- None
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/fps/pay",
                params={"fpsID": fpsID, "userID": userID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(pay, response.status, json)

            return json["chequeID"]
