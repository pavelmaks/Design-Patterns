# В системе есть несколько различных сервисов авторизации,
# и для успешной аутентификации пользователя необходимо реализовать паттерн "Цепочка ответственности".
# Каждый сервис авторизации будет представлять собой отдельный обработчик,
# который будет проверять наличие учетных данных и передавать управление следующему обработчику в цепочке,
# если не сможет обработать запрос.

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Handler(ABC):
    """Handler interface"""

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request: Any) -> Any:
        pass


class AuthenticationHandler(Handler):
    _next_handler: Handler = None

    def __init__(self, handler: Handler | None = None):
        self._next_handler = handler

    @abstractmethod
    def authenticate(self, user_data: dict) -> bool:
        pass

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    def handle(self, request):
        res = self.authenticate(request)
        if not res and self._next_handler is not None:
            return self._next_handler.handle(request)
        return res


class LocalAuthHandler(AuthenticationHandler):
    def authenticate(self, user_data: dict) -> bool:
        if user_data.get("username") == "admin" and user_data.get("password") == "admin":
            return True
        return False


class SmsAuthHandler(AuthenticationHandler):
    def authenticate(self, user_data: dict) -> bool:
        if user_data.get("phone") == "79991234567" and user_data.get("code") == "666":
            return True
        return False


if __name__ == "__main__":
    local_auth = LocalAuthHandler()
    sms_auth = SmsAuthHandler()
    local_auth.set_next(sms_auth)
    data = {"username": "admin", "password": "admin"}
    print(local_auth.handle(data))
    data = {"phone": "79991234567", "code": "666"}
    print(local_auth.handle(data))
    data = {"phone": "79991234567", "code": "232"}
    print(local_auth.handle(data))
