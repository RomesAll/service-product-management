from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path
from pika import URLParameters
import sys, logging

BASE_DIR = Path(__file__).parent.parent.parent
APP_DIR = BASE_DIR / 'app'
sys.path.append(str(BASE_DIR))
sys.path.append(str(APP_DIR))

class Base(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'{BASE_DIR}/.env', extra='ignore')

class RedisSettings(Base):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: SecretStr
    REDIS_USER: str
    REDIS_USER_PASSWORD: SecretStr
    REDIS_DB: int = 0

    @property
    def get_redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

class PostgresSettings(Base):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_MODE: str

    @property
    def get_database_url_sync(self):
        return (f'postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@'
                f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}')

class TelegramSettings(Base):
    TELEGRAM_TOKEN: SecretStr
    TELEGRAM_CHAT_ID: str

    @property
    def get_telegram_url_send_msg(self):
        return f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN.get_secret_value()}/sendMessage"

    @property
    def get_telegram_url_updates_msg(self):
        return f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN.get_secret_value()}/getUpdates"

class RabbitMQSettings(Base):
    RMQ_HOST: str
    RMQ_PORT: int
    RMQ_USER: str
    RMQ_PASS: SecretStr

    @property
    def get_rabbitmq_url(self):
        return URLParameters(f"amqp://{self.RMQ_USER}:{self.RMQ_PASS.get_secret_value()}@{self.RMQ_HOST}:{self.RMQ_PORT}")

class AuthTokenSettings(Base):
    private_key_path: Path = BASE_DIR / 'app' / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'app' / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_exp: int = 36000 # second
    refresh_token_exp: int = 50000 # second

class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    redis: RedisSettings = RedisSettings()
    auth: AuthTokenSettings = AuthTokenSettings()
    logger: logging.Logger = logging.getLogger('app')
    logger_requests: logging.Logger = logging.getLogger('app-request')
    telegram: TelegramSettings = TelegramSettings()

settings = Settings()