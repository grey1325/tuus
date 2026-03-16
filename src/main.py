#
# Основый Python
# raw_name_1 = "ИВАН"
# raw_name_2 = "мария"
# raw_name_3 = "пЕТР"
#
# print(raw_name_1.capitalize())
# print(raw_name_2.capitalize())
# print(raw_name_3.capitalize())
#
# price = "1999"
# result = "от " + price + " руб."
# print(result)
from itertools import product

from tomlkit import value

# name_1 = "  ИВАН  "
# name_2 = "мария"
# name_3 = "  пЕТР  "
# name_4 = "АННА"
# name_5 = "  олег  "
#
# other_name_1 = name_1.strip()
# other_name_3 = name_3.strip()
# other_name_5 = name_5.strip()
#
# print(other_name_1.capitalize())
# print(name_2.capitalize())
# print(other_name_3.capitalize())
# print(name_4.capitalize())
# print(other_name_5.capitalize())

# price_per_item = 1500.0
# quantity = 3
# discount = 0.1  # 10% скидка
#
# total_price = price_per_item * quantity * (1 - discount)
# print(round(total_price, 2))


# # Заказ 1: с обычной скидкой
# order_1_price = 2000.0
# order_1_quantity = 2
# order_1_discount = 0.15
#
# original_price_1 = order_1_price * order_1_quantity
# discount_amount_1 = original_price_1 * order_1_discount
# total_price_1 = original_price_1 - discount_amount_1
#
# print("Исходная цена " + str(original_price_1) + " руб.")
# print("Размер скидки " + str(discount_amount_1) + " руб.")
# print("Итоговая стоимость " + str(round(total_price_1, 2)) + " руб.")
#
#
# # Заказ 2: без скидки
# order_2_price = 3000.0
# order_2_quantity = 1
# order_2_discount = 0.0
#
# original_price_2 = order_2_price * order_2_quantity
# discount_amount_2 = original_price_2 * order_2_discount
# total_price_2 = original_price_2 - discount_amount_2
#
# print("Исходная цена " + str(original_price_2) + " руб.")
# print("Размер скидки " + str(discount_amount_2) + " руб.")
# print("Итоговая стоимость " + str(round(total_price_2, 2)) + " руб.")
#
# # Заказ 3: с большой суммой
# order_3_price = 5000.0
# order_3_quantity = 3
# order_3_discount = 0.2
#
# original_price_3 = order_3_price * order_3_quantity
# discount_amount_3 = original_price_3 * order_3_discount
# total_price_3 = original_price_3 - discount_amount_3
#
# print("Исходная цена " + str(original_price_3) + " руб.")
# print("Размер скидки " + str(discount_amount_3) + " руб.")
# print("Итоговая стоимость " + str(round(total_price_3, 2)) + " руб.")

# order_total = 6000
#
# if order_total > 10000:
#     discount_rate = 15
#     print(f"Размер скидки {float(discount_rate)} %")
# elif order_total > 5000:
#     discount_rate = 10
#     print(f"Размер скидки {float(discount_rate)} %")
# else:
#     discount_rate = 5
#     print(f"Размер скидки {float(discount_rate)} %")

# order_total = 6000
# print(f"Исходная сумма: {order_total} руб.")
#
# if order_total < 0:
#     print("Ошибка! Сумма должна быть больше нуля!")
# elif order_total > 10000:
#     discount_rate = 0.15
#     discount_amount = order_total * discount_rate
#     final_price = order_total - discount_amount
#     print(f"Размер скидки: {discount_rate * 100}%")
#     print(f"Размер скидки: {discount_amount} руб.")
#     print(f"Итоговая стоимость: {round(final_price, 2)}, руб.")
# elif order_total > 5000:
#     discount_rate = 0.10
#     discount_amount = order_total * discount_rate
#     final_price = order_total - discount_amount
#     print(f"Размер скидки: {discount_rate * 100}%")
#     print(f"Размер скидки: {discount_amount} руб.")
#     print(f"Итоговая стоимость: {round(final_price, 2)}, руб.")
# else:
#     discount_rate = 0.05
#     discount_amount = order_total * discount_rate
#     final_price = order_total - discount_amount
#     print(f"Размер скидки: {discount_rate * 100}%")
#     print(f"Размер скидки: {discount_amount} руб.")
#     print(f"Итоговая стоимость: {round(final_price, 2)}, руб.")


# price_1 = 500
# price_2 = 1500
# price_3 = 800
# price_4 = 2000
# price_5 = 1200
# count = 0
# max_order = 0
# max_price = 0
# print("Товары с ценой больше 1000:")
#
# for i in range(1, 6):
#     if i == 1:
#         order_total = price_1
#     elif i == 2:
#         order_total = price_2
#     elif i == 3:
#         order_total = price_3
#     elif i == 4:
#         order_total = price_4
#     else:
#         order_total = price_5
#
#
#     if order_total > 1000:
#         count += 1
#         print(f"Товар {i}: {order_total} руб.")
#
#         if order_total > max_price:
#                 max_price = order_total
#                 max_order = i
#
# if count == 0:
#     print("Товар не найден")
#
# print(f"Количество товаров с ценой больше 1000: {count}")
# print(f"Товар с максимальной ценой: Товар {max_order}, цена {max_price} руб.")


# prices = [1500, 2300, 890, 4500, 1200]
# prices.sort(reverse=True)
# print(f"Отсортированные цены: {prices}")
# print(f"Максимальная цена: {max(prices)}")
# print(f"Минимальная цена: {min(prices)}")

# cart = []
# max_price = 0
# best_item = None
#
#
# cart.append(['Ноутбук', 50000])
# cart.append(['Мышь', 1500])
# cart.append(['Клавиатура', 3000])
# print(f"Корзина после добавления товаров: {cart}")
# cart.remove(['Мышь', 1500])
# print(f"Корзина после удаления: {cart}")
# cart.sort(reverse=True, key=lambda x: x[1])
# print(f"Корзина после сортировки: {cart}")
#
# if len(cart) == 0:
#     print("Ваша корзина пуста!")
# else:
#     for item, price in cart:
#         if price > max_price:
#             max_price = price
#             best_item = item
# max_item = [best_item, max_price]
# print(f"Самый дорогой товар: {max_item}")



# user = {
#     'ID': {
#         'name': None,
#         'email': None,
#     }
# }
#
# product = {
#     'name': {
#         'price': int,
#         'category': None
#     }
# }
#
#
# user['ID 1'] = user.pop('ID')
# user['ID 1']['name'] = 'Иван'
# user['ID 1']['email'] = 'ivan@test.com'
# print(f"Пользователь добавален: {user.get('ID 1')}")
#
#
# product['Ноутбук'] = product.pop('name')
# product['Ноутбук']['price'] = 50000
# product['Ноутбук']['category'] = 'Компьютер'
# for key, value in product.items():
#     v = next(iter(value.values()))
#     print(f"Цена товара {key}: {v} руб.")
#
#
# visitors = {"user_456", "user_789"}
# visitors.add("user_123")
# if "user_123" in visitors: # возможно это проверка лишняя и достаточно принта ниже, но на всякий случай оставлю
#     print(f"Посетитель user_123 был на сайте: {"user_123" in visitors}")

# location_1 = (55.7558, 37.6173)
# location_2 = (59.9343, 30.3351)
# my_dict = {}
# some_key = 3
#
# my_dict[1] = location_1
# my_dict[2] = location_2
# print(f"Координаты заказа {next(iter(my_dict))} : {my_dict[1]}")
# latitude_1, longitude_1 = location_1
# print(f"Широта: {latitude_1}")
# print(f"Долгота: {longitude_1}")
# if some_key not in my_dict:
#     print(f"Координаты заказа {some_key}: Заказ не найден")

# def calculate_discount(price, discount_percent):
#     final_price = price * (1 - discount_percent)
#     return final_price
#
# result_1 = calculate_discount(1000, 0.10)
# result_2 = calculate_discount(1000, 0.15)
# print(result_1)
# print(result_2)

# def calculate_order_total(price, quantity, discount):
#     final_price = (price * quantity) * (1 - discount)
#     return final_price
#
# def check_stock_availability(stock_quantity, required_quantity):
#     if stock_quantity >= required_quantity:
#         return True
#     else:
#         return False
#
# def format_order_info(order_id, total):
#     return f"Информация о заказе: Заказ #{order_id}, Сумма: {total} руб."
#
# stock_availability = check_stock_availability(10, 3)
# print(f"Товар доступен: {stock_availability}")
# if stock_availability == True:
#     order_total = calculate_order_total(1000, 3, 0.1)
#     order_info = format_order_info(1, order_total)
#     print(order_info)
# else:
#     print("Товара нет в наличии")

# with open("SFMShop/data/products.txt", "r", encoding="utf-8") as file:
#     products = file.readlines()
#
# with open("SFMShop/data/products_with_prices.txt", "w", encoding="utf-8") as new_file:
#     for product in products:
#         product = product.strip()
#         new_line = product + " - 1000 руб.\n"
#         new_file.write(new_line)
#     products = new_file.readlines()
#     for product in products:
#         product = product.strip()
#         print(product)

# count = 0
# total = 0
# new_status = "новый"
# try:
#     with open("SFMShop/data/orders.txt", "r", encoding="utf-8") as file:
#         products = file.readlines()
#     with open("SFMShop/data/processed_orders.txt", "w", encoding="utf-8") as new_file:
#         for product in products:
#             product = product.strip()
#
#             equal_pos_1 = product.find(":")
#             equal_pos_2 = product.find(":", equal_pos_1 + 1)
#
#             if equal_pos_1 != -1 and equal_pos_2 != -1:
#                 key = product[0:equal_pos_1]
#                 value = product[equal_pos_1 + 1: equal_pos_2]
#                 status = product[equal_pos_2 + 1:]
#                 if status == new_status:
#                     total += int(value)
#                     count += 1
#         new_line = "Обработано заказов: " + str(count) + "\n" + "Общая сумма: " + str(total) + " руб.\n"
#         new_file.write(new_line)
#
# except FileNotFoundError:
#     print("Ошибка! Файл не существует")

# from utils.calculations  import calculate_discount, calculate_delivery, calculate_final_price
# from utils.validators import validate_age, validate_email
#
# valid_age = validate_age(20)
# print(f"Возраст валиден: {valid_age}")
# valid_email = validate_email("ivan@test.com")
# print(f"Email валиден: {valid_email}")
# if valid_age and valid_email:
#     discount = calculate_discount(1000, 0.1)
#     delivery = calculate_delivery(5)
#     final_price = calculate_final_price(1000, discount, delivery)
#     print(f"Итоговая стоимость заказа: {final_price} руб.")

# BASE_DISCOUNT = 0.1
# BASE_DELIVERY_COST = 100
#
# def calculate_order_price(price, quantity):
#     subtotal = price * quantity
#     discount = subtotal * BASE_DISCOUNT
#     total = subtotal - discount + BASE_DELIVERY_COST
#     return total
#
# def update_discount(new_discount):
#     global BASE_DISCOUNT
#     BASE_DISCOUNT = new_discount
#
# def func_without_global(price, quantity, new_discount):
#     subtotal = price * quantity
#     discount = subtotal * new_discount
#     total = subtotal - discount + BASE_DELIVERY_COST
#     return total
#
# order_price = calculate_order_price(1000, 2)
# print(f"Стоимость заказа (скидка {int(BASE_DISCOUNT * 100)}%) {order_price}")
# update_discount(0.15)
# order_price = calculate_order_price(1000, 2)
# print(f"Стоимость заказа (скидка {int(BASE_DISCOUNT * 100)}%) {order_price}")
# without_global = func_without_global(1000, 2, 0.3)
# print(f"Стоимость заказа без использования глобальной переменной (скидка 30%) {without_global}")

# def format_product_info(name, price, quantity):
#     return f"Товар: {name}, Цена: {price} руб., Количество: {quantity}"
# product_info = format_product_info("Ноутбук", 50000, 10)
# print(f"Информация о товаре: {product_info}")
# my_list = ["Ноутбук", "Мышь", "Клавиатура"]
# products = ", ".join(my_list)
# print(f"Товары: {products}")

# from datetime import datetime
#
# date = datetime.now()
# print(f"Текущее время: {date.strftime('%Y-%m-%d %H-%M-%S')}")
#
# order_date = datetime(2024, 1, 15, 10, 00, 00)
# delivery_date = datetime(2024, 1, 18, 10, 00, 00)
# print(f"Дата заказа: {order_date}")
# print(f"Дата доставки: {delivery_date}")
# days = delivery_date - order_date
# print(f"Дней до доставки: {days.days}")

# from datetime import datetime, timedelta
#
# def calculate_delivery_date(order_date, delivery_days):
#     return f"Дата доставки: {order_date + timedelta(days=delivery_days)}"
#
# def log_order_creation(order_id, order_time):
#     order_time = order_time.strftime("%Y-%m-%d %H:%M:%S")
#     return f"Заказ #{order_id} создан: {order_time}"
#
# or_date = datetime(2024, 1, 15, 10, 00, 00)
# delivery_date = calculate_delivery_date(or_date, 3)
# print(delivery_date)
# or_time = datetime.now()
# order_creation = log_order_creation(123, or_time)
# print(order_creation)
# import re
#
# def validate_email(email):
#     pattern = r".+@.+\..+"
#     result = re.match(pattern, email)
#     return result is not None
# email_1 = "ivan@example.com"
# email_2 = "invalid"
# email_3 = "test@"
#
# print(f"Email {email_1} валиден: {validate_email(email_1)}")
# print(f"Email {email_2} валиден: {validate_email(email_2)}")
# print(f"Email {email_3} валиден: {validate_email(email_3)}")

# import re
#
# def validate_email_regex(email):
#     pattern = r".+@.+\..+"
#     result = re.match(pattern, email)
#     return result is not None
#
# def validate_phone_regex(phone):
#     pattern = r"\+7[\s\d-]+"
#     result = re.match(pattern, phone)
#     return result is not None
#
# def clean_input(text):
#     pattern = r"[^\w\s.,?-]"
#     result = re.sub(pattern, "", text)
#     return result
#
# def extract_email_from_text(text):
#     pattern = r"\S+@\S+\.\S+"
#     result = re.search(pattern, text)
#     return result.group()

#ООП
# email_1 = "ivan@test.com"
# phone_1 = "+7 999 123-45-67"
# print(f"Email валиден: {validate_email_regex(email_1)}")
# print(f"Телефон валиден: {validate_phone_regex(phone_1)}")
#
# text_1 = "Заказ #123!!! Сумма: 5000 руб."
# print(f"Очищенный текст: {clean_input(text_1)}")
#
# text_2 = "Свяжитесь с нами: support@example.com для помощи"
# print(f"Извлеченный email: {extract_email_from_text(text_2)}")

# from models.user import User
# from models.product import Product
# from models.order import Order
#
# user = User("Иван Иванов", "ivan@test.com")
# product_1 = Product("Ноутбук", 50000, 1)
# product_2 = Product("Мышь", 1500, 2)
# product_1_total_price = product_1.get_total_price()
# product_2_total_price = product_2.get_total_price()
#
# order = Order(user, [product_1, product_2])
#
# print(user.get_info())
# print(f"Общая стоимость заказа: {order.calculate_total()}")

# from models.user import User
# from models.product import Product
# from models.order import Order
#
# user = User("Иван Иванов", "ivan@test.com")
# product_1 = Product("Ноутбук", 50000, 1)
# product_2 = Product("Мышь", 1500, 2)
# product_1_total_price = product_1.get_total_price()
# product_2_total_price = product_2.get_total_price()
#
# order = Order(user, [product_1, product_2])
#
# print(user.get_info())
# print(f"Общая стоимость заказа: {order.calculate_total()}")

# from models.payment import CardPayment, PayPalPayment
#
# payments = [
#     CardPayment(1000, "1234 5678 9012 3456"),
#     PayPalPayment(2000, "user@paypal.com")
# ]
#
# for payment in payments:
#     print(payment.process_payment())

# from models.product import Product
# from models.order import Order
#
# order = Order(1, "Иван", 50000, [])
# products = [
#     Product("Ноутбук", 50000, 10),
#     Product("Мышь", 1500, 20),
#     Product("Клавиатура", 3000, 15)
# ]
# products.sort()
# for product in products:
#     print(product)
# print(order)

# def divide(a, b):
#     try:
#         result = a / b
#     except ZeroDivisionError:
#         return "Нельзя делить на ноль!"
#     except TypeError:
#         return "Ошибка: неверный тип данных!"
#     else:
#         return result

# from models.product import Product
# from models.order import Order
# from models.user import User
#
# fake_product = Product("Наушники", 1000, 1)
# product = Product("Ноутбук", -50000, 10)
# products = [
#     Product("Ноутбук", 50000, 10),
#     Product("Мышь", 1500, 20),
#     Product("Клавиатура", 3000, 15)
# ]
# order = Order(1, "Иван", 0, products)
# order.product_search(fake_product)
# user = User("Иван Иванов", "ivantest.com")

# from models.product import Product
# from models.order import Order
# from src.models.exceptions import NegativePriceError, InsufficientStockError, InvalidOrderError
#
# product_1 = Product("Ноутбук", 50000, 10)
#
# try:
#     product_2 = Product("Клавиатура", -3000, 3)
# except NegativePriceError as e:
#     print("Ошибка валидации:", e)
#
# try:
#     product_1.sell(100)
# except InsufficientStockError as e:
#     print("Ошибка бизнес-логики:", e)
#
# try:
#     order = Order(1, "Иван", 3000, [])
# except InvalidOrderError as e:
#     print("Ошибка бизнес-логики:", e)

# Практическое задание
# def load_orders_from_file(filename):
#     orders_data = []
#     try:
#         with open(filename, "r", encoding="utf-8") as file:
#             for line in file:
#                 line = line.strip()
#                 elements = line.split(":")
#                 if len(elements) == 4:
#                     orders_data.append(line)
#     except FileNotFoundError:
#         print("Ошибка! Файл не существует")
#         return []
#     return orders_data
#
# def calculate_order_total(price, discount_rate):
#     if 0 <= discount_rate <= 1:
#         total = price * (1 - discount_rate)
#         return round(total, 2)
#
#
# def get_discount_by_total(total):
#     if total <= 0:
#         return 0
#     if  total > 10000:
#         discount_rate = 0.15
#     elif total > 5000:
#         discount_rate = 0.10
#     else:
#         discount_rate = 0.05
#     return discount_rate
#
# def process_orders(orders_data):
#     order_list =[]
#     for order in orders_data:
#         try:
#             order_dict = {}
#             parts = order.split(":")
#             parts[1] = int(parts[1])
#             discount = get_discount_by_total(parts[1])
#             total_sum = calculate_order_total(parts[1], discount)
#             order_dict['order_id'] = parts[0]
#             order_dict['total'] = total_sum
#             order_dict['status'] = parts[2]
#             order_dict['user'] = parts[3]
#             order_list.append(order_dict)
#         except ValueError:
#             print("Некорректные данные, должно быть число!")
#     return order_list
#
#
# def analyze_orders(processed_orders):
#     stats = {
#     "total_orders": 0,
#     "total_sum": 0,
#     "by_status": {},
#     "unique_users": set()
#               }
#     for order in processed_orders:
#         total_sum = order['total']
#         by_status = order['status']
#         unique_user = order['user']
#         stats['total_orders'] += 1
#         stats['total_sum'] += total_sum
#         if by_status not in stats['by_status']:
#             stats['by_status'][by_status] = 0
#         stats['by_status'][by_status] += 1
#         stats['unique_users'].add(unique_user)
#     stats['unique_users'] = sorted(list(stats['unique_users']))
#     return stats
#
# from src.models.exceptions import ValidationError, InsufficientStockError, InvalidOrderError, BusinessLogicError
# from src.models.order import Order
# from src.models.payment import CardPayment, PayPalPayment
# from src.models.product import Product
# from src.models.user import User
#
#
# def process_order_system():
#     user = User("Иван", "ivan@test.com")
#     product1 = Product("Ноутбук", 50000, 2)
#     product2 = Product("Мышь", 1500, 3)
#     order = Order(user, [product1, product2])
#     total = order.calculate_total()
#     print(f"Общая стоимость заказа: {total}")
#     payments = [
#         CardPayment(1000, "1234 5678 9012 3456"),
#         PayPalPayment(2000, "test@paypal.com")
#     ]
#     for payment in payments:
#         print(payment.process_payment())
#     sorted_products = sorted([product1, product2])
#     for product in sorted_products:
#         print(product)
#     try:
#         product2.set_price(-1000)
#     except ValidationError as e:
#         print("Ошибка валидации:", e)
#     try:
#         product1.sell(100)
#     except InsufficientStockError as e:
#         print("Ошибка бизнес-логики:", e)
#     try:
#         user.set_email("ivantest.com")
#     except ValidationError as e:
#         print("Ошибка валидации:", e)
#     try:
#         order.add_product("product1")
#     except InvalidOrderError as e:
#         print("Ошибка валидации:", e)
#     try:
#        order2 = Order(user, [])
#     except BusinessLogicError as e:
#         print("Ошибка бизнес-логики:", e)
#
#
# process_order_system()


