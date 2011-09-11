#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from utils import *

configfile = os.path.expanduser("~/.crypt-control")

if hasX():
    import gkeyringimpl
    keychain = gkeyringimpl.GnomeKeyringKeychain("truecrypt")
else:
    import plaintextkeychain
    keychain = plaintextkeychain.PlaintextKeychain(os.path.expanduser("~/.crypt-passwords"))
