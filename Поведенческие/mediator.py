# Позволяет уменьшить связность множества классов меджду собой вследствие перемещения этих связей в класс-посредник
# По цели - Поведенческий
# По применимости - Применятеся к объектам

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from random import choice
from typing import Optional

class Event(ABC):
    '''Абстрактный класс обмена сообщеинями'''
    pass

@dataclass
class Issue(Event):
    '''Конкретное сообщеине о проблеме'''
    topic: str
    description: str
    status: IssueStatus

    def __str__(self):
        return f'Тема проблемы: {self.topic}. Описание: {self.description}. Статус: {self.status}'

class IssueStatus(Enum):
    '''Состояние процесса решения проблемы'''
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    RESOLVED = 'resolved'

class Mediator(ABC):
    '''
    Абстрактный класс-посредник
    Посредник определяет алгоритм действий и централизованно обрабатывает сообщения от объектов-коллег 
    '''
    @abstractmethod
    def send(self, sender: Colleague, event: Event) -> None:
        pass
    

class Colleague(ABC):
    '''
    Абстрактный класс объектов-коллег
    Каждый объект-коллега будет знать только о посреднике и отправлять сообщения через него
    '''
    def __init__(self):
        self._mediator: Optional[Mediator] = None

    @property
    def mediator(self):
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator

class Employee(Colleague):
    '''Сотрудник предприятия'''

    def __init__(self):
        super().__init__()
        self.issue: Optional[Issue] = None

class Client(Colleague):
    '''Клиент'''

    def report_issue(self, topic, description):
        issue = Issue(topic, description, IssueStatus.NEW)
        print(f'Клиент подал заявку: {issue}')
        self.mediator.send(self, issue)

    def notify(self, issue: Issue):
        print(f'Клиент получил ответ по заявке {issue}')

class Supporter(Employee):
    '''Сотрудник предприятия из службы поддержки'''
    def resolve_issue(self):
        print(f'Сотрудник ТП самостоятельно решил проблему {self.issue}')
        self.issue.status = IssueStatus.RESOLVED
        self.mediator.send(self, self.issue)

    def escalate_issue(self):
        print(f'Сотрудник ТП перенаправил проблему {self.issue}')
        self.mediator.send(self, self.issue)
    
    def set_issue(self, issue: Issue):
        self.issue = issue
        self.issue.status = IssueStatus.IN_PROGRESS
        choice([self.resolve_issue, self.escalate_issue])()

class Programmer(Employee):
    '''Сотрудник отдела разработки'''
    def resolve_issue(self):
        self.issue.status = IssueStatus.RESOLVED
        print(f'Программист героически объявил баг {self.issue} фичей')
        self.mediator.send(self, self.issue)
    
    def set_issue(self, issue: Issue):
        self.issue = issue
        self.resolve_issue()

class CRM(Mediator):
    '''КОнкретный посредник в виде системы CRM'''
    def __init__(self, client: Client, supporter: Supporter, programmer: Programmer):
        self.client = client
        self.client.mediator = self
        self.supporter = supporter
        self.supporter.mediator = self
        self.programmer = programmer
        self.programmer.mediator = self

    def send(self, sender: Colleague, event: Issue):
        if isinstance(sender, Client):
            self.supporter.set_issue(event)
        elif isinstance(sender, Supporter):
            if event.status == IssueStatus.IN_PROGRESS:
                self.programmer.set_issue(event)
            else:
                self.client.notify(event)
        elif isinstance(sender, Programmer):
            self.client.notify(event)
        
if __name__ == '__main__':
    client = Client()
    supporter = Supporter()
    programmer = Programmer()
    CRM(client, supporter, programmer)

    print('='*130)
    client.report_issue('Ничего не работает', 'Сделайте хорошо')
    print('='*130)
    client.report_issue('Ничего не работаетx2', 'Сделайте хорошоx2')
    print('='*130)