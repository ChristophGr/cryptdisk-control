#!/bin/sh
umount "/dev/mapper/$1" && cryptsetup luksClose $1 && rm -r "/media/$1"
