import os


class Settings():

    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY")
    TOKEN_EXPIRY = os.getenv("TOKEN_EXPIRY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET")

    PROJECT_NAME: str = "FirmiFy"

    # Agregar el dominio del frontend
    BACKEND_CORS_ORIGINS: list[str] = [""]
    

settings = Settings()