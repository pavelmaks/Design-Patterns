# Гарантирует, что у класс будет только один экземпляр
# По цели - Порождающий
# По применимости - Применятеся к объектам

class Singleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

s = Singleton()
s1 = Singleton()
print(s, s1) 

class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class DatabaseConnection(metaclass=SingletonMeta):
    conn_count = 0

    def __init__(self):
        self.conn_count += 1

if __name__ == '__main__':
    d1 = DatabaseConnection()
    d2 = DatabaseConnection() 
    assert hash(d1) == hash(d2)
    print(d1.conn_count, d2.conn_count)