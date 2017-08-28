#coding=utf-8
import logging
from contextlib import contextmanager

@contextmanager
def debug_looging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)