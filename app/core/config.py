from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from redis import Redis

class Base(BaseSettings):
    model_config = SettingsConfigDict(env_file='../../.env', extra='ignore')

class RedisSettings(Base):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: SecretStr
    REDIS_USER: str
    REDIS_USER_PASSWORD: SecretStr
    REDIS_DB: int = 0

    @property
    def get_redis_url(self):
        return Redis.from_url(f'redis://{self.REDIS_USER}:{self.REDIS_PASSWORD.get_secret_value()}@'
                              f'{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}')

class PostgresSettings(Base):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_PORT: int

    @property
    def get_database_url_sync(self):
        return (f'postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@'
                f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}')

class RabbitMQSettings(Base):
    RMQ_HOST: str
    RMQ_PORT: int
    RMQ_USER: str
    RMQ_PASS: SecretStr

    @property
    def get_rabbitmq_url(self):
        return (f'amqp://{self.RMQ_USER}:{self.RMQ_PASS.get_secret_value()}@'
                f'{self.RMQ_HOST}:{self.RMQ_PORT}')

class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    redis: RedisSettings = RedisSettings()

settings = Settings()