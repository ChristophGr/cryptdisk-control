#!/bin/sh
echo $3 | cryptsetup luksOpen "$1" "$2"
mkdir "/media/$2"
mount "/dev/mapper/$2" "/media/$2"
