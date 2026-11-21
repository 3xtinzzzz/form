import psycopg2

from config import DB_CONFIG


def connect_db():
    """Создаёт подключение к PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)


def authorize_user(username, password):
    """
    Ищет пользователя по логину и паролю.
    Возвращает данные пользователя или None, если совпадение не найдено.
    """
    connection = connect_db()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, role, username, name
                FROM users
                WHERE username = %s AND password = %s
                """,
                (username, password),
            )
            row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "role": row[1],
            "username": row[2],
            "name": row[3],
        }
    finally:
        connection.close()
