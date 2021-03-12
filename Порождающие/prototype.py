# Позволяет копировать объекты, не вдаваясь в подробности их реализации
# По цели - Порождающий
# По применимости - Применятеся к объектам

from abc import abstractmethod, ABC
from copy import deepcopy

class Clonable(ABC):

    @abstractmethod
    def clone(self):
        pass

class Connection:
    def __init__(self, host, port, login, password):
        self.is_open = False
        self.host = host
        self.port = port
        self.login = login
        self.password = password

    def open(self):
        self.is_open = True
        print('Conn opened')

class Config:
    def __init__(self, topic, partition, offset):
        self.topic = topic
        self.partition = partition
        self.offset = offset

class Consumer(Clonable):
    def __init__(self, connection: Connection, config: Config):
        self.connection = connection
        self.config = config

    def clone(self):
        return Consumer(self.connection, deepcopy(self.config))

    def start(self):
        if not self.connection.is_open:
            self.connection.open()
        print(
            'Start to consume messages from '
            f'topic: {self.config.topic} '
            f'partition: {self.config.partition} '
            f'offset: {self.config.offset} '
        )

if __name__ == '__main__':
    connection = Connection('localhost', '4351', 'sysbda', 'not_masterkey')
    config = Config('topic A', '31', 1111)
    consumer = Consumer(connection, config)
    consumer.start()

    consumer_2 = consumer.clone()
    consumer_2.config.offset = 77
    consumer_2.start()
