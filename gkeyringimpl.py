#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk # sets app name
import gnomekeyring
from keychain import *
from utils import *

def getText():
    return get_password_from_dialog('Please enter password for new keyring \"truecrypt\"', "This keyring will contain all volume-keys and the encryption-key to the control file")

class GnomeKeyringKeychain(Keychain):
    def __init__(self, keyring = "truecrypt"):
        self.keyring = keyring
        if not keyring in gnomekeyring.list_keyring_names_sync():
            password = getText()
            gnomekeyring.create_sync(keyring, password)

    def store_password(self, volume, password):
        gnomekeyring.item_create_sync(self.keyring, gnomekeyring.ITEM_GENERIC_SECRET, "Truecrypt device " + volume, dict(appname="truecrypt-control", volume = volume), password, False)

    def get_password(self, volume):
        params = dict(appname = "truecrypt-control", volume = volume.encode('ascii','replace'))
        try:
            matches = gnomekeyring.find_items_sync(gnomekeyring.ITEM_GENERIC_SECRET, params)
            return matches[0].secret
        except gnomekeyring.NoMatchError:
            print "password not found"
            return None            
