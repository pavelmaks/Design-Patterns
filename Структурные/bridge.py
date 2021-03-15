# Позволяет разделить абстракция и реализацию так, чтобы их можно было изменять независимо друг от друга
# По цели - Структурный
# По применимости - Применятеся к объектам

from abc import ABC, abstractmethod

class Driver(ABC):
    '''Интефрейс'''
    
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def push(self, message):
        pass

class KafkaDriver(Driver):
    '''Конкретная имплементация'''

    def connect(self):
        self._connect_to_broker()

    def _connect_to_broker(self):
        print('Connected to Kafka broker')

    def _select_topic(self):
        print('Selecet topic')

    def disconnect(self):
        self._disconnect_from_broker()

    def _disconnect_from_broker(self):
        print('Disconnected from Kafka broker')
    
    def push(self, message):
        self._select_topic()
        print(f'Push message {message} into Kafka')

class RedisDriver(Driver):
    '''Конкретная имплементация'''

    def connect(self):
        self._connect_to_db()

    def _connect_to_db(self):
        print('Connected to Redis DB')

    def disconnect(self):
        self._disconnect_from_db()

    def _disconnect_from_db(self):
        print('Disconnected from Redis DB')
    
    def push(self, message):
        print(f'Push message {message} into Redis queue')

class Producer(ABC):
    '''Абстракция'''

    def __init__(self, driver: Driver):
        self.driver = driver

    @abstractmethod
    def send(self, message):
        pass

class MessageProducer(Producer):
    '''Уточненная абстракция'''

    def send(self, message):
        self.driver.connect()
        self.driver.push(message)
        self.driver.disconnect()

class SecureMessageProducer(Producer):
    '''Уточненная абстракция'''

    def send(self, message):
        self.driver.connect()
        encrypted_message = self._encrypt_message(message)
        self.driver.push(encrypted_message)
        self.driver.disconnect()

    def _encrypt_message(self, message):
        print('Encrypting message')
        return f'#_ecrypted_message_{message}_#'

if __name__ == '__main__':
    message_producer = MessageProducer(RedisDriver())
    message_producer.send('Some message')
    print(100*'=')
    secure_message_producer = SecureMessageProducer(KafkaDriver())
    secure_message_producer.send('Some message x2')