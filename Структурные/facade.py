# Позволяет скрыть сложность системы путем сведения всех воможных внешних вызовов к одному объекту, делегирующему их соответствующий объектам системы
# По цели - Структурный
# По применимости - Применятеся к классам

from uuid import uuid4

class UserSignup:
    def __init__(self, login, password):
        self.login = login
        self.password = password

class C1:
    def make_invoice(self, user_id: str, license_price: int):
        print(
            f'C1: Выставление счета клиенту с айди \
            {user_id} на сумму {license_price}'
        )

class AuthServer:
    def signup(self, user_signup: UserSignup) -> str:
        print(f'CA: Регистрируем нового пользователя с логином {user_signup.login}')
        return uuid4()

class NodeServer:
    def create_layer(self) -> str:
        print('CH: Инициализиуем данные для нового слоя')
        return uuid4()

    def link_user_to_layer(self, user_id: str, layer_id: int):
        print(f'CH: Связываем ползователя с id {user_id} со слоем {layer_id}')

class Promo:
    discount = 500

    def verify_promocode(self, promocode: str) -> int:
        print(f'Промо: Выполняем проверку промокода {promocode}')
        return self.discount if promocode.startswith('VALID') else 0

class Billing:
    license_price = 2000

    def get_license_price(self, discount: int) -> int:
        return self.license_price - discount

class RegistrationFacade:
    def __init__(self):
        self.c1 = C1()
        self.auth_server = AuthServer()
        self.node_server = NodeServer()
        self.promo = Promo()
        self.billing = Billing()

    def signup(self, user_signup: UserSignup, promocode=None):
        user_id = self.auth_server.signup(user_signup)
        layer_id = self.node_server.create_layer()
        self.node_server.link_user_to_layer(user_id, layer_id)
        discount = 0
        if promocode:
            discount = self.promo.verify_promocode(promocode)
        license_price = self.billing.get_license_price(discount)
        self.c1.make_invoice(user_id, license_price)

if __name__ == '__main__':
    user_signup = UserSignup('Misha', 'asldkhaslkjd23487')
    registration_facade = RegistrationFacade()
    registration_facade.signup(user_signup, 'VALID_PROMO_1')