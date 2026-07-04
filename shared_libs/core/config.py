import os

class ConfigService:
    @staticmethod
    def get_db_url() -> str:
        user = os.environ.get("POSTGRES_USER", "acb_user")
        pwd = os.environ.get("POSTGRES_PASSWORD", "acb_pass")
        host = os.environ.get("POSTGRES_HOST", "postgres")
        port = os.environ.get("POSTGRES_PORT", "5432")
        db = os.environ.get("POSTGRES_DB", "acb_db")
        return f"postgresql://{user}:{pwd}@{host}:{port}/{db}"
    
    @staticmethod
    def get_postgres_host() -> str: return os.environ.get("POSTGRES_HOST", "localhost")
    @staticmethod
    def get_postgres_port() -> str: return os.environ.get("POSTGRES_PORT", "5432")
    @staticmethod
    def get_postgres_db() -> str: return os.environ.get("POSTGRES_DB", "acb_db")
    @staticmethod
    def get_postgres_user() -> str: return os.environ.get("POSTGRES_USER", "acb_user")
    @staticmethod
    def get_postgres_password() -> str: return os.environ.get("POSTGRES_PASSWORD", "acb_pass")

    @staticmethod
    def get_jwt_secret() -> str:
        return os.environ.get("JWT_SECRET", "super-secret-default-key-for-sprint6-only")

    @staticmethod
    def get_jwt_algorithm() -> str:
        return "HS256"

    @staticmethod
    def get_jwt_access_expire_minutes() -> int:
        return 15

    @staticmethod
    def get_jwt_refresh_expire_days() -> int:
        return 7
        
    @staticmethod
    def get_gemini_api_key() -> str:
        return os.environ.get("GEMINI_API_KEY", "")
        
    @staticmethod
    def get_registry_path() -> str:
        return os.environ.get("REGISTRY_PATH", "/app/workflows/16-registry")
        
class SecretProvider:
    @staticmethod
    def get_secret(key: str) -> str:
        return os.environ.get(key, "")
