#!/bin/sh
umount "/dev/mapper/$1" || exit 1
cryptsetup luksClose $1
CODE=$?
if [ "$CODE" == "241" ]; then # busy
  dmsetup remove luks0
elif [ "$CODE" != "0" ]; then
  exit 1;
fi
rmdir "/media/$1"
