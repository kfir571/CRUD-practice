import logging

def setup_logging(file_name : str = "get_save_proj.log", level: int = logging.WARNING):
    logger = logging.basicConfig(
        filename=file_name,
        filemode="a",
        level= level,
        format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)s',
    )