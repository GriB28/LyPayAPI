from asyncio import sleep
from .scripts import random_data


async def main() -> bytes:
    """
    Запускает 1 итерацию симуляции ответа сервера на 1 мегабайт

    :return: пакет с мусорными данными
    """

    await sleep(0.005)
    return random_data(1024)
