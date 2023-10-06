import logging
from logging import Logger
import sys


def get_logger(name: str) -> Logger:
    logger = Logger(name=name)
    sh = logging.StreamHandler(sys.stdout)
    fh = logging.FileHandler(f"{name}.log")
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%a, %d %b %Y %H:%M:%S",
    )
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger
