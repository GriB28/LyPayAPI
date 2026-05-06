from psutil import cpu_percent as CPU, virtual_memory as RAM, process_iter
from platform import system as get_platform_name

from ..__exceptions__ import APIError
from ..__config__ import CONFIGURATION
from ..scripts.sender import create_session

_platform_name = get_platform_name()


async def core_machine() -> dict[str, ...]:
    """
    Запрос данных о нагрузке на сервер ядра в следующем формате:

    | {
    | "cpu": float (процент занятости процессора),
    | "ram_p": float (процент занятости оперативки),
    | "ram_v": float (абсолютное значение занятости оперативки в гигабайтах),
    | "cpu_build": float (процент занятости процессора сборкой),
    | "ram_build_p": float (процент занятости оперативки сборкой),
    | "ram_build_v": float (абсолютное значение занятости оперативки сборкой в гигабайтах),
    | "cpu_cores": list[float] (процент занятости каждого ядра процессора (по порядку))
    | }

    :return: словарь с данными о машине ядра
    """

    async with create_session() as session:
        async with session.get(f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/admin/machine") as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(core_machine, response.status, json)

            return json


def local_machine() -> dict[str, ...]:
    """
    Делает то же самое, что и ``core_machine``, но берёт данные с локальной машины клиента

    :return: словарь с данными о локальной машине
    """

    python_processes = list()
    for running_process in process_iter():
        if running_process.name() == (
                "python.exe" if _platform_name == 'Windows' else
                ("python3" if _platform_name == 'Linux' else "")
        ) and len(running_process.cmdline()) > 0:  # and running_process.cmdline()[-1] == lls -- legacy part
            python_processes.append(running_process)
    if len(python_processes) == 0:
        raise APIError.get(local_machine, 404, {"error": "NameError", "message": "no python processes found"})

    r = RAM()
    return {
        "cpu": CPU(),
        "ram_p": r.percent,
        "ram_v": (r.total - r.available) / 1073741824,
        "cpu_build": sum(list(map(lambda p: p.cpu_percent(), python_processes))) / len(python_processes),
        "ram_build_p": round(sum(list(map(lambda p: p.memory_percent(), python_processes))) / len(python_processes), 2),
        "ram_build_v": sum(list(map(lambda p: p.memory_info().rss, python_processes))) / 1073741824 / len(python_processes),
        "cpu_cores": CPU(percpu=True)
    }


async def db_query(db_type: str, query: str) -> list[...]:
    """
    Функция для исполнения любого запроса к любой базе данных ядра (см. ``db_type``)

    :param db_type: 'main' (главная база данных) или 'fw' (файерволл)
    :param query: запрос
    :return: словарь с данными о машине ядра
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/admin/db",
                params={"db_type": db_type, "query": query}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(db_query, response.status, json)

            return json["result"]
