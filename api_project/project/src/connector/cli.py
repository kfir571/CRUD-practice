import argparse
from json import dumps
import logging
from dotenv import load_dotenv, find_dotenv
import os

from connector.logging_setup import setup_logging
from connector.api import get_comments, get_posts
from connector.service import get_posts_with_users, get_number_post_per_user, posts_with_keyword, get_longest_posts
from connector.config import load_settings


def main() -> int:

    load_dotenv(find_dotenv())
    settings = load_settings()

    print(settings.base_url)

    setup_logging()
    logger = logging.getLogger("cli.py")

    parser = argparse.ArgumentParser(description='Get Weather of cities')
    parser.add_argument('-c', '--cities', required=True, help='Comma-separated list, e.g. "Tel Aviv,Haifa"')
    args = parser.parse_args()

    cities = [c.strip() for c in args.cities.split(',') if c.strip()]

    print(dumps(get_number_post_per_user(), indent=2))
    print(dumps(posts_with_keyword("nesciunt"), indent=2))
    print(dumps(get_longest_posts(10), indent=2))

    

    logger.info(f"args: {cities}")

    return 0
