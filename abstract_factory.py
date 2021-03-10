# Позволяет создавать семейства связанных объектов, скрывая информаци о конкретных классах создаваемых объектов
# По цели - Порождающий
# По применимости - Применятеся к объектам

from __future__ import annotations
from abc import abstractmethod, ABC

class Shirt(ABC):
    '''Abs prod 1'''
    @abstractmethod
    def get_size(self):
        pass

class Pants(ABC):
    '''Abs prod 2'''
    @abstractmethod
    def get_size(self):
        pass

class Headdress(ABC):
    '''Abs prod 3'''
    @abstractmethod
    def get_size(self):
        pass

class TShirt(Shirt):
    '''Concrete prod 1 family 1'''
    def get_size(self):
        print(f'{self.__class__.__name__} size XL')

class Jeans(Pants):
    '''Concrete prod 2 family 1'''
    def get_size(self):
        print(f'{self.__class__.__name__} size XL')

class BaseballCap(Headdress):
    '''Concrete prod 3 family 1'''
    def get_size(self):
        print(f'{self.__class__.__name__} size XL')

class ClassicShirt(Shirt):
    '''Concrete prod 1 family 1'''
    def get_size(self):
        print(f'{self.__class__.__name__} size XL')

class ClassicPants(Pants):
    '''Concrete prod 2 family 1'''
    def get_size(self):
        print(f'{self.__class__.__name__} size XL')

class Hat(Headdress):
    '''Concrete prod 3 family 1'''
    def get_size(self):
        print(f'{self.__class__.__name__} size XL')

class ClothingStore(ABC):
    def get_shirt(self) -> Shirt:
        pass
    
    def get_jeans(self) -> Pants:
        pass

    def get_headdress(self) -> Headdress:
        pass

class CasualClothingStore(ClothingStore):
    '''Concrete fabric 1'''
    def get_shirt(self) -> TShirt:
        return TShirt()
    
    def get_jeans(self) -> Jeans:
        return Jeans()

    def get_headdress(self) -> BaseballCap:
        return BaseballCap()

class ClassicClothingStore(ClothingStore):
    '''Concrete fabric 2'''
    def get_shirt(self) -> ClassicShirt:
        return ClassicShirt()
    
    def get_jeans(self) -> ClassicPants:
        return ClassicPants()

    def get_headdress(self) -> Hat:
        return Hat()

def pick_clothes(store: ClothingStore):
    store.get_shirt().get_size()
    store.get_jeans().get_size()
    store.get_headdress().get_size()

if __name__ == '__main__':
    print('Подобрать одежу в магазине повседневной одежды')
    pick_clothes(CasualClothingStore())
    print('Подобрать одежу в магазине классической одежды')
    pick_clothes(ClassicClothingStore())

