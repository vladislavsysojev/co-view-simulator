#!/usr/bin/env python
import datetime
import logging
import os
from os import getenv as os_getenv

HOSTNAME = os_getenv("HOSTNAME", "host")


# fmt_pattern = '{"time":"%(asctime)s.%(msecs)03dZ", ' \
#               '"loglevel":"%(levelname)s", "hostname":"' \
#               + HOSTNAME + '", "message":%(message)s}'
# date_fmt_pattern = '%Y-%m-%dT%H:%M:%S'
# handler = logging.FileHandler("Logs/automation_log")  # create new logging handler
# handler.setLevel("INFO")  # set level
# formatter = logging.Formatter(fmt=fmt_pattern, datefmt=date_fmt_pattern)
# # set log and date format
# handler.setFormatter(formatter)
# LOGGER = logging.getLogger("automation_logger")  # set the formatter to handler
# LOGGER.addHandler(handler)
date_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


def create_log_dir(name):
    full_path = os.path.join(os.getcwd(), name)
    if not os.path.isdir(full_path):
        os.mkdir(full_path)


class ILog:
    def __init__(self, className=__name__):
        create_log_dir("Logs/")
        create_log_dir("Logs/")
        create_log_dir("Logs/info_crit_war_err")
        create_log_dir("Logs/info_debug")
        self.logger = logging.getLogger(className)
        self.logger.setLevel(logging.DEBUG)


        # logging format
        date_fmt_pattern = '%Y-%m-%dT%H:%M:%S'
        file_fmt = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s: %(message)s'
        con_fmt = '%(asctime)s %(message)s'

        # create a file handler
        handler_info = logging.FileHandler("Logs/info_crit_war_err/test_{0}.log".format(date_time))
        handler_info.setLevel(logging.INFO)
        handler_debug = logging.FileHandler("Logs/info_debug/prog_debug_{0}.log".format(date_time))
        handler_debug.setLevel(logging.DEBUG)

        # create console handler
        handler_console_info = logging.StreamHandler()
        handler_console_info.setLevel(logging.INFO)

        # create a logging format
        file_formatter = logging.Formatter(file_fmt, datefmt=date_fmt_pattern)
        handler_info.setFormatter(file_formatter)
        handler_debug.setFormatter(file_formatter)
        con_formatter = logging.Formatter(con_fmt, datefmt=date_fmt_pattern)
        handler_console_info.setFormatter(con_formatter)

        # handler adding
        self.logger.addHandler(handler_info)
        self.logger.addHandler(handler_console_info)
        self.logger.addHandler(handler_debug)

        self.info = self.logger.info
        self.warning = self.logger.warning
        self.critical = self.logger.critical
        self.debug = self.logger.debug
        self.error = self.logger.error
        self.exception = self.logger.exception
