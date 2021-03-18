# Позволяет добавлять в программу новые операции, не изменяя классы объектов, надо которыми эти операции могут выполняться
# По цели - Поведенческий
# По применимости - Применятеся к объектам

from abc import ABC, abstractmethod

class MongoConnector:
    def repair_db(self):
        print('Repairing MongoDB')

    def active_connections(self):
        return 10

class FirebirdConnector:
    connection_count = 20

    def backup(self):
        print('Backing up Firebird db')

    def restore(self):
        print('Restoring Firebird db')

    def connections(self):
        return self.connection_count
    
class PostgresSqlConnector:
    def vacuum(self):
        print('Making Vacuum of POstregSQL db')

    def get_connections(self):
        return 30

class Visitable(ABC):
    @abstractmethod
    def accept(self):
        # Можно было бы использовать интерфейс Visitor и его единый метод, он мы усложним
        # и применим механизм "Двойной диспетчеризации" в каждом из классво ниже
        # visitor.visit()
        pass

class MongoConnectorVisitable(MongoConnector, Visitable):
    def accept(self, visitor):
        visitor.visit_mongo(self)

class FirebirdConnectorVisitable(FirebirdConnector, Visitable):
    def accept(self, visitor):
        visitor.visit_firebird(self)

class PostgresSqlConnectorVisitable(PostgresSqlConnector, Visitable):
    def accept(self, visitor):
        visitor.visit_postgresql(self)

class Maintainer:
    def visit_mongo(self, connector):
        connector.repair_db()

    def visit_firebird(self, connector):
        connector.backup()
        connector.restore()
        
    def visit_postgresql(self, connector):
        connector.vacuum()

class ConnectionCounter:
    count = 0   

    def visit_mongo(self, connector):
        mongo_count = connector.active_connections()
        print(f'Mongo has {mongo_count} connections')
        self.count += mongo_count

    def visit_firebird(self, connector):
        firebird_count = connector.connections()
        print(f'Firebird has {firebird_count} connections')
        self.count += firebird_count

    def visit_postgresql(self, connector):
        postgres_count = connector.get_connections()
        print(f'Postgres has {postgres_count} connections')
        self.count += postgres_count

connectors = [
    MongoConnectorVisitable(), 
    FirebirdConnectorVisitable(), 
    PostgresSqlConnectorVisitable()
]

def maintaine_database():
    maintainer = Maintainer()
    for connector in connectors:
        connector.accept(maintainer)

def count_connections():
    connection_counter = ConnectionCounter()
    for connector in connectors:
        connector.accept(connection_counter)
    print(f'Total {connection_counter.count} connections')

if __name__ == '__main__':
    maintaine_database()
    print('='*50)
    count_connections()