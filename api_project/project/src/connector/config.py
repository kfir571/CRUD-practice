
from dataclasses import dataclass
import requests
import os


@dataclass
class Settings():
    base_url: str = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
    timout_connect: float = os.getenv("TIMEOUT_CONNECT", 2.0)
    timeout_read: float = os.getenv("TIMEOUT_READ", 8.0)
    # session: requests.Session = requests.Session()

def load_settings() -> Settings:
    return Settings()

def get_url(endpoint: str = "") -> str:
    return load_settings().base_url.strip('/') + endpoint
