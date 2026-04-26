from random import choice as r_choice


alphabet = tuple("0123456789abcdefghijklmnopqrstuvwxyz")


def generate(length: int = 24) -> str:
    """
    Создаёт цифро-буквенный код, состоящий из символов ``0-9`` и ``a-z``

    :param length: необходимая длина кода
    :return: код (строка)
    """

    return ''.join(r_choice(alphabet) for _ in range(length))
