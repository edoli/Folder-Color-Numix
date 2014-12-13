#!/bin/bash
rm -r ../icons
rm -r ../po
rm ../README

# setup
sed -i '25,32d' ../setup.py
sed -i 's/]),/])]/' ../setup.py
sed -i 's/Change your folder color with just a click/Change your folder color in Caja/' ../setup.py
sed -i 's/nautilus-python/caja-python/' ../setup.py
sed -i 's/nautilus-extension/caja-extension/' ../setup.py
sed -i 's/"folder-color"/"folder-color-caja"/' ../setup.py

# extension
mv ../nautilus-extension/ ../caja-extension
sed -i 's/nautilus/caja/g' ../caja-extension/folder-color.py
sed -i 's/Nautilus/Caja/g' ../caja-extension/folder-color.py
sed -i 's/\"metadata::custom-icon-name\", new_color)/\"metadata::custom-icon\", \"\".join([\"file:\/\/\/usr\/share\/icons\/hicolor\/scalable\/places\/\", new_color, \".svg\"]\)\)/' ../caja-extension/folder-color.py

# debian
rm ../debian/postinst

sed -i '2d' ../debian/install
sed -i 's/nautilus/caja/g' ../debian/install

sed -i 's/Upstream-Name: folder-color/Upstream-Name: folder-color-caja/' ../debian/copyright
sed -i '25,45d' ../debian/copyright

sed -i 's/Source: folder-color/Source: folder-color-caja/' ../debian/control
sed -i 's/Package: folder-color/Package: folder-color-caja/' ../debian/control
sed -i 's/python-nautilus, nautilus, libgtk2.0-bin, /python-caja, gir1.2-caja, caja, gir1.2-gtk-2.0, folder-color-common, /' ../debian/control
sed -i '14,15d' ../debian/control
sed -i 's/Folder Color for Nautilus/Folder Color for Caja/' ../debian/control
sed -i 's/Change a folder color used in Nautilus/Change a folder color used in Caja/' ../debian/control

sed -i 's/folder-color/folder-color-caja/' ../debian/changelog

# me
rm -r ../install_scripts

