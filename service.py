#!/usr/bin/env python
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

class TruecryptFileHandler:
    def on_create(self, path):
        password = keychain.get_password(path)
        if password == None:
            logger.warn("password not found in keyring")
            return
        mount_volume(path, password)
        logger.info("mounted path %s" % path)
    def on_delete(self, path):
        subprocess.call(["truecrypt", "-d", path])
        logger.info("deleted path %s " % path)

def main():
    if not os.path.exists(configfile):
        write_json_file(configfile, dict(truecryptvolumes = []))

    known = read_json_file(configfile)["volumes"]
    truecryptvolumes = [ x.encode('ascii','replace') for (x,y) in known.iteritems() if y == "truecrypt" ]
    for f in truecryptvolumes:
        if len(f) > 0:
            start_watching_disk_file(f, TruecryptFileHandler())
            print f
    logger.info("initialized")

if __name__ == '__main__':
    main()
