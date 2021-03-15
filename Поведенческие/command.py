# Представляет запрос в виде объекта
# По цели - Поведенческий
# По применимости - Применятеся к объектам

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import List

class ArithmeticOperation(Enum):
    PLUS = '+'
    MINUS = '-'

class Command(ABC):
    '''
    Command
    Абстрактный интерфейс операции
    '''

    def __init__(self, processor: Processor, operand: float):
        self.processor = processor
        self.operand = operand
        self.result = None  

    @abstractmethod
    def do(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class Plus(Command):
    '''
    Concrete command
    Конкретная команда
    - реалиует операцию сложения, делегируя исполнение Получателю (объекту Processor)
    - также логирует исполнение 
    '''  
    
    def do(self):
        print(f'Add {self.operand}')
        self.result = self.processor.calculate(
            ArithmeticOperation.PLUS, self.operand)

    def undo(self):
        print(f'Undo add {self.operand}')
        self.processor.calculate(ArithmeticOperation.MINUS, self.operand)

class Minus(Command):
    '''
    Concrete command
    Конкретная команда
    - реалиует операцию сложения, делегируя исполнение Получателю (объекту Processor)
    - также логирует исполнение
    '''

    def do(self):
        print(f'Subtract {self.operand}')
        self.result = self.processor.calculate(
            ArithmeticOperation.MINUS, self.operand)

    def undo(self):
        print(f'Undo add {self.operand}')
        self.processor.calculate(ArithmeticOperation.PLUS, self.operand)

class Processor(ABC):
    '''
    Abstract Receiver
    Абстрактнй интерфейс получателя
    Определяет интерфейс команды расчета для операции и операнда
    '''

    def __init__(self, register: Regsiter):
        self.register = register

    @abstractmethod
    def calculate(self, operation: Enum, operand: float):
        return self.register.value

class ArithmeticProcessor(Processor):
    '''
    Receiver
    Получатель - реализует логику выполнения конкретных команд сложения и вычитания
    '''

    def calculate(self, operation: ArithmeticOperation, operand: float):
        if operation == ArithmeticOperation.PLUS:
            self.register.value += operand
        if operation == ArithmeticOperation.MINUS:
            self.register.value -= operand
        return self.register.value

class Register:
    '''
    Command value storage
    Класс вычисляемого значения
    '''
    
    def __init__(self):
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class Controller:
    '''
    Invoker
    Инициатор - исполняет команды и хранитих историю
    '''

    def __init__(self):
        self._commands: List[Command] = []
        self._current_command: int = 0

    def push_command(self, command: Command):
        self._commands.append(command)

    def do_command(self):
        self._commands[self._current_command].do()
        self._current_command += 1

    def undo_command(self):
        self._current_command -= 1
        self._commands[self._current_command].undo()
        self._commands.pop(self._current_command)

class ArithmeticCalculator:
    '''
    Client
    Клиент - арифметический калькулятор
    Использует арифметический процессор и набор команд
    '''

    def __init__(self):
        self.register = Register()
        self.arithemetic_processor = ArithmeticProcessor(self.register)
        self.controller = Controller() 

    def add(self, operand: float):
        self.calculate(Plus(self.arithemetic_processor, operand))

    def substract(self, operand: float):
        self.calculate(Minus(self.arithemetic_processor, operand))

    def calculate(self, command: Command):
        self.controller.push_command(command)
        self.controller.do_command()
        return self.register.value

    @property
    def value(self):
        return self.register.value

    def __str__(self):
        return f'==> {self.value}'

if __name__ == '__main__':
    calculator = ArithmeticCalculator()
    print(calculator)
    calculator.add(10)
    print(calculator)
    calculator.add(20)
    print(calculator)
    calculator.substract(15)
    print(calculator)