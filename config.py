import secret

DB_ENGINE = 'postgresql+asyncpg'
DB_NAME = secret.DB_NAME
DB_USER = secret.DB_USER
DB_PASSWORD = secret.DB_PASSWORD
DB_HOST = secret.DB_HOST
DB_PORT = 5432
DB_URL = f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
