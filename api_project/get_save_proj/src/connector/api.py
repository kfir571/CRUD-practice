import requests

from functools import lru_cache
import openai
from openai import OpenAI
import json
import logging
from json import dumps


class ProcessingError(Exception):
    pass

@lru_cache(maxsize=1)
def get_session():
    s = requests.Session()
    s.headers = {'Content-Type': 'application/json'}
    return s

# def get_endpoint(endpoint: str) -> list[dict]:
#     url = 
#     respons = get_session()
        
    
def iner_qery(q: str):
    client = OpenAI()
    logger = logging.getLogger(__name__)

    try:
        response = client.responses.create(
            model="gpt-5",
            input="i give u messge and i wont thet u retrne me the output at json format my messge is: retrn me massge at default json format, thet hve 3 keys: messge, time, scor. retern 3 messges, and the messge be abute this subject:" + q
        )
        logger.info("responce recive")

    except openai.OpenAIError as e:
        logger.exception("OpenAI request failed")
        raise ProcessingError("OpenAI request failed") from e

    try:
        data = json.loads(response.output_text)

    except json.JSONDecodeError as e:
        logger.error("Bad JSON from model", exc_info=True) 
        raise ProcessingError("Bad JSON from model") from e

    return data



def reapit(q: str, n: int = 3):
    logger = logging.getLogger(__name__)
    data = None

    for i in range(n):
        try:
            data = iner_qery(q)
            break
        except Exception as e:
            logger.error("repit file at try:" + str(i + 1))
            continue
    
    return data if data else None


def query(q: str):
    return reapit(q)