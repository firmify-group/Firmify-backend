import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY")
    TOKEN_EXPIRY: str = os.getenv("TOKEN_EXPIRY", "3600")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    PROJECT_NAME: str = "FirmiFy"
    ACCESS_KEY: str = os.getenv("ACCESS_KEY",)
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    S3_ENDPOINT = str=os.getenv("S3_ENDPOINT")

    cors_origins = os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000")
    BACKEND_CORS_ORIGINS = [origin.strip() for origin in cors_origins.split(",")]

settings = Settings()
