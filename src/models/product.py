from src.models.exceptions import InsufficientStockError, ValidationError


class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def get_total_price(self):
        return self.price * self.quantity

    def sell(self, amount):
        if self.quantity < amount:
            raise InsufficientStockError(
                f"Товара недостаточно. На складе: {self.quantity}, требуется: {amount}"
            )
        self.quantity -= amount

    def set_price(self, price):
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        self.price = price


    def apply_discount(self, percent):
        if 0 < percent < 100:
            discount_amount = (percent * self.price) / 100
            self.price -= discount_amount
        return self.price

    def check_stock(self):
        if self.quantity <= 0:
            raise InsufficientStockError("Товара нет на складе")
        return True

    def update_stock(self, amount):
        self.quantity += amount
        return self.quantity

    def calculate_shipping(self):
        if self.price <= 5000:
            delivery_size = 0.1
            delivery_cost = self.price * delivery_size
            return delivery_cost
        return 0

    def get_category(self):
        return self.name




    def __str__(self):
        return f"Товар: {self.name}, Цена: {self.price} руб., Количество: {self.quantity}"

    def __repr__(self):
        return f"Product({self.name}, {self.price}, {self.quantity})"

    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.name == other.name and self.price == other.price







