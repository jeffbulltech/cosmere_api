import os

# You can use environment variables for flexibility, or hardcode for local dev
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://jbthejedi@localhost/cosmere"
)