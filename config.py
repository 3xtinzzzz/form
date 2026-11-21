import os

# Пароль задаётся в переменной окружения POSTGRES_PASSWORD.
# Не сохраняйте настоящий пароль PostgreSQL в GitHub.

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "database": os.getenv("POSTGRES_DB", "form"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
}
