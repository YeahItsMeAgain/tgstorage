from app.dependencies.settings import get_settings

settings = get_settings()

DATABASE_URL = f"mysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@mysql:3306/{settings.MYSQL_DATABASE}"
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
