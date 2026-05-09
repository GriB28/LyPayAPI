from ..__exceptions__ import APIError
from ..__config__ import CONFIGURATION
from ..scripts.sender import create_session


async def view(ID: int) -> int:
    """
    Запрос баланса пользователя

    :param ID: ID пользователя
    :return: число
    """

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/user/balance",
                params={"ID": ID}
        ) as response:
            json = await response.json()
            if response.status >= 400:
                raise APIError.get(view, response.status, json)

            return json["balance"]


async def deposit(ID: int, value: int, agent_id: int | None = None) -> None:
    """
    Функция пополнения баланса. Создаёт новую валюту в системе.

    Формально разрешено "отрицательное" зачисление, поэтому этой функции следует избегать при работе с любыми
    переводами во избежание излишних проверок; для переводов есть `transfer()`

    :param ID: ID пользователя
    :param value: сумма для зачисления
    :param agent_id: ID агента (необязательный аргумент, но необходимо указывать везде, где это возможно)
    :return: ничего (может вызвать ошибку выполнения)
    """

    payload = dict()
    if agent_id is not None:
        payload['agent_id'] = agent_id
    payload['ID'] = ID
    payload['value'] = value

    async with create_session() as session:
        async with session.get(
                f"{CONFIGURATION.HOST}:{CONFIGURATION.PORT}/user/deposit",
                params=payload
        ) as response:
            if response.status >= 400:
                raise APIError.get(deposit, response.status, await response.json())


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
