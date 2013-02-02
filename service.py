#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from utils import *
from logconfig import logger
import os
import subprocess
import sys
import keychain
#import gkeyringimpl
import plaintextkeychain
import json

from mountwatcher import *

from config import *

def ask_password_and_mount(path):
    print("NYI")
    raise Exception("NYI")

class TruecryptFileHandler:
    def on_create(self, path):
        password = keychain.get_password(path)
        if password == None:
            ask_password_and_mount(path)
        if mount_volume(path, password):
            logger.info("mounted path %s" % path)
        else:
            ask_password_and_mount(path)

    def on_delete(self, path):
        subprocess.call(["truecrypt", "-d", path])
        logger.info("deleted path %s " % path)

def main():
    if not os.path.exists(configfile):
        write_json_file(configfile, dict(volumes = dict()))

    known = read_json_file(configfile)["volumes"]
    truecryptvolumes = [ x.encode('ascii','replace') for (x,y) in known.iteritems() if y == "truecrypt" ]
    for f in truecryptvolumes:
        if len(f) > 0:
            start_watching_disk_file(f, TruecryptFileHandler())
            print f
    logger.info("initialized")

if __name__ == '__main__':
    main()
