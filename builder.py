# Цель - создавать сложные объекты пошагово
# По цели - Порождающий
# По применимости - Применятеся к объектам

from enum import Enum

class Cutlery(Enum):
    pass

class Product:
    @property
    def name(self):
        pass

class Sushi(Product):
    @property
    def name(self):
        return 'Sushi'

class Burger(Product):
    @property
    def name(self):
        return 'Burger'

class OrderBuilder:
    def serve(self):
        pass

    def pack(self):
        pass

    def add_cutlery(self, cutlery: Cutlery):
        pass

    def add_toopings(self):
        pass

    def add_gloves(self):
        pass

    def get_order_read(self) -> Product:
        pass

class SushiCutlery(Cutlery):
    FORK = 'FORK'
    STICKS = 'STICKS'

class SushiOrederBuilder(OrderBuilder):

    def serve(self):
        print('Cooking...')

    def pack(self):
        print('Packing...')

    def add_cutlery(self, cutlery: SushiCutlery):
        if cutlery == SushiCutlery.FORK:
            print('Forks are on there way...')
        if cutlery == SushiCutlery.STICKS:
            print('Sticks are on there way...')

    def add_toopings(self):
        print('Adding toppings...')

    def add_gloves(self):
        print('Adding toppings...')

    def get_ready_order(self):
        print('Sushi is ready!')
        return Sushi()

    # e.t.c

class BurgerBuilder(OrderBuilder):
    # all the same as sushi builder
    pass

class Packer:
    '''aka Director'''

    def __init__(self, order_builder: OrderBuilder):
        self.order_builder = order_builder

    def pack_sushi(self, cutlery: SushiCutlery):
        self.order_builder.serve()
        self.order_builder.add_toopings()
        self.order_builder.add_cutlery(cutlery)
        self.order_builder.pack()
        return self.order_builder.get_ready_order()

    def pack_burger(self):
        # all the same
        print('Buger is ready!')

if __name__ == '__main__':
    print('Клиент заказал суши')
    packer = Packer(SushiOrederBuilder())
    # print(packer.order_builder)
    order = packer.pack_sushi(SushiCutlery.STICKS)
