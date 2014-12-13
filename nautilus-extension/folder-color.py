# -*- coding: utf-8 -*-
# Folder Color 0.0.46
# Copyright (C) 2012-2014 Marcos Alvarez Costales https://launchpad.net/~costales
#
# Folder Color is free software; you can redistribute it and/or modify
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

import os, urllib, gettext, webbrowser, glob, subprocess
from gi.repository import Gtk, Nautilus, GObject, Gio, GLib

# i18n
gettext.textdomain('folder-color-common')
_ = gettext.gettext


class ChangeColorFolder(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        dummy_default_i18n = (_("Brown"), _("Blue"), _("Green"), _("Grey"), _("Orange"), _("Pink"), _("Red"), _("Purple"), _("Yellow"), _("Favorite"), _("Finished"), _("Important"), _("In Progress")) # Need i18n, because colors/emblems are dynamic now
        if not len(self.get_menu_items()):
            return # No icons = Nothing to do
        
        self.GRADIENT_MIDDLE_RANGE = 2500
        self.GRADIENT_DARK_RANGE = 5000
        self.HIDE_DONATION = os.path.join(os.getenv('HOME'), '.config', 'folder-color', 'hide_donation')
        self.FOLDER_ICONS_CUSTOM = os.path.join(os.getenv('HOME'), '.config', 'folder-color', 'custom_icons')
        self.DEFAULT_FOLDERS = self.get_default_folders()
        
        if not os.path.exists(self.FOLDER_ICONS_CUSTOM):
            try:
                os.makedirs(self.FOLDER_ICONS_CUSTOM)
            except OSError as exception:
                pass
            except:
                pass
        pass
    
    def get_theme_path(self, what='places'):
        default_theme_path = '/usr/share/icons/hicolor/scalable' # hardcode, because if not colors, not entry by init
        
        icon_theme = Gtk.IconTheme.get_default()
        icon_info = icon_theme.lookup_icon('folder_color_custom', 0, 0)
        try:
            theme_path = icon_info.get_filename().replace('/places/folder_color_custom.svg', '') # Will be something like /usr/share/icons/Theme/scalable/places/folder_color_custom.svg
            # Hack for emblems: Exist theme, but without emblems, get hicolor emblems
            if what == 'emblem':
                emblems_in_theme = glob.glob(os.path.join(theme_path, 'emblems/folder_emblem_*.svg'))
                if not len(emblems_in_theme):
                    theme_path = default_theme_path
        except:
            theme_path = default_theme_path
        
        if what == 'emblem':
            return os.path.join(theme_path, 'emblems')
        else:
            return os.path.join(theme_path, 'places')
    
    def get_menu_items(self, get_type='color'):
        available_items = {}
        available_icons = glob.glob(os.path.join(self.get_theme_path(get_type), 'folder_' + get_type + '_*.svg'))
        for each_icon in available_icons:
            each_icon = os.path.basename(each_icon)
            if not any(not_count in each_icon for not_count in ('undo', 'edit', 'picker', 'custom', 'desktop', 'documents', 'downloads', 'music', 'pictures', 'public', 'templates', 'videos')):
                color = each_icon.replace('folder_' + get_type + '_', '').replace('.svg', '').replace('_', ' ')
                available_items[color] = _(color.title())
        return available_items
    
    def get_default_folders(self):
        folders = {}
        folders[GLib.get_user_special_dir(GLib.USER_DIRECTORY_DESKTOP)]      = 'desktop'
        folders[GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOCUMENTS)]    = 'documents'
        folders[GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOWNLOAD)]     = 'downloads'
        folders[GLib.get_user_special_dir(GLib.USER_DIRECTORY_MUSIC)]        = 'music'
        folders[GLib.get_user_special_dir(GLib.USER_DIRECTORY_PICTURES)]     = 'pictures'
        folders[GLib.get_user_special_dir(GLib.USER_DIRECTORY_PUBLIC_SHARE)] = 'public'
        folders[GLib.get_user_special_dir(GLib.USER_DIRECTORY_TEMPLATES)]    = 'templates'
        folders[GLib.get_user_special_dir(GLib.USER_DIRECTORY_VIDEOS)]       = 'videos'
        return folders
    
    def get_icon_name(self, folder, icon, get_type='color'):
        icon = icon.replace(' ', '_') # Come from the file name
        
        # Available preconfigured icon?
        try:
            if os.path.isfile(os.path.join(self.get_theme_path(get_type), 'folder_%s_%s_%s.svg' % (get_type, icon, self.DEFAULT_FOLDERS[folder]))):
                return '_'.join(['folder', 'color', icon, self.DEFAULT_FOLDERS[folder]])
        except:
            pass
        
        # Default icon
        return '_'.join(['folder', get_type, icon])
    
    def choose_custom_color(self):
        colorselectiondialog = Gtk.ColorSelectionDialog(_("Choose a Folder Color"))
        selector = colorselectiondialog.get_color_selection()
        response = colorselectiondialog.run()
        colorselectiondialog.destroy()
        
        if response == Gtk.ResponseType.OK:
            color = selector.get_current_color()
            # Control max color range
            if color.red <= self.GRADIENT_DARK_RANGE:
                color.red = self.GRADIENT_DARK_RANGE
            if color.green <= self.GRADIENT_DARK_RANGE:
                color.green = self.GRADIENT_DARK_RANGE
            if color.blue <= self.GRADIENT_DARK_RANGE:
                color.blue = self.GRADIENT_DARK_RANGE
            # Convert to hex
            rgb_ligth = (color.red, color.green, color.blue)
            rgb_middle = (color.red-self.GRADIENT_MIDDLE_RANGE, color.green-self.GRADIENT_MIDDLE_RANGE, color.blue-self.GRADIENT_MIDDLE_RANGE)
            rgb_dark = (color.red-self.GRADIENT_DARK_RANGE, color.green-self.GRADIENT_DARK_RANGE, color.blue-self.GRADIENT_DARK_RANGE)
            htmlcolor_light =  ''.join((str(hex(i/257))[2:].rjust(2, '0') for i in rgb_ligth)).upper()
            htmlcolor_middle = ''.join((str(hex(i/257))[2:].rjust(2, '0') for i in rgb_middle)).upper()
            htmlcolor_dark =   ''.join((str(hex(i/257))[2:].rjust(2, '0') for i in rgb_dark)).upper()
            return (htmlcolor_light, htmlcolor_middle, htmlcolor_dark)
        
        return None
    
    def generate_icon_from_template(self, folder, colors):
        # Parsing template to a custom color
        orig_file = os.path.join(self.get_theme_path(), self.get_icon_name(folder, 'custom') + '.svg')
        dest_file = os.path.join(self.FOLDER_ICONS_CUSTOM, ''.join([self.get_icon_name(folder, 'custom'), '_', colors[0], '.svg']))
        
        f_input = open(orig_file, 'r') # This has to exists always
        f_output = open(dest_file, 'w')
        
        f_generate  = f_input.read().replace('value_light', colors[0]).replace('value_middle', colors[1]).replace('value_dark', colors[2])
        f_output.write(f_generate)
        
        return dest_file
    
    def reload_icon(self, folder):
        # Reload the current folder
        os.system('touch "%s"' % folder)
    
    def menu_activate_color(self, menu, color, folders):
        # Custom
        if color == 'custom':
            custom_color = self.choose_custom_color()
            # Cancel?
            if custom_color == None:
                return
        
        for each_folder in folders:
            if each_folder.is_gone():
                continue
            
            # Get info
            folder_name = urllib.unquote(each_folder.get_uri()[7:])
            folder = Gio.File.new_for_path(folder_name)
            info = folder.query_info('metadata::custom-icon-name', 0, None)
            
            # Restore always previously, because I don't know if I set previously with custom-icon or custom-icon-name
            info.set_attribute('metadata::custom-icon', Gio.FileAttributeType.INVALID, 0)
            info.set_attribute('metadata::custom-icon-name', Gio.FileAttributeType.INVALID, 0)
            
            # Set color
            if not color == 'restore':
                if not color == 'custom':
                    new_color = self.get_icon_name(folder_name, color)
                    info.set_attribute_string("metadata::custom-icon-name", new_color)
                else:
                    file_custom_color = ''.join(['file://', self.generate_icon_from_template(folder_name, custom_color)]) # Generate file color
                    info.set_attribute_string('metadata::custom-icon', file_custom_color)
            else:
                self.set_emblem(folder_name, '') # Restore all
            
            # Write changes
            folder.set_attributes_from_info(info, 0, None)
            
            # Reload changes
            self.reload_icon(folder_name)
    
    def set_emblem(self, folder, emblem=''):
        # TODO: Use Gio for doing this
        if emblem:
            subprocess.call('gvfs-set-attribute -t stringv "%s" metadata::emblems %s' % (folder, emblem), shell=True)
        else:
            subprocess.call('gvfs-set-attribute -t unset "%s" metadata::emblems' % folder, shell=True)
            
    def menu_activate_emblem(self, menu, emblem, folders):
        for each_folder in folders:
            if each_folder.is_gone():
                continue
            
            folder = urllib.unquote(each_folder.get_uri()[7:])
            new_emblem = ''
            if not emblem == 'restore':
                new_emblem = ''.join(['folder_emblem_', emblem.replace(' ', '_')])
            
            self.set_emblem(folder, new_emblem)
            
            # Reload changes
            self.reload_icon(folder)
    
    def menu_activate_donate(self, menu):
        webbrowser.open_new('http://gufw.org/donate_foldercolor')
        # Hide donation after show it
        try:
            os.makedirs(self.HIDE_DONATION)
        except OSError as exception:
            pass
        except:
            pass
        return
    
    # Nautilus invoke this function in its startup > Then, create menu entry
    def get_file_items(self, window, items_selected):
        if not len(self.get_menu_items()):
            return # No icons = Nothing to do
        
        # No items selected
        if not len(items_selected):
            return
        for each_item in items_selected:
            # GNOME can only handle files
            if each_item.get_uri_scheme() != 'file':
                return
            # Only folders
            if not each_item.is_directory():
                return
        
        # Main menu [1 or +1 folder(s)]
        if len(items_selected) > 1:
            top_menuitem = Nautilus.MenuItem(name='ChangeFolderColorMenu::Top', label=_("Folders' Color"), icon='folder_color_picker')
        else:
            top_menuitem = Nautilus.MenuItem(name='ChangeFolderColorMenu::Top', label=_("Folder's Color"),  icon='folder_color_picker')
        submenu = Nautilus.Menu()
        top_menuitem.set_submenu(submenu)
        
        # Colors submenu
        sorted_colors = sorted(self.get_menu_items().items(), key=lambda x:x[1])
        for color in sorted_colors:
            name = ''.join(['ChangeFolderColorMenu::Colors"', color[0], '"'])
            label = color[1]
            item = Nautilus.MenuItem(name=name, label=label, icon=self.get_icon_name('Default', color[0].lower()))
            item.connect('activate', self.menu_activate_color, color[0], items_selected)
            submenu.append_item(item)
        
        # Custom color
        item_custom = Nautilus.MenuItem(name=''.join(['ChangeFolderColorMenu::"custom"']), label=_("Custom"), icon='folder_color_edit')
        item_custom.connect('activate', self.menu_activate_color, 'custom', items_selected)
        submenu.append_item(item_custom)
        
        # Restore
        # Separator
        item_sep = Nautilus.MenuItem(name='ChangeFolderEmblemMenu::Sep', label=_("Restore"), sensitive=False)
        submenu.append_item(item_sep)
        
        item_restore = Nautilus.MenuItem(name='ChangeFolderColorMenu::Restore', label=_("By Default"), icon='folder_color_undo')
        item_restore.connect('activate', self.menu_activate_color, 'restore', items_selected)
        submenu.append_item(item_restore)
        
        # Emblems submenu
        sorted_emblems = sorted(self.get_menu_items('emblem').items(), key=lambda x:x[1])
        for i,emblem in enumerate(sorted_emblems):
            # Separator
            if not i:
                item_sep = Nautilus.MenuItem(name='ChangeFolderColorMenu::Sep1', label=_("Categorize"), sensitive=False)
                submenu.append_item(item_sep)
            
            name = ''.join(['ChangeFolderEmblemMenu::Emblem"', emblem[0], '"'])
            label = emblem[1]
            item = Nautilus.MenuItem(name=name, label=label, icon=self.get_icon_name('Default', emblem[0].lower(), 'emblem'))
            item.connect('activate', self.menu_activate_emblem, emblem[0], items_selected)
            submenu.append_item(item)
        
        # Donation
        if not os.path.exists(self.HIDE_DONATION):
            # Separator
            item_sep = Nautilus.MenuItem(name='ChangeFolderColorMenu::Sep2', label=_("Support this app"), sensitive=False)
            submenu.append_item(item_sep)
            # Donation
            item = Nautilus.MenuItem(name=''.join(['ChangeFolderColorMenu::"donate"']), label=_("Donate? Click for hiding"))
            item.connect('activate', self.menu_activate_donate)
            submenu.append_item(item)
        
        return top_menuitem,
