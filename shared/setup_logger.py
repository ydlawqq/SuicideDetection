import logging
import sys



def setup_logger(level: int = logging.INFO):
    logging.basicConfig(level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)], force=True, 
        datefmt="%Y-%m-%d %H:%M:%S")


    