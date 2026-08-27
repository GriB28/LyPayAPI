from inspect import currentframe


class APIError(Exception):
    def __init__(self, response: int | None = None, json: dict | None = None):
        """
        Класс ошибки API

        :param response: HTTP-код ответа от API
        :param json: JSON ответ от API
        """

        frame = currentframe().f_back
        if hasattr(frame.f_code, 'co_qualname'):
            self.method = frame.f_code.co_qualname
        else:
            self.method = frame.f_code.co_name

        self.status_code = response if response is not None else 0
        self.error_code = json["error"] if json is not None and "error" in json.keys() else "unknown"
        self.message = json["message"] if json is not None and "message" in json.keys() else None

    def __str__(self):
        return self.form_str_message()

    def form_str_message(self, custom_message: str | None = None) -> str:
        return f"""\
Получен код HTTP:{self.status_code} при вызове {self.method}. \
Сообщение ядра: {self.error_code} {
        f"({custom_message})" if custom_message is not None and len(custom_message) > 0 else
        (f"({self.message})" if self.message is not None and len(self.message) > 0 else "")
}
"""

    @classmethod
    def get(cls, response: int | None = None, json: dict | None = None) -> APIError:
        """
        Автоматический определитель конкретной ошибки

        :param response: HTTP-код ответа от API
        :param json: ответ от API в формате JSON
        :return: экземпляр APIError
        """

        if json is None or response is None or 'message' not in json.keys():
            pass

        elif json['message'] == 'bad parsing':
            return BadRequest(response, json)

        elif json['message'] == 'invalid route':
            return InvalidRoute(response, json)

        elif json['message'] == 'email not found':
            return EmailNotFound(response, json)

        elif json['message'] == 'ID not found':
            return IDNotFound(response, json)
        elif json['message'] == 'ID already exists':
            return IDAlreadyExists(response, json)

        elif json['message'] == 'login not found':
            return LoginNotFound(response, json)
        elif json['message'] == 'login already exists':
            return LoginAlreadyExists(response, json)

        elif json['message'] == 'not enough balance':
            return NotEnoughBalance(response, json)
        elif json['message'] == 'subzero input':
            return SubZeroInput(response, json)

        elif json['message'] == 'avatar not found':
            return MediaNotFound(response, json)

        elif json['message'] == 'bad censor flag: user name':
            return InvalidUserName(response, json)
        elif json['message'] == 'bad censor flag: login':
            return InvalidUserLogin(response, json)

        elif json['message'] == 'bad censor flag: store name':
            return InvalidStoreName(response, json)
        elif json['message'] == 'bad censor flag: store desc':
            return InvalidStoreDescription(response, json)

        elif json['message'] == 'bad censor flag: store item name':
            return InvalidStoreItemName(response, json)
        elif json['message'] == 'bad censor flag: store item price':
            return InvalidStoreItemPrice(response, json)

        elif json['message'] == 'bad censor flag: FPS desc':
            return InvalidFPSDescrition(response, json)

        elif json['message'] == 'link email not found':
            return RegistrationEmailNotFound(response, json)

        elif json['message'] == 'no python processes found':
            return NoPythonProcessesFound(response, json)

        elif json['message'] == 'db returned a void':
            return DBReturnedAVoid(response, json)

        elif json['message'] == 'bad fw check':
            return BadFireWallCheck(response, json)

        elif json['message'] == 'user is already a shopkeeper':
            return UserIsAlreadyAShopkeeper(response, json)

        elif json['message'] == 'launcher flag blocked':
            return LauncherFlagBlocked(response, json)

        elif json['message'] == 'ticket has already been purchased':
            return LotteryTicketCantBePurchased(response, json)

        return cls(response, json)


class IDNotFound(APIError):
    def __str__(self):
        return super().form_str_message("ID не был найден")


class EmailNotFound(APIError):
    def __str__(self):
        return super().form_str_message("эл. почта не была найдена в базе")


class LoginNotFound(APIError):
    def __str__(self):
        return super().form_str_message("логин не был найден в базе")


class IDAlreadyExists(APIError):
    def __str__(self):
        return super().form_str_message("ID уже существует")


class LoginAlreadyExists(APIError):
    def __str__(self):
        return super().form_str_message("пользователь с таким логином уже существует")


class BadRequest(APIError):
    def __str__(self):
        return super().form_str_message("ядро не смогло обработать запрос")


class InvalidRoute(APIError):
    def __str__(self):
        return super().form_str_message("выбраный параметр пути некорректен")


class NotEnoughBalance(APIError):
    def __str__(self):
        return super().form_str_message("баланса пользователя недостаточно для оплаты")


class SubZeroInput(APIError):
    def __str__(self):
        return super().form_str_message("в поле для перевода введено число меньше нуля")


class MediaNotFound(APIError):
    def __str__(self):
        return super().form_str_message("медиа-контент не был найден")


class InvalidUserName(APIError):
    def __str__(self):
        return super().form_str_message("имя пользователя не прошло проверку")


class InvalidUserLogin(APIError):
    def __str__(self):
        return super().form_str_message("логин пользователя не прошёл проверку")


class InvalidStoreName(APIError):
    def __str__(self):
        return super().form_str_message("название магазина не прошло проверку")


class InvalidStoreDescription(APIError):
    def __str__(self):
        return super().form_str_message("описание магазина не прошло проверку")


class InvalidStoreItemName(APIError):
    def __str__(self):
        return super().form_str_message("название айтема не прошло проверку")


class InvalidStoreItemPrice(APIError):
    def __str__(self):
        return super().form_str_message("цена айтема некорректна")


class InvalidFPSDescrition(APIError):
    def __str__(self):
        return super().form_str_message("описание FPS-линка не прошло проверку")


class RegistrationEmailNotFound(APIError):
    def __str__(self):
        return super().form_str_message("почта с таким кодом доступа не найдена в базе данных")


class NoPythonProcessesFound(APIError):
    def __str__(self):
        return super().form_str_message("ядро не смогло найти процесс(ы) Python")


class DBReturnedAVoid(APIError):
    def __str__(self):
        return super().form_str_message("ответа на запрос к базе данных не последовало")


class BadFireWallCheck(APIError):
    def __str__(self):
        return super().form_str_message("запрос не прошёл проверку файерволла")


class UserIsAlreadyAShopkeeper(APIError):
    def __str__(self):
        return super().form_str_message("пользователь уже имеет доступ к какому-то магазину")


class LauncherFlagBlocked(APIError):
    def __str__(self):
        return super().form_str_message("действие заблокировано флагом ядра")


class LotteryTicketCantBePurchased(APIError):
    def __str__(self):
        return super().form_str_message("билет лотереи уже был куплен")


__all__ = (
    "APIError",
    "IDNotFound",
    "EmailNotFound",
    "LoginNotFound",
    "IDAlreadyExists",
    "LoginAlreadyExists",
    "BadRequest",
    "InvalidRoute",
    "NotEnoughBalance",
    "SubZeroInput",
    "MediaNotFound",
    "InvalidUserName",
    "InvalidUserLogin",
    "InvalidStoreName",
    "InvalidStoreDescription",
    "InvalidStoreItemName",
    "InvalidStoreItemPrice",
    "InvalidFPSDescrition",
    "RegistrationEmailNotFound",
    "NoPythonProcessesFound",
    "DBReturnedAVoid",
    "BadFireWallCheck",
    "UserIsAlreadyAShopkeeper",
    "LauncherFlagBlocked",
    "LotteryTicketCantBePurchased"
)