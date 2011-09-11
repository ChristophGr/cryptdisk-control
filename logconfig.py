#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import subprocess

logging.basicConfig(format='%(asctime)-15s %(module)s:%(lineno)s %(levelname)s %(message)s')
logger = logging.getLogger("crypt-control")
logger.setLevel("DEBUG")

#if(subprocess.call("tty -s") > 0):
if True:
    hdlr = logging.FileHandler('crypt-control.log')
    formatter = logging.Formatter('%(asctime)-15s %(module)s:%(lineno)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)


if __name__ == "__main__":
    logger.info("bla")