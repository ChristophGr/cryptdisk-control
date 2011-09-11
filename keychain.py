#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getpass

class Keychain:
    def store_password(self, volume, password):
        pass
    def get_password(self, volume):
        pass

#def get_password(keychain, volume):
    #result = keychain.get_password(volume)
    #if result == None:
        #result = getpass.getpass()
        #keychain.store_password(volume, result)
    #return result
