#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent, IN_DELETE, IN_CREATE, IN_DELETE_SELF
import subprocess

from utils import *
from logconfig import logger

mask = IN_DELETE | IN_CREATE | IN_DELETE_SELF # watched events
wm = WatchManager()
# wm.add_watch("/dev/disk/by-id", mask)

class PTmp(ProcessEvent):
    def __init__(self, wm, fullname, handler):
        self.fullname = fullname
        self.wm = wm
        self.handler = handler

        self.wd = None
        self.recalcWatchDir()

    def process_IN_CREATE(self, event):
        logger.debug("CREATED: %s" %  os.path.join(event.path, event.name))
        fullname = os.path.join(event.path, event.name)
        if fullname == self.fullname:
            self.handler.on_create(fullname)
        elif event.name == self.filename:
            logger.info("matched file-CREATED: %s" %  os.path.join(event.path, event.name))
            self.recalcWatchDir()

    def process_IN_DELETE(self, event):
        logger.debug("DELETED: %s" %  os.path.join(event.path, event.name))
        fullname = os.path.join(event.path, event.name)
        if fullname == self.fullname:
            self.handler.on_delete(fullname)
        elif event.name == self.filename:
            logger.info("matched file-DELETED: %s" %  os.path.join(event.path, event.name))
            self.recalcWatchDir()

    def process_IN_DELETE_SELF(self, event):
        logger.debug("DELETED_SELF: %s" %  os.path.join(event.path, event.name))
        self.wd = None
        self.recalcWatchDir()

    def recalcWatchDir(self, arg = None):
        if self.wd != None:
            logger.debug("removing current watch %s" % self.wd)
            self.wm.rm_watch(self.wd)
        path, filename = find_first_existing_dir_in_path(self.fullname)
        self.filename = filename
        wdd = self.wm.add_watch(path, mask)
        self.wd = wdd[path]
        logger.debug("_currently watching %s / %s" % (path, filename))


notifiers = dict()

def start_watching_disk_file(filename, handler):
    logger.info("start watching %s" % filename)
    wm = WatchManager()
    notifier = ThreadedNotifier(wm, PTmp(wm, filename, handler))
    notifier.start()
    notifiers[filename] = notifier
    if os.path.exists(filename):
        handler.on_create(filename)

def stop_watching_disk_file(filename):
    logger.info("stop watching %s" % filename)
    notifiers[filename].stop()
    del notifiers[filename]

def mount_volume(path, password):
    logger.info("mounting %s with pw %s" % (path, "****"))
    if password == None:
        logger.error("cannot mount volume, missing password")
        return False
    command = ["truecrypt", "-t", "--non-interactive", "--fs-options=user", "--mount", path, "-p", password]
    logger.debug(" ".join(command))
    return subprocess.call(command) == 0

def find_name():
    base = "luks"
    i = 0
    while os.path.exists("/dev/mapper/" + base + str(i)):
        i = i + 1
    return base + str(i)

def mount_luks_volume(path, password):
    logger.info("mounting %s with pw %s" % (path, "****"))
    if password == None:
        logger.error("cannot mount volume, missing password")
        return False
    name = find_name()
    luksopencommand = ["cryptsetup", "luksOpen", path, name]
    subprocess.call(luksopencommand)
    os.mkdir("/media/" + name)
    mountcommand = ["mount", "/dev/mapper/" + name, "/media/" + name ]
    subprocess.call(mountcommand)
    return name


def main():
    print find_name()

if __name__ == "__main__":
    main()