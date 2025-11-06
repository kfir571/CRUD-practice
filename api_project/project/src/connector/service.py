from collections import defaultdict
from json import dumps
from connector.api import get_posts, get_users, get_comments
from connector.config import load_settings, get_url
import pandas as pd # type: ignore

_post: list[dict] | None = None
_users: list[dict] | None = None
_comments: list[dict] | None = None

# def get_url(endpoint: str = "") -> str:
#     return load_settings().strip('/') + endpoint

def _get_comments() -> list[dict]:
    global _comments
    if _comments is None:
        _comments = get_comments(get_url("/comments"))
    
    return _comments

def _get_users() -> list[dict]:
    global _users
    if _users is None:
        # url = os.getenv("BASE_URL", "").rstrip('/') + "/users"
        _users = get_users(get_url("/users"))
    
    return _users


def _get_posts() -> list[dict]:
    global _post
    if _post is None:
        # url = os.getenv("BASE_URL", "").rstrip('/') + "/posts"
        _post = get_posts(get_url("/posts"))
    
    return _post



def get_posts_with_users() -> pd.DataFrame:
    posts = _get_posts().copy()
    users = _get_users()
    user_map = {u["id"]: u["name"] for u in users}

    for p in posts:
        p["userName"] = user_map.get(p["userId"], "unknown")

    return pd.DataFrame(posts)

def get_number_post_per_user() -> dict:
    posts = _get_posts()
    users = _get_users()

    user_map = {u["id"]: u["name"] for u in users}
    res = defaultdict(int)

    for p in posts:
        res[user_map[p["userId"]]] = res[user_map[p["userId"]]] + 1

    return res

def posts_with_keyword(keyword: str) -> list[dict]:
    post = _get_posts()

    return [u["id"] for u in post if keyword in u["body"]]

def get_longest_posts(n: int) -> list[dict]:
    post = sorted(_get_posts(), key=lambda p: len(p["body"]), reverse=True)[:n]
    users = _get_users()
    user_map = {u["id"]: u["name"] for u in users}

    res = [{user_map[p["userId"]]: p["body"]} for p in post]

    return res