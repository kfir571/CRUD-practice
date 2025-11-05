
from dataclasses import dataclass
import os


@dataclass
class Settings():
    base_url: str = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
    timout_connect: float = os.getenv("TIMEOUT_CONNECT", 2.0)
    timeout_read: float = os.getenv("TIMEOUT_READ", 8.0)

def load_settings() -> Settings:
    return Settings()
