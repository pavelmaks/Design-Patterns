# Определяет общий интерфейс для создания объектов в суперсклассе, позволяя подклассам изменять тип содаваемых объектов
# По цели - Порождающий
# По применимости - Применятеся к классам

from abc import ABC, abstractmethod
import random
from enum import Enum

class User(ABC):
    '''Пользователь'''
    pass

class MtsUser(User):
    '''Пользователь МТС с номером телефона'''

    def __init__(self, phone):
        print(f'Created MtsUser with phone {phone}')

class LiteboxUser(User):
    '''Пользователь Лайтбокс с почтой'''

    def __init__(self, email):
        print(f'Created LiteboxUser with email {email}')

class Credentials(ABC):
    '''Абстрактные учетные данные'''
    pass

class LiteboxCredentials(Credentials):
    '''Учетные данные для входа в лайтбокс'''
    def __init__(self, email, password):
        self._email = email
        self._password = password

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

class MtsCredentials(Credentials):
    '''Учетные данные для входа в мтс'''
    def __init__(self, email, password):
        self._phone = phone
        self._password = password

    @property
    def phone(self):
        return self._phone

    @property
    def password(self):
        return self._password

class Authenticator(ABC):
    @abstractmethod
    def authenticate(self, credentials: Credentials) -> User:
        pass

class LiteboxAuthenticator(Authenticator):
    def authenticate(self, credentials: LiteboxCredentials) -> LiteboxUser:
        print(f'Authenticated by email {credentials.email}')
        return LiteboxUser(credentials.email)

class MtsAuthenticator(Authenticator):
    def authenticate(self, credentials: MtsCredentials) -> MtsUser:
        print(f'Authenticated by phone {credentials.phone}')
        return MtsUser(credentials.phone)

def authenticate(authenticator: Authenticator, credentials: Credentials) -> User:
    return authenticator().authenticate(credentials)

phone = '+79164752676'
password = '***'
credentials = MtsCredentials(phone, password)
user: MtsUser = authenticate(MtsAuthenticator, credentials)

email = 'litebox@litebox.com'
password = '***'
credentials = LiteboxCredentials(email, password)
user: LiteboxUser = authenticate(LiteboxAuthenticator, credentials)


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

from __future__ import annotations

class Interval:
    multyplicity_seconds = 1000
    multyplicity_minutes = 60
    '''
    Фабричный метод использзуется для удобных операция инстанцирования
    (Конструктор vs фабричный метод)
    '''
    def __init__(self, milliseconds):
        self._milliseconds = milliseconds

    @staticmethod
    def from_milliseconds(milliseconds) -> Interval:
        return Interval(milliseconds)

    @classmethod
    def from_seconds(cls, seconds) -> Interval:
        return cls.from_milliseconds(second*cls.multyplicity_seconds)

    @classmethod
    def from_minutes(cls, minutes) -> Interval:
        return cls.from_seconds(minutes*cls.multyplicity_minutes)

    @property
    def milliseconds(self):
        return self._milliseconds
    
    @property
    def seconds(self):
        return self._milliseconds / self.multyplicity_seconds

    @property
    def minutes(self):
        return self._milliseconds / self.multyplicity_minutes
