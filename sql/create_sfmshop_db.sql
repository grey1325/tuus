-- Таблица пользователей
CREATE TABLE users (
 id SERIAL PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 email VARCHAR(100) UNIQUE NOT NULL,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица товаров
CREATE TABLE products (
 id SERIAL PRIMARY KEY,
 name VARCHAR(200) NOT NULL,
 price DECIMAL(10, 2) NOT NULL,
 quantity INTEGER DEFAULT 0,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица заказов
CREATE TABLE orders (
 id SERIAL PRIMARY KEY,
 user_id INTEGER REFERENCES users(id),
 total DECIMAL(10, 2) NOT NULL,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица товаров в заказах
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price DECIMAL(10, 2) NOT NULL
);

-- Таблица отзывов
CREATE TABLE reviews (
 id SERIAL PRIMARY KEY,
 product_id INTEGER REFERENCES products(id),
 user_id INTEGER REFERENCES users(id),
 review_text TEXT,
 rating INTEGER CHECK (rating >= 1 AND rating <= 5),
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Денормализация может помочь в следующих случаях:
--Поле user_name хранит имя пользователя на момент создания заказа
-- и не обновляется при изменении имени пользователя, что является осознанным компромиссом.
CREATE TABLE orders (
 id SERIAL PRIMARY KEY,
 user_id INTEGER REFERENCES users(id),
 user_name VARCHAR(100), -- Денормализация: дублирование для производительности
 total DECIMAL(10, 2)
);
-- Для ускорения отчетов по отзывам добавлено поле reviews.product_name,
-- что позволяет избежать JOIN с таблицей products.
-- Триггер AFTER UPDATE на products обновляет значение при изменении имени товара,
-- поддерживая согласованность данных.
CREATE TABLE reviews (
 id SERIAL PRIMARY KEY,
 product_id INTEGER REFERENCES products(id),
 product_name VARCHAR(200), -- Денормализация: для ускорения отчетов
 user_id INTEGER REFERENCES users(id),
 review_text TEXT,
 rating INTEGER CHECK (rating >= 1 AND rating <= 5),
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Обновление денормализованного поля при изменении товара
CREATE OR REPLACE FUNCTION update_review_product_name()
RETURNS TRIGGER AS $$
BEGIN
 UPDATE reviews SET product_name = NEW.name WHERE product_id = NEW.id;
 RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_reviews_on_product_change
AFTER UPDATE ON products
FOR EACH ROW
WHEN (OLD.name IS DISTINCT FROM NEW.name)
EXECUTE FUNCTION update_review_product_name();

-- Для ускорения расчёта суммы заказов пользователя добавлено поле users.total_spent.
-- Для поддержания актуальности данных реализованы триггеры:
-- - AFTER INSERT — увеличивает сумму при создании заказа
-- - AFTER UPDATE — корректирует сумму на разницу между новым и старым значением
-- - AFTER DELETE — уменьшает сумму при удалении заказа
-- Таким образом исключается необходимость выполнения агрегатной функции SUM,
-- что значительно ускоряет выполнение отчетных запросов.
-- Целостность данных обеспечивается за счет обработки всех типов изменений
-- (INSERT, UPDATE, DELETE), что предотвращает рассинхронизацию денормализованных данных.
CREATE TABLE users (
 id SERIAL PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 email VARCHAR(100) UNIQUE NOT NULL,
 total_spent DECIMAL (10, 2) DEFAULT 0 --ускорение поиска суммы заказов пользователя
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- создаем триггер
CREATE OR REPLACE FUNCTION insert_user_total()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE users
    SET total_spent = total_spent + NEW.total
    WHERE id = NEW.user_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_insert_user_total
AFTER INSERT ON orders
FOR EACH ROW
EXECUTE FUNCTION insert_user_total();

CREATE OR REPLACE FUNCTION update_user_total()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.user_id = OLD.user_id THEN
        UPDATE users
        SET total_spent = total_spent + (NEW.total - OLD.total)
        WHERE id = NEW.user_id;
    ELSE
        UPDATE users
        SET total_spent = total_spent - OLD.total
        WHERE id = OLD.user_id;

        UPDATE users
        SET total_spent = total_spent + NEW.total
        WHERE id = NEW.user_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_user_total
AFTER UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION update_user_total();

CREATE OR REPLACE FUNCTION delete_user_total()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE users
    SET total_spent = total_spent - OLD.total
    WHERE id = OLD.user_id;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_delete_user_total
AFTER DELETE ON orders
FOR EACH ROW
EXECUTE FUNCTION delete_user_total();

--Для ускорения аналитических запросов (например, получения количества проданных товаров)
--было добавлено денормализованное поле products.total_sold.
--Для поддержания его актуальности реализованы триггеры:
-- - AFTER INSERT — увеличивает значение при добавлении позиции заказа
-- - AFTER UPDATE — корректирует значение при изменении количества
-- - AFTER DELETE — уменьшает значение при удалении позиции
-- Это позволяет избежать выполнения агрегатных функций (SUM), что значительно ускоряет отчёты.
CREATE TABLE products (
 id SERIAL PRIMARY KEY,
 name VARCHAR(200) NOT NULL,
 price DECIMAL(10, 2) NOT NULL,
 quantity INTEGER DEFAULT 0,
 total_sold INTEGER DEFAULT 0 --ускорение поиска количества проданного товара
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
--создаем триггер
CREATE OR REPLACE FUNCTION insert_product_total()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE products
    SET total_sold = total_sold + NEW.quantity
    WHERE id = NEW.product_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_insert_product_total
AFTER INSERT ON order_items
FOR EACH ROW
EXECUTE FUNCTION insert_product_total();

CREATE OR REPLACE FUNCTION update_product_total()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.product_id = OLD.product_id THEN
        UPDATE products
        SET total_sold = total_sold + (NEW.quantity - OLD.quantity)
        WHERE id = NEW.product_id;
    ELSE
        UPDATE products
        SET total_sold = total_sold - OLD.quantity
        WHERE id = OLD.product_id;

        UPDATE products
        SET total_sold = total_sold + NEW.quantity
        WHERE id = NEW.product_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_product_total
AFTER UPDATE ON order_items
FOR EACH ROW
EXECUTE FUNCTION update_product_total();

CREATE OR REPLACE FUNCTION delete_product_total()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE products
    SET total_sold = total_sold - OLD.quantity
    WHERE id = OLD.product_id;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_delete_product_total
AFTER DELETE ON order_items
FOR EACH ROW
EXECUTE FUNCTION delete_product_total();

-- Целостность данных обеспечивается с помощью триггеров,
-- которые обрабатывают все операции изменения данных (INSERT, UPDATE, DELETE).

-- Дополнительно учитываются сложные случаи:
-- - изменение user_id → перенос суммы между пользователями
-- - изменение product_id → перенос количества между товарами
-- Это гарантирует согласованность денормализованных данных с основными таблицами.

-- Преимущества:
-- - ускорение SELECT-запросов
-- - уменьшение количества JOIN
-- - отказ от агрегатных функций (SUM, COUNT)

-- Недостатки:
-- - дублирование данных
-- - усложнение логики обновления
-- - увеличение нагрузки на INSERT/UPDATE/DELETE
-- - риск рассинхронизации при ошибках в триггерах
-- Компромисс:
-- денормализация оправдана для часто выполняемых отчетов, но требует дополнительной логики для поддержания целостности.