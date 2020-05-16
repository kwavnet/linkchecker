# Copyright (C) 2000-2014 Bastian Kleineidam
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
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
A HTML logger.
"""

import html
import os
import time

from . import _Logger
from .. import strformat, configuration


# ss=1 enables show source
validate_html = "http://validator.w3.org/check?ss=1&amp;uri=%(uri)s"
# options are the default
validate_css = "http://jigsaw.w3.org/css-validator/validator?" \
               "uri=%(uri)s&amp;warning=1&amp;profile=css2&amp;usermedium=all"

HTML_HEADER = """<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=%(encoding)s"/>
<title>%(title)s</title>
<style type="text/css">
<!--
 h2 { font-family: Verdana,sans-serif; font-size: 22pt; font-weight: bold; }
 body { font-family: Arial,sans-serif; font-size: 11pt; background-color: %(body)s; }
 td { font-family: Arial,sans-serif; font-size: 11pt; }
 code { font-family: Courier; }
 a:link {color: %(link)s;}
 a:visited {color: %(vlink)s;}
 a:active {color: %(alink)s;}
 a:hover { color: #34a4ef; }
 table { border-collapse:collapse; }
 table, th, td { border: 1px solid black; padding: 2px; }
 td.url { background-color: %(url)s }
 td.valid { background-color: %(valid)s }
 td.error { background-color: %(error)s }
 td.warning { background-color: %(warning)s }
-->
</style>
</head>
<body>
"""


class HtmlLogger(_Logger):
    """Logger with HTML output."""

    LoggerName = 'html'

    LoggerArgs =  {
        "filename":        "linkchecker-out.html",
        'colorbackground': '#fff7e5',
        'colorurl':        '#dcd5cf',
        'colorborder':     '#000000',
        'colorlink':       '#191c83',
        'colorwarning':    '#e0954e',
        'colorerror':      '#db4930',
        'colorok':         '#3ba557',
    }

    def __init__ (self, **kwargs):
        """Initialize default HTML color values."""
        args = self.get_args(kwargs)
        super(HtmlLogger, self).__init__(**args)
        self.init_fileoutput(args)
        self.colorbackground = args['colorbackground']
        self.colorurl = args['colorurl']
        self.colorborder = args['colorborder']
        self.colorlink = args['colorlink']
        self.colorwarning = args['colorwarning']
        self.colorerror = args['colorerror']
        self.colorok = args['colorok']

    def part (self, name):
        """Return non-space-breakable part name."""
        return super(HtmlLogger, self).part(name).replace(" ", "&nbsp;")

    def comment (self, s, **args):
        """Write HTML comment."""
        self.write("<!-- ")
        self.write(s, **args)
        self.write(" -->")

    def start_output (self):
        """Write start of checking info."""
        super(HtmlLogger, self).start_output()
        header = {
            "encoding": self.get_charset_encoding(),
            "title": configuration.App,
            "body": self.colorbackground,
            "link": self.colorlink,
            "vlink": self.colorlink,
            "alink": self.colorlink,
            "url": self.colorurl,
            "error": self.colorerror,
            "valid": self.colorok,
            "warning": self.colorwarning,
        }
        self.write(HTML_HEADER % header)
        self.comment("Generated by %s" % configuration.App)
        if self.has_part('intro'):
            self.write("<h2>"+configuration.App+
                       "</h2><br/><blockquote>"+
                       configuration.Freeware+"<br/><br/>"+
                       (_("Start checking at %s") %
                       strformat.strtime(self.starttime))+
                       os.linesep+"<br/>")
            self.check_date()
        self.flush()

    def log_url (self, url_data):
        """Write url checking info as HTML."""
        self.write_table_start()
        if self.has_part("url"):
            self.write_url(url_data)
        if url_data.name and self.has_part("name"):
            self.write_name(url_data)
        if url_data.parent_url and self.has_part("parenturl"):
            self.write_parent(url_data)
        if url_data.base_ref and self.has_part("base"):
            self.write_base(url_data)
        if url_data.url and self.has_part("realurl"):
            self.write_real(url_data)
        if url_data.dltime >= 0 and self.has_part("dltime"):
            self.write_dltime(url_data)
        if url_data.size >= 0 and self.has_part("dlsize"):
            self.write_size(url_data)
        if url_data.checktime and self.has_part("checktime"):
            self.write_checktime(url_data)
        if url_data.info and self.has_part("info"):
            self.write_info(url_data)
        if url_data.modified and self.has_part("modified"):
            self.write_modified(url_data)
        if url_data.warnings and self.has_part("warning"):
            self.write_warning(url_data)
        if self.has_part("result"):
            self.write_result(url_data)
        self.write_table_end()
        self.flush()

    def write_table_start (self):
        """Start html table."""
        self.writeln('<br/><br/><table>')

    def write_table_end (self):
        """End html table."""
        self.write('</table><br/>')

    def write_id (self):
        """Write ID for current URL."""
        self.writeln("<tr>")
        self.writeln('<td>%s</td>' % self.part("id"))
        self.write("<td>%d</td></tr>" % self.stats.number)

    def write_url (self, url_data):
        """Write url_data.base_url."""
        self.writeln("<tr>")
        self.writeln('<td class="url">%s</td>' % self.part("url"))
        self.write('<td class="url">')
        self.write("`%s'" % html.escape(url_data.base_url))
        self.writeln("</td></tr>")

    def write_name (self, url_data):
        """Write url_data.name."""
        args = (self.part("name"), html.escape(url_data.name))
        self.writeln("<tr><td>%s</td><td>`%s'</td></tr>" % args)

    def write_parent (self, url_data):
        """Write url_data.parent_url."""
        self.write("<tr><td>"+self.part("parenturl")+
                   '</td><td><a target="top" href="'+
                   url_data.parent_url+'">'+
                   html.escape(url_data.parent_url)+"</a>")
        if url_data.line is not None:
            self.write(_(", line %d") % url_data.line)
        if url_data.column is not None:
            self.write(_(", col %d") % url_data.column)
        if url_data.page > 0:
            self.write(_(", page %d") % url_data.page)
        if not url_data.valid:
            # on errors show HTML and CSS validation for parent url
            vhtml = validate_html % {'uri': url_data.parent_url}
            vcss = validate_css % {'uri': url_data.parent_url}
            self.writeln()
            self.writeln('(<a href="'+vhtml+'">HTML</a>)')
            self.write('(<a href="'+vcss+'">CSS</a>)')
        self.writeln("</td></tr>")

    def write_base (self, url_data):
        """Write url_data.base_ref."""
        self.writeln("<tr><td>"+self.part("base")+"</td><td>"+
                     html.escape(url_data.base_ref)+"</td></tr>")

    def write_real (self, url_data):
        """Write url_data.url."""
        self.writeln("<tr><td>"+self.part("realurl")+"</td><td>"+
                     '<a target="top" href="'+url_data.url+
                     '">'+html.escape(url_data.url)+"</a></td></tr>")

    def write_dltime (self, url_data):
        """Write url_data.dltime."""
        self.writeln("<tr><td>"+self.part("dltime")+"</td><td>"+
                     (_("%.3f seconds") % url_data.dltime)+
                     "</td></tr>")

    def write_size (self, url_data):
        """Write url_data.size."""
        self.writeln("<tr><td>"+self.part("dlsize")+"</td><td>"+
                     strformat.strsize(url_data.size)+
                     "</td></tr>")

    def write_checktime (self, url_data):
        """Write url_data.checktime."""
        self.writeln("<tr><td>"+self.part("checktime")+"</td><td>"+
                     (_("%.3f seconds") % url_data.checktime)+"</td></tr>")

    def write_info (self, url_data):
        """Write url_data.info."""
        sep = "<br/>"+os.linesep
        text = sep.join(html.escape(x) for x in url_data.info)
        self.writeln('<tr><td valign="top">' + self.part("info")+
               "</td><td>"+text+"</td></tr>")

    def write_modified(self, url_data):
        """Write url_data.modified."""
        text = html.escape(self.format_modified(url_data.modified))
        self.writeln('<tr><td valign="top">' + self.part("modified") +
            "</td><td>"+text+"</td></tr>")

    def write_warning (self, url_data):
        """Write url_data.warnings."""
        sep = "<br/>"+os.linesep
        text = sep.join(html.escape(x[1]) for x in url_data.warnings)
        self.writeln('<tr><td class="warning" '+
                     'valign="top">' + self.part("warning") +
                     '</td><td class="warning">' + text + "</td></tr>")

    def write_result (self, url_data):
        """Write url_data.result."""
        if url_data.valid:
            self.write('<tr><td class="valid">')
            self.write(self.part("result"))
            self.write('</td><td class="valid">')
            self.write(html.escape(_("Valid")))
        else:
            self.write('<tr><td class="error">')
            self.write(self.part("result"))
            self.write('</td><td class="error">')
            self.write(html.escape(_("Error")))
        if url_data.result:
            self.write(": "+html.escape(url_data.result))
        self.writeln("</td></tr>")

    def write_stats (self):
        """Write check statistic infos."""
        self.writeln('<br/><i>%s</i><br/>' % _("Statistics"))
        if self.stats.number > 0:
            self.writeln(_(
              "Content types: %(image)d image, %(text)d text, %(video)d video, "
              "%(audio)d audio, %(application)d application, %(mail)d mail"
              " and %(other)d other.") % self.stats.link_types)
            self.writeln("<br/>")
            self.writeln(_("URL lengths: min=%(min)d, max=%(max)d, avg=%(avg)d.") %
                         dict(min=self.stats.min_url_length,
                         max=self.stats.max_url_length,
                         avg=self.stats.avg_url_length))
        else:
            self.writeln(_("No statistics available since no URLs were checked."))
        self.writeln("<br/>")

    def write_outro (self):
        """Write end of check message."""
        self.writeln("<br/>")
        self.write(_("That's it.")+" ")
        if self.stats.number >= 0:
            self.write(_n("%d link checked.", "%d links checked.",
                       self.stats.number) % self.stats.number)
            self.write(" ")
        self.write(_n("%d warning found", "%d warnings found",
             self.stats.warnings_printed) % self.stats.warnings_printed)
        if self.stats.warnings != self.stats.warnings_printed:
            self.write(_(" (%d ignored or duplicates not printed)") %
                (self.stats.warnings - self.stats.warnings_printed))
        self.write(". ")
        self.write(_n("%d error found", "%d errors found",
             self.stats.errors_printed) % self.stats.errors_printed)
        if self.stats.errors != self.stats.errors_printed:
            self.write(_(" (%d duplicates not printed)") %
                (self.stats.errors - self.stats.errors_printed))
        self.writeln(".")
        self.writeln("<br/>")
        num = self.stats.internal_errors
        if num:
            self.write(_n("There was %(num)d internal error.",
                "There were %(num)d internal errors.", num) % {"num": num})
            self.writeln("<br/>")
        self.stoptime = time.time()
        duration = self.stoptime - self.starttime
        self.writeln(_("Stopped checking at %(time)s (%(duration)s)") %
             {"time": strformat.strtime(self.stoptime),
              "duration": strformat.strduration_long(duration)})
        self.writeln('</blockquote><br/><hr><small>'+
                     configuration.HtmlAppInfo+"<br/>")
        self.writeln(_("Get the newest version at %s") %
           ('<a href="'+configuration.Url+'" target="_top">'+
            configuration.Url+"</a>.<br/>"))
        self.writeln(_("Write comments and bugs to %s") %
           ('<a href="'+configuration.SupportUrl+'">'+
            configuration.SupportUrl+"</a>.<br/>"))
        self.writeln("</small></body></html>")

    def end_output (self, **kwargs):
        """Write end of checking info as HTML."""
        if self.has_part("stats"):
            self.write_stats()
        if self.has_part("outro"):
            self.write_outro()
        self.close_fileoutput()
