from ..__exceptions__ import APIError
from ..__config__ import CONFIGURATION
from ..scripts.sender import create_session


async def transfer(ID_out: int, ID_in: int | str, amount: int) -> None:
    """
    Функция перевода от покупателя покупателю (или магазину). Не изменяет количество валюты в системе.

    Ряд очевидных проверок проводится в самом ядре: сумма перевода положительна, оба ID существуют, у отправителя
    достаточно средств.

    Клиенту рекомендуется отдельно проверить случай ID_in = ID_out, к ошибке в ядре он не приведёт, но в общем случае
    пользователю сначала будет отправлено сообщение о снятии с его счёта денег, а потом сразу же о зачислении, что
    не является хорошим UX

    :param ID_out: ID пользователя (только покупатель)
    :param ID_in: ID получателя (другой покупатель или магазин)
    :param amount: сумма для перевода
    :return: ничего (может вызвать ошибку выполнения)
    """

    payload = dict()
    payload['ID_out'] = ID_out
    payload['ID_in'] = ID_in
    payload['amount'] = amount
    if type(ID_in) is int:
        payload['mode'] = 't'  # transfer
    else:
        payload['mode'] = 'b'  # buy

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/user/transfer",
                params=payload
        ) as response:
            if response.status >= 400:
                raise APIError.get(transfer, response.status, await response.json())


async def history(ID_out: int | None = None, ID_in: int | None = None) -> list:
    """
    Функция запроса списка всех переводов пользователь-пользователь.
    Если указан ID_out, то поиск вернёт список списков вида [ID_in (int), amount (int)].
    Если указан ID_in, то будет возвращено, соответственно, [ID_out (int), amount (int)].

    Ровно один из аргументов должен быть указан.

    :param ID_out: ID пользователя (если нужен поиск отправленных переводов)
    :param ID_in: ID пользователя (если нужен поиск полученных переводов)
    :return: список списков в указанном формате
    """

    payload = dict()
    if ID_out is not None:
        payload['ID_out'] = ID_out
    elif ID_in is not None:
        payload['ID_in'] = ID_in
    else:
        raise AttributeError

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/user/transfer/list",
                params={"ID_out": ID_out} if ID_out is not None else {"ID_in": ID_in}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(history, response.status, json)

            return json['result']
