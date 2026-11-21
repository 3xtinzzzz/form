-- ВНИМАНИЕ: DROP TABLE удалит старую таблицу users и все её данные.
-- Если данные нужно сохранить, уберите DROP TABLE и измените существующую таблицу отдельно.

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    role VARCHAR(30) NOT NULL DEFAULT 'user',
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- Пример пользователя для проверки входа:
-- Логин: admin
-- Пароль: 12345

INSERT INTO users (role, username, password, name)
VALUES ('admin', 'admin', '12345', 'Администратор');
