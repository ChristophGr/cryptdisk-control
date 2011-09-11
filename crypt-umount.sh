#!/bin/sh
umount "/dev/mapper/$2"
cryptsetup luksClose $2
rm -r "/media/$2"
