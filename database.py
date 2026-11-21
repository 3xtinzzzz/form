import psycopg2

from config import DB_CONFIG


def connect_db():
    """Создаёт подключение к PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)


def authorize_user(login, password):
    """
    Проверяет логин и пароль в таблице users.
    Возвращает словарь с данными пользователя или None,
    если пользователь не найден либо пароль неверный.
    """
    connection = connect_db()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, login, name, age, email
                FROM users
                WHERE login = %s AND password = %s
                """,
                (login, password),
            )
            row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "login": row[1],
            "name": row[2],
            "age": row[3],
            "email": row[4],
        }
    finally:
        connection.close()
