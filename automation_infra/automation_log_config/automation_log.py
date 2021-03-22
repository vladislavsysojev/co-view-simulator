import logging
from os import getenv as os_getenv

HOSTNAME = os_getenv("HOSTNAME", "host")
fmt_pattern = '{"time":"%(asctime)s.%(msecs)03dZ", ' \
			  '"loglevel":"%(levelname)s", "hostname":"' \
			  + HOSTNAME + '", "message":%(message)s}'
datefmt_pattern = '%Y-%m-%dT%H:%M:%S'
handler = logging.FileHandler("automation_log")  # create new logging handler
handler.setLevel("INFO")  # set level
formatter = logging.Formatter(fmt=fmt_pattern, datefmt=datefmt_pattern)
# set log and date format
handler.setFormatter(formatter)
LOGGER = logging.getLogger("automation_logger")   # set the formatter to handler
LOGGER.addHandler(handler)