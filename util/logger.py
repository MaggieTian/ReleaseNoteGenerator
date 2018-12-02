#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @File    : logger.py
# @Date    : 2018-11-28
# @Author  : qitian

import logging


# save the log level
format_dict = {
   1: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   2: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   3: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   4: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   5: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
}


class Logger:

    def __init__(self,logname, loglevel, logger):
        '''

        :param logname: the file name that save the log
        :param loglevel: the level of logging
        :param logger: set the logger name
        '''

        self.logger = logging.getLogger(logger)
        self.logger.setLevel(loglevel)

        fh = logging.FileHandler(logname)
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # set formatter
        formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    @staticmethod
    def get_logger():
        logger = Logger(logname='log.txt', loglevel=1, logger="git_logger")
        return logger.logger


if __name__ == '__main__':

    logger = Logger(logname='log.txt', loglevel=1, logger="git_logger").get_logger()