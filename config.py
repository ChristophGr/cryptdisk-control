#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

configfile = os.path.expanduser("~/.crypt-control")

#import plaintextkeychain
#keychain = plaintextkeychain.PlaintextKeychain(os.path.expanduser("~/.crypt-passwords"))

import gkeyringimpl
keychain = gkeyringimpl.GnomeKeyringKeychain("truecrypt")
