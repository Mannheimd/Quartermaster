#!/usr/bin/env python

from collections import OrderedDict
import logging

levels = OrderedDict((lvl, getattr(logging, lvl.upper()))
                     for lvl in ('critical', 'error', 'warning', 'info', 'debug'))


def log_file(name, mode='a', verbosity=levels['debug']):
        fh = logging.FileHandler(name, mode=mode)
        fh.setLevel(verbosity)
        return fh


def logger(verbosity=levels['error'], log_file=None):
    """Create a logger which streams to the console, and optionally a file."""

    # create/get logger for this instance
    logger = logging.getLogger(__name__)
    logger.setLevel(levels['debug'])
    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # with stream (console) handle
    ch = logging.StreamHandler()
    ch.setLevel(verbosity)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # optionally with file handle
    if log_file:
        log_file.setFormatter(fmt)
        logger.addHandler(log_file)

    return logger
