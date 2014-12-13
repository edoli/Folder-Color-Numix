#!/bin/bash
rm -r ../icons
rm -r ../po
rm ../README

# setup
sed -i '25,32d' ../setup.py
sed -i 's/]),/])]/' ../setup.py
sed -i 's/Change your folder color with just a click/Change your folder color in Nautilus/' ../setup.py

# extension

# debian
rm ../debian/postinst

sed -i '2d' ../debian/install

sed -i '14,15d' ../debian/control
sed -i 's/ python-nautilus, nautilus, libgtk2.0-bin, / python-nautilus, nautilus, folder-color-common, /' ../debian/control

sed -i '25,45d' ../debian/copyright

sed -i 's/folder-color/folder-color/' ../debian/changelog

# me
rm -r ../install_scripts
