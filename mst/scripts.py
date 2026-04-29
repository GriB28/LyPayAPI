from os import urandom


def random_data(N: int) -> bytes:
    """
    Создаёт ``N`` килобайт случайной информации

    :param N: размер данных
    :return: мусорные данные
    """

    return urandom(1024 * N)
