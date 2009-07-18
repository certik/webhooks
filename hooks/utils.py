import traceback
import sys
import logging

def log_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logging.info("Exception raised")
            etype, value, tb = sys.exc_info()
            s = "".join(traceback.format_exception(etype, value, tb))
            logging.info(s)
            logging.info("-"*40)
            raise
    return wrapper
