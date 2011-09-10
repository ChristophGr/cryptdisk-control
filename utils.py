#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import json
from time import sleep
from logconfig import logger

def read_file_contents(path):
    mfile = open(path, 'r')
    result = [ x for x in mfile.xreadlines() ]
    mfile.close()
    return result

def read_json_file(path):
    f = open(path, 'r')
    config = json.loads(f.read())
    f.close()
    return config

def write_json_file(path, content):
    f = open(path, 'w')
    f.write(json.dumps(content))
    f.close()

def read_command_output(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    return proc.stdout.readlines()

def generate_random_key(length):
    import string
    import random
    charset = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(charset) for x in range(length))

def listdircontents(path):
    dirList = os.listdir(path)
    return [ os.path.join(path, x) for x in dirList ]

def do_find_first_existing_dir_in_path(dirname, filename):
    if os.path.exists(dirname):
        return dirname, filename
    else:
        dir2, file2 = os.path.split(dirname)
        logger.debug("recursing %s, %s" % (dir2, file2))
        if dir2 == dirname:
            return None
        return do_find_first_existing_dir_in_path(dir2, file2)

def find_first_existing_dir_in_path(path):
    dirname, filename = os.path.split(path)
    if os.path.exists(path):
        return dirname, filename
    else:
        return do_find_first_existing_dir_in_path(dirname, filename)

def find_unique_dev_path(devpath):
    dirList = [ x for x in listdircontents("/dev/disk/by-id/") if os.path.samefile(x, devpath) ]
    if len(dirList) > 0:
        return dirList[0];
    return None

import gtk

def responseToDialog(entry, dialog, response):
    dialog.response(response)

def get_password_from_dialog(message = "Enter password", message2 = ""):
    #base this on a message dialog
    dialog = gtk.MessageDialog(
        None,
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        gtk.MESSAGE_QUESTION,
        gtk.BUTTONS_OK,
        None)
    dialog.set_markup(message)
    #create the text input field
    entry = gtk.Entry()
    entry.set_visibility(False)
    #allow the user to press enter to do ok
    entry.connect("activate", responseToDialog, dialog, gtk.RESPONSE_OK)
    #create a horizontal box to pack the entry and a label
    hbox = gtk.HBox()
    hbox.pack_start(gtk.Label("Password:"), False, 5, 5)
    hbox.pack_end(entry)
    #some secondary text
    dialog.format_secondary_markup(message2)
    #add it and show it
    dialog.vbox.pack_end(hbox, True, True, 0)
    dialog.show_all()
    #go go go
    dialog.run()
    text = entry.get_text()
    dialog.destroy()
    return text
