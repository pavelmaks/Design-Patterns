# Позволяет схранятьи  восстанавливать прошлые состояния объекта, не раскрывая их реалиации
# По цели - Поведенческий
# По применимости - Применятеся к объектам

from abc import ABC, abstractmethod
from time import time
from typing import List
from functools import reduce

class DocumentSnapshot:
    '''Memento'''

    def __init__(self, positions: List):
        self._positions = positions

    def get_state(self):
        return self._positions

    def __str__(self):
        return f'Snapshot of {len(self._positions)}, positions: {self._positions}'

class Document:
    '''Originator'''

    def __init__(self):
        self._positions = []

    def add_position(self, position: str):
        print(f'+ {position}')
        self._positions.append(position)

    def create_shapshot(self) -> DocumentSnapshot:
        '''Create memento'''
        return DocumentSnapshot(self._positions[:])

    def restore_shapshot(self, snapshot: DocumentSnapshot):
        '''Set memento'''
        self._positions = snapshot.get_state()

    def __str__(self):
        return f'positions in document: {", ".join(self._positions)}'

class History:
    '''Caretaker'''

    def __init__(self, document: Document):
        self._document: Document = document
        self._snapshots: List[DocumentSnapshot] = [] # memento storage

    def _print_snapshots(self):
        if len(self._snapshots) > 0:
            str_snapshots = reduce(
                lambda prev, cur: f'{cur}, {prev}', 
                self._snapshots
            )
            print(f'Current history {str_snapshots}')
        else:
            print('Current history is empty')

    def backup(self):
        print('---> backing up current state')
        self._snapshots.append(self._document.create_shapshot())
        self._print_snapshots()

    def undo(self):
        print('<--- Undo last change')
        if len(self._snapshots) > 0:
            snapshot = self._snapshots.pop()
            self._document.restore_shapshot(snapshot)
        self._print_snapshots()

    def restore_to_index(self, index):
            assert index >= 0 and index < len(self._snapshots)
            print(f'<--- restore to {index + 1} snapshot')
            snapshot = self._snapshots[index]
            self._document.restore_shapshot(snapshot)
            self._snapshots = self._snapshots[0:index]

if __name__ == '__main__':
    document = Document()
    history = History(document)
    document.add_position('position 1')
    print(document)
    history.backup()
    document.add_position('position 2')
    document.add_position('position 3')
    print(document)
    history.undo()
    print(document)
    document.add_position('position 4')
    print(document)
    history.backup()
    print(document)
    document.add_position('position 5')
    print(document)
    history.backup()
    print(document)
    history.restore_to_index(0)
    print(document)