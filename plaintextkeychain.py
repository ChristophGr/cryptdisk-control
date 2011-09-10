#!/usr/bin/env python
# -*- coding: utf-8 -*-

from keychain import *
from utils import *
from logconfig import logger

class PlaintextKeychain(Keychain):
    def __init__(self, path):
        if not os.path.exists(path):
            write_json_file(path, dict())
        self.path = path

    def store_password(self, volume, password):
        logger.info("storing password for volume %s as plain text: %s" % (volume, password))
        passwords = read_json_file(self.path)
        logger.debug("just read %s" % self.path)
        passwords[volume] = password
        write_json_file(self.path, passwords)

    def get_password(self, volume):
        passwords = read_json_file(self.path)
        if volume not in passwords:
            return None
        return passwords[volume].encode('ascii','replace')

