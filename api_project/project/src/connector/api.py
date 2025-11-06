
import logging
import os
import requests
from typing import Optional, Any
from functools import lru_cache

from connector.config import get_url
from connector.config import load_settings

logger = logging.getLogger(__name__)

class RemoteTimeout(Exception):
    pass

class RemoteConnectionError(Exception):
    pass

class RemoteHTTPError(Exception):
    pass

class ParseError(Exception):
    pass

class ApiRequestError(Exception):
    def __init__(self, url: str = "", message: str = ""):
        super().__init__(f"API Error for {url}: {message}")
        self.url = url
        self.message = message

@lru_cache(maxsize=1)
def get_session() -> requests.Session:
    session = requests.Session()
    session.headers = {"Content-Type": "application/json"}
    
    return session


def _base_url() -> str:
    base = os.getenv("BASE_URL", "").rstrip("/")
    if not base:
        raise ValueError("BASE_URL is empty or missing (did you load .env?)")
    return base

def _url(path: str) -> str:
    return f"{_base_url()}/{path.lstrip('/')}"

def request_json(
        method: str,
        url: str, 
        params: dict[str, Any] = dict(),
        json: dict[str, Any] = dict(),
        headers: dict[str, str] = dict(),
        timeout: tuple[float, float] = (
            float(os.getenv("TIMEOUT_CONNECT", "2.0")), 
            float(os.getenv("TIMEOUT_RECIVE", "8.0"))
        ),
)-> dict[str, Any]:
        
    try:
        resp = get_session().request(method=method, url=url, params=params, json=json, timeout=timeout)
        # resp.raise_for_status() # is neadd?
    except requests.exceptions.Timeout as e:
        logger.error("TimeOut %s", url)
        raise RemoteTimeout(e) from e
    except requests.exceptions.ConnectionError as e:
        logger.error("ConnectionError %s" , url)
        raise RemoteConnectionError(e) from e
    except Exception as e:
        logger.critical(f"❌ Unexpected error: {e}")
        raise ApiRequestError(url, str(e)) from e

    if not resp.ok:
        preview = resp.text[:200] if resp.text else ""
        logger.error("HTTP %s for %s | %r", resp.status_code, url, preview)
        raise RemoteHTTPError(f"{resp.status_code} {url}")
    
    try:
        data = resp.json()
    except ValueError as e:
        logger.error("JSON parse error from %s", url)
        raise ParseError(e) from e
    
    return data


def retry(
        method: str,
        url: str, 
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: tuple[float, float] = (
                float(os.getenv("TIMEOUT_CONNECT", "2.0")), 
                float(os.getenv("TIMEOUT_RECIVE", "8.0"))
            ),
) -> dict[str, Any] | list[Any]:
    tries_limit = int(os.getenv("TRIES_LIMIT", "3"))
    data = None

    for t in range(tries_limit):
        try:
            data = request_json(method=method, url=url, params=params, json=json, headers=headers, timeout=timeout)
            logger.info("Get json")
            break
        except (RemoteTimeout, RemoteConnectionError, RemoteHTTPError, ParseError) as e:
            logger.warning("Failed to get response after %s retries", t + 1)
            if t == tries_limit - 1:
                logger.error("Failed to get response after multiple retries")
                raise ApiRequestError(url, "Failed to get response after multiple retries")
            
            continue

    return data 

def get_posts(url: str) -> list[dict]:
    return retry("GET", url, timeout= (2.0, 8.0))

def get_users(url: str) -> list[dict]:
    return retry("GET", url, timeout= (2.0, 8.0))

def get_comments(url: str) -> list[dict]:
    # url = os.getenv("BASE_URL", "").rstrip('/') + "/comments"
    return retry("GET", url, timeout= (2.0, 8.0))

def creat_post(url: str, user_id: int, title: str, body: str) -> dict[str, Any]:
    # url = os.getenv("BASE_URL", "").rstrip('/') + "post/" + str(user_id)
    data = {"user_id": user_id, "title": title, "body": body}
    return retry("POST", url=url,json=data, timeout= (2.0, 8.0))

def update_post_put(post_id: int, user_id: int, title: str, body: str) -> dict[str, Any]:
    if post_id <= 0 or user_id <= 0:
        raise ValueError("post_id and user_id must be positive")
    if not title or not body:
        raise ValueError("title and body are required")
    url = get_url("/posts") + str(user_id)
    payload = {"id": post_id, "userId": user_id, "title": title, "body": body}
    return retry("PUT", url, json=payload, timeout=(2.0, 8.0))


def update_post_patch(url: str, post_id: int, **fields) -> dict[str, Any]:
    if post_id <= 0:
        raise ValueError("post_id must be positive")
    if not fields:
        raise ValueError("no fields to update")
    # מותר לעדכן כל תת-קבוצה מתוך: userId/title/body
    allowed = {"userId", "title", "body"}
    unknown = set(fields) - allowed
    if unknown:
        raise ValueError(f"unknown fields for patch: {', '.join(sorted(unknown))}")
    url = _url(f"posts/{post_id}")
    return retry("PATCH", url, json=fields, headers={"Content-Type": "application/json"}, timeout=(2.0, 8.0))


def delete_post(url: str, post_id: int) -> bool:
    if post_id <= 0:
        raise ValueError("post_id must be positive")
    url = _url(f"posts/{post_id}")
    # JSONPlaceholder מחזיר 200/204; ה-retry ירים חריגה אם יש כשל
    retry("DELETE", url, timeout=(2.0, 8.0))
    return True






