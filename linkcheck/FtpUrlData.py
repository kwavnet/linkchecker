"""
    Copyright (C) 2000  Bastian Kleineidam

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
import ftplib
from UrlData import UrlData
from linkcheck import _


class FtpUrlData(UrlData):
    """
    Url link with ftp scheme. 
    """
    
    def checkConnection(self, config):
        _user, _password = self._getUserPassword(config)
        self.urlConnection = ftplib.FTP(self.urlTuple[1], _user, _password)
        info = self.urlConnection.getwelcome()
        if not info:
            self.closeConnection()
            raise Exception, _("Got no answer from FTP server")
        self.setInfo(info)
       
    def closeConnection(self):
        try: self.urlConnection.quit()
        except: pass
        self.urlConnection = None
       
    def __str__(self):
        return "FTP link\n"+UrlData.__str__(self)

    
