"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(1)
        assert product.check_quantity(999)
        assert product.check_quantity(1000)
        assert not product.check_quantity(1001)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        need_q_ty = product.quantity//2
        stock_after = product.quantity - need_q_ty
        product.buy(need_q_ty)
        assert product.quantity == stock_after

        product.buy(stock_after - 1)
        assert product.quantity

        product.buy(1)
        assert not product.quantity

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError) as exception:
            product.buy(product.quantity + 1)
            assert f"Нет нужного кол-ва продукта {product.name}" in exception.value


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product):
        cart.add_product(product, 1)
        assert product in cart.products
        assert cart.products[product] == 1

        cart.add_product(product, 2)
        assert cart.products[product] == 3

    def test_remove_product(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 4)
        assert cart.products[product] == 1

        cart.remove_product(product, 2)
        assert product not in cart.products

    def test_remove_product_full_q_ty(self, cart, product):
        cart.add_product(product, 7)
        cart.remove_product(product, 7)
        assert product not in cart.products

    def test_remove_product_completely(self, cart, product):
        cart.add_product(product, 2)
        cart.remove_product(product)
        assert product not in cart.products

    def test_clear_cart(self, cart, product):
        cart.add_product(product, 5)
        cart.clear()
        assert not cart.products

    def test_get_total_price(self, cart, product):
        cart.add_product(product, 35)
        expected_total = 35 * product.price
        assert cart.get_total_price() == expected_total

    def test_buy_valid_q_ty(self, cart, product):
        cart.add_product(product, 777)
        cart.buy()
        assert product.quantity == 223

    def test_buy_exception(self, product, cart):
        cart.add_product(product, product.quantity + 1)
        with pytest.raises(ValueError) as exception:
            cart.buy()
            assert f"Нет нужного кол-ва продукта {product.name}" in exception.value
