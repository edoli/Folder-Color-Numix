#!/usr/bin/env python

# Folder Color 0.0.46 - http://launchpad.net/folder-color
# Copyright (C) 2012-2014 Marcos Alvarez Costales https://launchpad.net/~costales
#
# folder-color is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# Folder Color is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Folder Color; if not, see http://www.gnu.org/licenses 
# for more information.


import os, sys, glob, DistUtilsExtra.auto

# Create data files
data = [ ('/usr/share/nautilus-python/extensions',     ['nautilus-extension/folder-color.py']),
         ('/usr/share/icons/hicolor/scalable/places',  glob.glob('icons/hicolor/scalable/places/*.svg')),
         ('/usr/share/icons/hicolor/scalable/emblems', glob.glob('icons/hicolor/scalable/emblems/*.svg')),
         ('/usr/share/icons/hicolor/48x48/places',     glob.glob('icons/hicolor/48x48/places/*.svg')),
         ('/usr/share/icons/hicolor/48x48/emblems',    glob.glob('icons/hicolor/48x48/emblems/*.svg')),
         ('/usr/share/icons/hicolor/16x16/actions',    glob.glob('icons/hicolor/16x16/actions/*.svg')),
         ('/usr/share/icons/hicolor/16x16/places',     glob.glob('icons/hicolor/16x16/places/*.svg')),
         ('/usr/share/icons/hicolor/22x22/places',     glob.glob('icons/hicolor/22x22/places/*.svg')),
         ('/usr/share/icons/hicolor/24x24/places',     glob.glob('icons/hicolor/24x24/places/*.svg')) ]

# Setup stage
DistUtilsExtra.auto.setup(
    name         = "folder-color",
    version      = "0.0.46",
    description  = "Change your folder color with just a click",
    author       = "Marcos Alvarez Costales https://launchpad.net/~costales",
    author_email = "https://launchpad.net/~costales",
    url          = "https://launchpad.net/folder-color",
    license      = "GPL3",
    data_files   = data
    )

