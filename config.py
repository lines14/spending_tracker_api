import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    CURRENCY_RATES_URL: str
    REDIS_HOST: str
    REDIS_ROOT_PASSWORD: str
    REDIS_PORT: int
    DB_NAME: str
    DB_ROOT_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    TOKEN_TTL: int
    ENCODE_ALGORITHM: str
    FRONT_URL: str

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

    @property
    def DB_URL_ASYNC(self) -> str:
        return (f"mysql+aiomysql://root:{self.DB_ROOT_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
    
    @property
    def DB_URL_SYNC(self) -> str:
        return (f"mysql+pymysql://root:{self.DB_ROOT_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
    
    @property
    def REDIS_URL(self) -> str:
        return (f"redis://:{self.REDIS_ROOT_PASSWORD}@"
                f"{self.REDIS_HOST}:{self.REDIS_PORT}/0")
    
    @property
    def PROTECTED_PATHS(self) -> list:
        return [
            "/user", 
            "/greetings", 
            "/purchase", 
            "/bank_account"
        ]