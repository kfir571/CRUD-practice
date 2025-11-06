import logging

def setup_logging(file_name : str = "api_connector.log", level: int = logging.INFO) -> None:
    logger = logging.basicConfig(
        filename= file_name,
        level= level,
        format= "%(asctime)s | %(levelname)s | %(name)s | %(message)s | %(lineno)d",
        filemode= "a",
    )