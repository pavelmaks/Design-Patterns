# Позволяет объектам менять поведения в зависимости от состояния
# По цели - Поведенческий
# По применимости - Применятеся к объектам

from __future__ import annotations
from abc import ABC, abstractmethod

class State(ABC):
    '''интерфейс состояния'''

    def __init__(self, context: PosEmulator):
        self.context = context

    @abstractmethod
    def make_operation(self, operation: str):
        pass

    @abstractmethod
    def open_session(self):
        pass

    @abstractmethod
    def close_session(self):
        pass

class SessionClosedState(State):
    def open_session(self):
        print('Открываем смену')
        self.context.state = SessionOpenedState(self.context)

    def close_session(self):
        print('Печатаем копию отчета')

    def make_operation(self, operation: str):
        print(f'Выполняем операцию {operation}')
        raise Exception('Смена закрыта. Операция невозможна')

class SessionOpenedState(State):
    def open_session(self):
        pass

    def close_session(self):
        print('Печатаем копию отчета')
        self.context.state = SessionClosedState(self.context)

    def make_operation(self, operation: str):
        print(f'Выполняем операцию {operation} - успешно')

class SessionExpiredState(State):
    def open_session(self):
            pass

    def close_session(self):
        print('Печатаем копию отчета')
        self.context.state = SessionClosedState(self.context)

    def make_operation(self, operation: str):
        print(f'Выполняем операцию {operation}')
        raise Exception('Смена превысила 24 часа. Операция невозможна')

class PosEmulator:
    def __init__(self):
        self.state: State = SessionClosedState(self)

    def open_session(self):
        self.state.open_session()

    def close_session(self):
        self.state.close_session()

    def make_operation(self, operation: str):
        self.state.make_operation(operation)

    def make_session_expired(self):
        print('Смена кончилась, прошло 24 часа!')
        self.state = SessionExpiredState(self)

if __name__ == '__main__':
    emulator = PosEmulator()
    try:
        emulator.make_operation('Оплата 200р')
    except Exception as e:
        print(e)
    emulator.open_session()
    try:
        emulator.make_operation('Оплата 250р')
    except Exception as e:
        print(e)
    emulator.make_session_expired()
    try:
        emulator.make_operation('Оплата 300р')
    except Exception as e:
        print(e)
    emulator.close_session()
    emulator.open_session()
    try:
        emulator.make_operation('Оплата 350р')
    except Exception as e:
        print(e)
    emulator.close_session()