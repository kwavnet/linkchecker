# Copyright (C) 2000-2002  Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from StandardLogger import StandardLogger

class ColoredLogger (StandardLogger):
    """ANSI colorized output"""

    def __init__ (self, **args):
        esc="\x1b[%sm"
        apply(StandardLogger.__init__, (self,), args)
        self.colorparent = esc % args['colorparent']
        self.colorurl = esc % args['colorurl']
        self.colorname = esc % args['colorname']
        self.colorreal = esc % args['colorreal']
        self.colorbase = esc % args['colorbase']
        self.colorvalid = esc % args['colorvalid']
        self.colorinvalid = esc % args['colorinvalid']
        self.colorinfo = esc % args['colorinfo']
        self.colorwarning = esc % args['colorwarning']
        self.colordltime = esc % args['colordltime']
        self.colorreset = esc % args['colorreset']
        self.currentPage = None
        self.prefix = 0

    def newUrl (self, urlData):
        if self.fd is None: return
        if self.logfield("parenturl"):
            if urlData.parentName:
                if self.currentPage != urlData.parentName:
                    if self.prefix:
                        self.fd.write("o\n")
                    self.fd.write("\n"+linkcheck._("Parent URL")+Spaces["parenturl"]+
		              self.colorparent+urlData.parentName+
			      self.colorreset+"\n")
                    self.currentPage = urlData.parentName
                    self.prefix = 1
            else:
                if self.prefix:
                    self.fd.write("o\n")
                self.prefix = 0
                self.currentPage=None
        if self.logfield("url"):
            if self.prefix:
                self.fd.write("|\n+- ")
            else:
                self.fd.write("\n")
            self.fd.write(linkcheck._("URL")+Spaces["url"]+self.colorurl+
	              urlData.urlName+self.colorreset)
            if urlData.line: self.fd.write(linkcheck._(", line ")+`urlData.line`+"")
            if urlData.cached:
                self.fd.write(linkcheck._(" (cached)\n"))
            else:
                self.fd.write("\n")

        if urlData.name and self.logfield("name"):
            if self.prefix:
                self.fd.write("|  ")
            self.fd.write(linkcheck._("Name")+Spaces["name"]+self.colorname+
                          urlData.name+self.colorreset+"\n")
        if urlData.baseRef and self.logfield("base"):
            if self.prefix:
                self.fd.write("|  ")
            self.fd.write(linkcheck._("Base")+Spaces["base"]+self.colorbase+
	                  urlData.baseRef+self.colorreset+"\n")
            
        if urlData.url and self.logfield("realurl"):
            if self.prefix:
                self.fd.write("|  ")
            self.fd.write(linkcheck._("Real URL")+Spaces["realurl"]+self.colorreal+
	                  urlData.url+self.colorreset+"\n")
        if urlData.downloadtime and self.logfield("dltime"):
            if self.prefix:
                self.fd.write("|  ")
            self.fd.write(linkcheck._("D/L Time")+Spaces["dltime"]+self.colordltime+
	        (linkcheck._("%.3f seconds") % urlData.downloadtime)+self.colorreset+"\n")
        if urlData.checktime and self.logfield("checktime"):
            if self.prefix:
                self.fd.write("|  ")
            self.fd.write(linkcheck._("Check Time")+Spaces["checktime"]+
                self.colordltime+
	        (linkcheck._("%.3f seconds") % urlData.checktime)+self.colorreset+"\n")
            
        if urlData.infoString and self.logfield("info"):
            if self.prefix:
                self.fd.write("|  "+linkcheck._("Info")+Spaces["info"]+
                      StringUtil.indentWith(StringUtil.blocktext(
                        urlData.infoString, 65), "|      "+Spaces["info"]))
            else:
                self.fd.write(linkcheck._("Info")+Spaces["info"]+
                      StringUtil.indentWith(StringUtil.blocktext(
                        urlData.infoString, 65), "    "+Spaces["info"]))
            self.fd.write(self.colorreset+"\n")
            
        if urlData.warningString:
            #self.warnings += 1
            if self.logfield("warning"):
                if self.prefix:
                    self.fd.write("|  ")
                self.fd.write(linkcheck._("Warning")+Spaces["warning"]+
		          self.colorwarning+
	                  urlData.warningString+self.colorreset+"\n")

        if self.logfield("result"):
            if self.prefix:
                self.fd.write("|  ")
            self.fd.write(linkcheck._("Result")+Spaces["result"])
            if urlData.valid:
                self.fd.write(self.colorvalid+urlData.validString+
	                      self.colorreset+"\n")
            else:
                self.errors += 1
                self.fd.write(self.colorinvalid+urlData.errorString+
	                      self.colorreset+"\n")
        self.fd.flush()


    def endOfOutput (self, linknumber=-1):
        if self.fd is None: return
        if self.logfield("outro"):
            if self.prefix:
                self.fd.write("o\n")
        StandardLogger.endOfOutput(self, linknumber=linknumber)


