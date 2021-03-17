# Позволяет последовательно обходить элементы составных объектов, не раскрывая их внутреннего представления
# По цели - Поведенческий
# По применимости - Применятеся к объектам

from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from enum import Enum
from typing import List

@dataclass
class Client:
    '''Client with a name and balance'''
    name: str
    balance: int

class ClientCollection(Iterable):
    '''
    Client collection
    Offers an ability to sort clients in different ways
    '''

    def __init__(self):
        self._clients: List[CLient] = []
        self._default_iterator = self.by_alphabet

    def add_client(self, client: Client):
        self._clients.append(client)

    def get_clients(self) -> List[Client]:
        return self._clients

    def __iter__(self) -> ClientSortIterator:
        return self._default_iterator()

    def by_fifo(self) -> ClientSortIterator:
        return FifoIterator(self)
    
    def by_lifo(self) -> ClientSortIterator:
        return LifoIterator(self)

    def by_alphabet(self) -> ClientSortIterator:
        return AlphabetIterator(self)

    def by_balance(self) -> ClientSortIterator:
        return BallanceIterator(self)

class ClientSortIterator(Iterator):
    def __init__(self, collection: ClientCollection, is_reverse=False):
        self.clients = collection.get_clients()
        self.cursor = len(self.clients) - 1 if is_reverse else 0
        self.is_reverse: bool = is_reverse
        self.sort(self.clients)

    def sort(self, clients: List[Client]):
        pass

    def __next__(self) -> Client:
        try:
            if self.cursor < 0:
                raise IndexError()
            value = self.clients[self.cursor]
            self.cursor += -1 if self.is_reverse else 1
            return value
        except IndexError:
            raise StopIteration()

class FifoIterator(ClientSortIterator):
    '''FIFO'''
    pass

class LifoIterator(ClientSortIterator):
    '''FIFO'''
    
    def __init__(self, collection: ClientCollection):
        super().__init__(collection, is_reverse=True)

class AlphabetIterator(ClientSortIterator):
    
    def sort(self, clients: List[Client]):
        self.clients = sorted(clients, key=lambda client: client.name)

class BallanceIterator(ClientSortIterator):

    def __init__(self, collection: ClientCollection):
        super().__init__(collection, is_reverse=True)

    def sort(self, clients: List[Client]):
        self.clients = sorted(clients, key=lambda client: client.balance)

if __name__ == '__main__':
    clients = ClientCollection()

    clients.add_client(Client(name='Vasya', balance=10))
    clients.add_client(Client(name='Misha', balance=123))
    clients.add_client(Client(name='Seryozha', balance=1238))
    clients.add_client(Client(name='Sasha', balance=192))

    print('='*50)
    print('By name:')
    [print(client) for client in clients]
    print('='*50)
    print('FIFO:')
    [print(client) for client in clients.by_fifo()]
    print('='*50)
    print('LIFO:')
    [print(client) for client in clients.by_lifo()]
    print('='*50)
    print('By balance:')
    [print(client) for client in clients.by_balance()]
    print('='*50)


