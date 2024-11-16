# Передает запрос вдоль цепочки, пока один из обрабтчиков не обработает передаваемый запрос.
# По цели - Поведенческий
# По применимости - Применятеся к объектам

from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from typing import Union


class Handler(ABC):
    '''Handler interface'''

    @abstractmethod
    def set_next(self, handler: Handler) ->  Handler:
        pass

    @abstractmethod
    def handle(self, request):
        pass

class Decoder(Handler):
    '''Abstract Handler'''

    def __init__(self):
        self._next_handler: Union[Handler, None] = None

    @property
    @abstractmethod
    def encoding(self) -> str:
        pass

    def set_next(self, handler: Handler):
        self._next_handler = handler
        return handler

    def handle(self, request):
        try:
            print(f'Попытка декодировать строку в кодировке {self.encoding}')
            return DecodingResult(self.encoding, request.decode(self.encoding), True)
        except UnicodeDecodeError:
            if self._next_handler is not None:
                return self._next_handler.handle(request)

class Cp1251Decoder(Decoder):
    '''Concrete handler'''

    @property
    def encoding(self) -> str:
        return 'cp1251'

class Utf8Decoder(Decoder):
    '''Concrete handler'''

    @property
    def encoding(self) -> str:
        return 'utf-8'

class DecodingResult:
    def __init__(
        self, encoding: str = None, encoded_str: str = None, 
        is_encoded: bool = False
    ):
        self.encoding = encoding
        self.encoded_str = encoded_str
        self.is_encoded = is_encoded

    def __str__(self):
        return self.encoded_str

class FailedDecodingLogger(Handler):
    '''Concrete handler (Terminator)'''

    def set_next(self, handler):
        pass

    def handle(self, request):
        print(f"Не удалось обработать строку: {request.decode(sys.stdout.encoding, 'replace')}")
        return DecodingResult(is_encoded=False)

if __name__ == '__main__':
    
    print('Chain #1 example')
    utf_8_encoded = 'привет '.encode('utf-8')
    cp_1251_encoded = 'привет'.encode('cp1251')
    cp_1251 = Cp1251Decoder()
    utf_8 = Utf8Decoder()
    failed_logger = FailedDecodingLogger()
    cp_1251.set_next(utf_8).set_next(failed_logger)
    result = cp_1251.handle(utf_8_encoded)
    if result.is_encoded:
        print(f'Успешно декодировано, кодировка определена: {result.encoding}')
    print('='*100)

    print('Chain #2 example')
    utf_8 = Utf8Decoder()
    failed_logger = FailedDecodingLogger()
    utf_8.set_next(failed_logger)
    result = utf_8.handle(b'\x81')