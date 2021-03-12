# Позволяет подставлять вместо реальных объектов специальные объекты-заменители
# Эти объекты прерыватывают вызовы к оригинальному объекту, позволяя сделать что-то до или после передачи вызова к оригиналу 
# По цели - Структурный
# По применимости - Применятеся к классам

import random
import time
from abc import ABC, abstractmethod
from typing import Dict
from uuid import uuid4

class Token:
    def __init__(self, key, ttl):
        self.key = key
        self.ttl = ttl
        self.created = time.time()

    @property
    def is_expired(self):
        return time.time() - self.created > self.ttl

class AbstractTokenManager(ABC):
    pass

    @abstractmethod
    def create_token(self, user_id):
        pass

class TokenManager(AbstractTokenManager):
    ttl = 3

    def create_token(self, user_id):
        key = self._get_token_from_db(user_id)
        print(f'Токен для пользователя {user_id}: {key}')
        return Token(key, self.ttl)

    def _get_token_from_db(self, user_id):
        print(f'Запрос токена из базы для пользователя {user_id}')
        time.sleep(2)
        print(f'Получен токен из базы для пользователя {user_id}')
        return uuid4()

class User:
    def __init__(self):
        self._user_id = random.randint(0, 100)

    @property   
    def user_id(self):
        return self._user_id

class CachedTokenManager(AbstractTokenManager):
    def __init__(self, token_manager: TokenManager):
        self.token_manager = token_manager
        self.cache: Dict[int, Token] = {}

    def refresh_token(self, user_id):
            self.cache[user_id] = self.token_manager.create_token(user_id)

    def create_token(self, user_id):
        if user_id in self.cache:
            cached_token: Token = self.cache[user_id]
            if cached_token.is_expired:
                print('Токен устарел, запрашиваю новый')
                self.refresh_token(user_id)
        else:
            self.refresh_token(user_id)

        print(f'Возвращаю токен из кэша для пользователя {user_id}')
        return self.cache[user_id]

if __name__ == '__main__':
    user = User()
    token_manager = TokenManager()
    time_start = time.time()
    token_manager.create_token(user.user_id)
    token_manager.create_token(user.user_id)
    print(f'Время двух запросов без прокси {time.time()-time_start:0.4f} секунд')
    print('---------------------------------------------------------------------')
    user = User()
    token_manager = CachedTokenManager(TokenManager())
    time_start = time.time()
    token_manager.create_token(user.user_id)
    token_manager.create_token(user.user_id)
    print(f'Время двух запросов c прокси {time.time()-time_start:0.4f} секунд')