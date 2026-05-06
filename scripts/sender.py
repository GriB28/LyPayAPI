from aiohttp import ClientSession, TCPConnector
from ..__config__ import CONFIGURATION


class CustomSession(ClientSession):
    def __init__(self, *args, extra: dict | None = None, **kwargs):
        """
        Кастомная сессия, которая добавляет заданные query-параметры ко всем запросам

        :param extra: словарь с дополнительными дефолтными параметрами
        :param args: args
        :param kwargs: kwargs
        """
        super().__init__(*args, **kwargs)
        self._extra_params = extra if extra is not None else dict()

    async def _request(self, method, url, **kwargs):
        params = kwargs.get('params')

        if params is not None:
            if isinstance(params, dict):
                new_params = {**params, **self._extra_params}
            elif isinstance(params, (list, tuple)):
                new_params = list(params)
                new_params.extend(self._extra_params.items())
            elif hasattr(params, 'extend'):
                params.extend(self._extra_params)
                new_params = params
            else:
                try:
                    new_params = dict(params)
                    new_params.update(self._extra_params)
                except TypeError, ValueError:
                    new_params = params
            kwargs['params'] = new_params

        elif self._extra_params:
            kwargs['params'] = self._extra_params.copy()

        return await super()._request(method, url, **kwargs)


def create_session():
    """
    Создаёт новый инстэнс кастомной сессии
    """

    return CustomSession(
        connector=TCPConnector(ssl=CONFIGURATION.SSL),
        extra={"token": CONFIGURATION.TOKEN} if CONFIGURATION.TOKEN is not None else None,
    )
