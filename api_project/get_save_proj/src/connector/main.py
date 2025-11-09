from connector.api import query
from connector.logging_setup import setup_logging
from connector.service import loud_data_mg
from dotenv import load_dotenv, find_dotenv
load_dotenv()

def main() -> int:
    setup_logging()
    
    data = query("banna")

    print(data)

    loud_data_mg(data)

    return 0