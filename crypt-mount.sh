#!/bin/sh
echo $3 | cryptsetup luksOpen "$1" "$2" && mkdir -p "/media/$2" && mount "/dev/mapper/$2" "/media/$2"
