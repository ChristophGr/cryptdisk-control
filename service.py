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

def try_get_password():
    if hasX():
        from xutils import get_password_from_dialog
        logger.info("get password from dialog")
        password = get_password_from_dialog()
        logger.info("read %s from dialog" % password)
        return password

def ask_password_and_mount(path):
    password = ""
    logger.info("ask_password_and_mount:")
    while password != None:
        password = try_get_password()
        if mount_volume(path, password):
            keychain.store_password(path, password)
            break

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

class LuksHandler:
    def on_create(self, path):
        password = keychain.get_password(path)
        self.name = mount_luks_volume(path, password)
    def on_delete(self, path):
        luksclosecommand = ["crypt-umount.sh", name]
        subprocess.call(luksclosecommand)

def main():
    if not os.path.exists(configfile):
        write_json_file(configfile, dict(volumes = dict()))

    known = read_json_file(configfile)["volumes"]
    truecryptvolumes = [ x.encode('ascii','replace') for (x,y) in known.iteritems() if y == "truecrypt" ]
    for f in truecryptvolumes:
        if len(f) > 0:
            start_watching_disk_file(f, TruecryptFileHandler())
            print f

    luksvolumes = [ x.encode('ascii','replace') for (x,y) in known.iteritems() if y == "luks" ]

    logger.info("initialized")

if __name__ == '__main__':
    main()
