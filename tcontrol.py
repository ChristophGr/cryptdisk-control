#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *
import os
import subprocess
import sys
import keychain
from mountwatcher import *
import getpass

from config import *
from logconfig import logger

def save_truecrypt_device(path):
    content = read_json_file(configfile)
    content["volumes"][path] = "truecrypt"
    write_json_file(configfile, content)

def initial_mount(volume, password):
    path = find_unique_dev_path(volume)
    if path == None:
        path = volume
    save_truecrypt_device(path)
    result = mount_volume(path, password)
    if result > 0:
        raise Exception("failed to mount volume")

    keychain.store_password(path, password)

def main():
    if not os.path.exists(configfile):
        logger.info("creating configfile {}".format(configfile))
        write_json_file(configfile, dict(truecryptvolumes = []))
    reffile = sys.argv[1]
    password = getpass.getpass()
    initial_mount(reffile, password)
    logger.info(find_unique_dev_path(reffile))

if __name__ == '__main__':
    main()