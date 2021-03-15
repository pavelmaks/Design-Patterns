# Определяет структуру алгоритма, перекладывая ответственность за некоторые его шаги на подклассы
# По цели - Поведенческий
# По применимости - Применятеся к классам

from abc import ABC, abstractmethod

class Scales(ABC):
    '''Абстрактный класс'''

    def get_weight(self):
        self.before_connect()
        self.connect()
        self.after_connect()
        raw_data = self.read_raw_data()
        weight = self.process_raw_data(raw_data)
        self.before_disconncect()
        self.disconnect()
        self.after_disconnect()
        return weight

    def before_connect(self):
        pass

    @abstractmethod
    def connect(self):
        pass

    def after_connect(self):
        pass

    @abstractmethod
    def read_raw_data(self):
        pass

    def process_raw_data(self, data):
        '''Обязательный шаг алгоритма'''
        return data

    def before_disconncect(self):
        pass

    @abstractmethod    
    def disconnect(self):
        pass

    def after_disconnect(self):
        pass

class ScalesModelA(Scales):
    '''Concrete class'''

    def connect(self):
        print('ScalesModelA is connecting through ORM')

    def disconnect(self):
        print('ScalesModelA is disconnecting')

    def before_connect(self):
        print('ScalesModelA is preparing to connect')

    def read_raw_data(self):
        return 100

class ScalesModelX(Scales):
    '''Concrete class'''

    def connect(self):
        print('ScalesModelX is connecting through ORM')

    def disconnect(self):
        print('ScalesModelX is disconnecting')

    def read_raw_data(self):
        return 100

    def process_raw_data(self, data):
        return 0.001 * data

    def after_disconnect(self):
        print('ScalesModelX is shutting down port')
        

if __name__ == '__main__':
    scales_model_a = ScalesModelA()
    weight = scales_model_a.get_weight()
    print(f'ScalesModelA {weight}')
    scales_model_x = ScalesModelX()
    weight = scales_model_x.get_weight()
    print(f'ScalesModelX {weight}')