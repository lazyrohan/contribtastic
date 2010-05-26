# python
#    EVE-Central.com Contribtastic
#    Copyright (C) 2005-2010 Yann Ramin
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License (in file COPYING) for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


import sys
import os
import pickle
import time

try:
    from win32com.shell import shell, shellcon
except:
    pass


def find_first_path(path, pref = None):
    dirlist = os.listdir(path)

    if pref is None:
        return dirlist[0]

    for p in pref:
        if p in dirlist or unicode(p) in dirlist:
            return p
    return dirlist[0]


def default_location():
    if sys.platform == 'win32':

        document_folder = "c:/"
        try:
            document_folder = os.path.join( shell.SHGetFolderPath( 0,
                                                                   shellcon.CSIDL_LOCAL_APPDATA,
                                                                   0, 0 ), 'CCP', 'EVE', )
            document_folder = os.path.join ( document_folder,
                                             find_first_path(document_folder, ['237', '236', '235']),
                                             'cache', 'MachoNet', '87.237.38.200')
            document_folder = os.path.join ( document_folder,
                                             find_first_path(document_folder), 'CachedMethodCalls')

        except:
            pass
    elif sys.platform == 'darwin':
        from Carbon import Folder, Folders
        folderref = Folder.FSFindFolder( Folders.kUserDomain, Folders.kPreferencesFolderType, False )
        document_folder = os.path.join( folderref.as_pathname(), 'Eve Online Preferences', 'p_drive', 'My Documents', 'EVE', 'logs', 'MarketLogs' )
    else:
        document_folder = '' # don't know what the linux client has
        document_folder = os.path.normpath( document_folder )

    return document_folder


class Config(object):

    CONFIG_VERSION = '2.0-alpha1'


    def __init__(self):
        self.config_obj = {}

        self.filename = ""
	try:
            import wx
            sp = wx.StandardPaths.Get()
            wx.GetApp().SetAppName("EVE-Central MarketUploader")
            path = sp.GetUserLocalDataDir()

            try:
                os.mkdir(path)
            except:
                pass

            self.filename = os.path.normpath( os.path.join( path, 'data.pickle' ) )
	except:
            pass

        if not len(self.filename):
            try:
                self.filename = os.path.normpath( os.path.join( os.environ['HOME'], '.contribtastic.pickle' ) )
            except:
                pass

        self.reinit = self.load_config()

    def __getitem__(self, key):
        return self.config_obj[key]

    def __setitem__(self, key, value):
        ret =  self.config_obj[key] = value
        self.save_config()
        return ret

    def __len__(self):
        return len(self.config_obj)

    def __delitem__(self, key):
        del self.config_obj[key]


    def default_data(self):

        loc = default_location()
        loc = [loc]

        self.config_obj = { 'version' : Config.CONFIG_VERSION,
                            'path_set' : False,
                            'backup' : 'backup',
                            'evepath' : loc,
                            'character_name' : 'Anonymous',
                            'character_id' : 0,
                            'last_upload_time' : time.time()
                            }

    def save_config(self):


        file = open( self.filename, "w")

        pickle.dump(self.config_obj, file)

        file.close()



    def load_config(self):


        ret = 0
        file = None
        try:
            file = open( self.filename, "r")
            ret = 0
            self.config_obj = pickle.load(file)
        except:
            if file:
                file.close()
                file = None

            self.default_data()
            self.save_config()
            return -1
        finally:
            if file:
                file.close()

        if self.config_obj['version'] != Config.CONFIG_VERSION:
            self.default_data()
            self.save_config()
            ret = -1

        return ret
