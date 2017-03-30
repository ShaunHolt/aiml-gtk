#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# AIML-Gtk is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# AIML-Gtk is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with AIML-Gtk. If not, see <http://www.gnu.org/licenses/>.

import os, gi, locale, gettext, datetime, aiml
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

locale.setlocale(locale.LC_ALL, "")
lang = locale.getlocale(locale.LC_MESSAGES)[0]
language_list = ["en_US", "es_ES", "it_IT"]

if lang in language_list:
    gettext.translation(lang,\
    localedir="po/locale", languages=language_list).install()
else:
    gettext.translation("en_US",\
    localedir="po/locale", languages=language_list).install()

width = 500
height = 500

program = "AIML-Gtk"
version = "0.1.2"
website = "https://github.com/sidus-dev/aiml-gtk"
authors = "Andrea Pasciuta  <sidus@arbornet.org>"
comments = _("A simple Gtk frontend for PyAIML")
license = """
AIML-Gtk is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

AIML-Gtk is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with AIML-Gtk. If not, see <http://www.gnu.org/licenses/>.
"""

kern = aiml.Kernel()
kern.setTextEncoding(None)

class dialogs(Gtk.Window):

    def about(self, window):

        d = Gtk.AboutDialog(self)
        d.set_program_name(program)
        d.set_version(version)
        d.set_logo(window.pixbuf)
        d.set_website(website)
        d.set_website_label(website)
        d.set_authors([authors])
        d.set_comments(comments)
        d.set_license(license)
        d.set_wrap_license(True)
        d.set_copyright("{} © {}".format(program, datetime.datetime.now().year))
        d.set_transient_for(window)
        d.run()
        d.destroy()

    def open_brain(self):

        d = Gtk.FileChooserDialog(_("Open brain file"), self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))

        d.set_modal(True)

        filt = Gtk.FileFilter()
        filt.set_name("Brain files (.brn)")
        filt.add_pattern("*.brn")
        d.add_filter(filt)

        if d.run() == Gtk.ResponseType.ACCEPT:
            filename = d.get_filename()
            d.destroy()
            return filename

        d.destroy()

    def open_aiml(self):

        d = Gtk.FileChooserDialog(_("Open aiml file(s)"), self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))

        d.set_select_multiple(True)
        d.set_modal(True)

        filt = Gtk.FileFilter()
        filt.set_name("AIML files (.aiml)")
        filt.add_pattern("*.aiml")
        d.add_filter(filt)

        if d.run() == Gtk.ResponseType.ACCEPT:
            filenames = d.get_filenames()
            d.destroy()
            return filenames

        d.destroy()

    def save(self, title):

        d = Gtk.FileChooserDialog(title, self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))

        d.set_do_overwrite_confirmation(True)
        d.set_modal(True)

        if d.run() == Gtk.ResponseType.ACCEPT:
            filename = d.get_filename()
            d.destroy()
            return filename

        d.destroy()

    def error(self, first, second):

        d = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, first)
        d.format_secondary_markup(second)
        d.run()
        d.destroy()

class main(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self)

        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file("icons/aiml-gtk-logo.svg")
        self.set_icon(self.pixbuf)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(width, height)

        bar = Gtk.HeaderBar()
        bar.set_title(program)
        bar.set_show_close_button(True)
        self.set_titlebar(bar)

        box = Gtk.HBox()
        entry = Gtk.Entry()
        entry.connect("activate", self.chat)

        cbtn = Gtk.ToolButton.new_from_stock(Gtk.STOCK_EXECUTE)
        cbtn.connect("clicked", self.chat)

        opop = Gtk.Popover()
        opop.set_position(Gtk.PositionType.BOTTOM)

        obrn = self.modelbutton(_("Import .brn file ..."))
        obrn.connect("clicked", self.on_obrn_clicked)

        oaim = self.modelbutton(_("Import .aiml file(s) ..."))
        oaim.connect("clicked", self.on_oaim_clicked)

        ogrid = Gtk.Grid()
        ogrid.set_property("margin", 5)
        ogrid.attach(obrn, 0, 1, 1, 1)
        ogrid.attach(oaim, 0, 2, 1, 1)
        ogrid.set_column_homogeneous(True)

        opop.add(ogrid)

        spop = Gtk.Popover()
        spop.set_position(Gtk.PositionType.BOTTOM)

        sbrn = self.modelbutton(_("Save .brn file ..."))
        sbrn.connect("clicked", self.on_sbrn_clicked)

        scht = self.modelbutton(_("Save conversation ..."))
        scht.connect("clicked", self.on_scht_clicked)

        sgrid = Gtk.Grid()
        sgrid.set_property("margin", 5)
        sgrid.attach(sbrn, 0, 1, 1, 1)
        sgrid.attach(scht, 0, 2, 1, 1)
        sgrid.set_column_homogeneous(True)

        spop.add(sgrid)

        logo = Gtk.Image()
        logo.set_from_file("icons/aiml-gtk-logo.png")

        lbtn = Gtk.Button()
        lbtn.set_image(logo)
        lbtn.set_relief(Gtk.ReliefStyle.NONE)
        lbtn.connect("clicked", lambda x: dialogs().about(self))

        obtn = Gtk.ToolButton.new_from_stock(Gtk.STOCK_OPEN)
        obtn.connect("clicked", self.on_obtn_clicked)

        sbtn = Gtk.ToolButton.new_from_stock(Gtk.STOCK_SAVE)
        sbtn.connect("clicked", self.on_sbtn_clicked)

        bar.pack_start(lbtn)
        bar.pack_start(obtn)
        bar.pack_start(sbtn)

        sw = Gtk.ScrolledWindow()
        sw.set_hexpand(True)
        sw.set_vexpand(True)
        sw.set_shadow_type(Gtk.ShadowType.IN)
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)

        console = Gtk.TextView()
        console.set_top_margin(10)
        console.set_left_margin(10)
        console.set_wrap_mode(Gtk.WrapMode.WORD)
        console.set_editable(False)

        sw.add(console)

        box.set_property("margin", 10)
        box.pack_start(entry, True, True, 5)
        box.pack_end(cbtn, False, False, 5)

        grid = Gtk.Grid()
        grid.attach(box, 0, 1, 1, 1)
        grid.attach(sw, 0, 2, 1, 1)
        grid.set_column_homogeneous(True)

        self.add(grid)
        self.opop = opop
        self.spop = spop
        self.entry = entry
        self.console = console
        self.loaded = False
        self.entry.grab_focus()

    def modelbutton(self, text):

        button = Gtk.ModelButton(text)
        button.set_alignment(0, 0.5)

        return button

    def reset(self):

        kern.resetBrain()
        self.console.get_buffer().set_text("")

    def on_obtn_clicked(self, widget):

        self.opop.set_relative_to(widget)
        self.opop.show_all()

    def on_sbtn_clicked(self, widget):

        self.spop.set_relative_to(widget)
        self.spop.show_all()

    def on_sbrn_clicked(self, widget):

        filename = dialogs().save(_("Save brain file (.brn)"))
        if filename: kern.saveBrain(filename)

    def on_scht_clicked(self, widget):

        filename = dialogs().save(_("Save chat file (.txt)"))

        if filename:

            buf = self.console.get_buffer()
            text = buf.get_text(buf.get_start_iter(),
                   buf.get_end_iter(),
                   True)
    
            try: open(filename, 'w').write(text)
            except: dialogs().error(_("Save failed"), "{} {}".format(_("Could not save"), filename))

    def on_obrn_clicked(self, widget):

        filename = dialogs().open_brain()

        if filename:

            self.reset()

            try:
                kern.bootstrap(brainFile = filename)
                self.console.get_buffer().set_text("\"{}\" {}.\n".format(
                os.path.basename(filename), _("has been loaded")))

            except:
                self.console.get_buffer().set_text("\"{}\" {}".format(
                os.path.basename(filename), _("file could be corrupted or invalid")))
                return True

            self.loaded = True
            self.entry.grab_focus()

    def on_oaim_clicked(self, widget):

        filenames = dialogs().open_aiml()

        if filenames:

            self.reset()
            buf = self.console.get_buffer()
            itr = buf.get_end_iter()

            for i in filenames:

                try:
                    kern.bootstrap(learnFiles = i)
                    buf.insert(itr, "\"{}\" {}.\n".format(
                    os.path.basename(i), _("has been loaded")))

                except:
                    self.console.get_buffer().set_text("\"{}\" {}".format(
                    os.path.basename(i), _("file could be corrupted or invalid")))
                    return True

            self.loaded = True
            self.entry.grab_focus()

    def chat(self, widget):

        if not self.loaded:
            dialogs().error(_("Kernel have no files loaded"), _("Load some file(s) before to chat"))
            return True

        if type(widget) != Gtk.Entry: widget = self.entry
        if not widget.get_text(): return True

        buf = self.console.get_buffer()
        itr = buf.get_end_iter()

        answer = kern.respond(widget.get_text())
        if not answer: answer = "{}: {}".format(_("No match found for input"), widget.get_text())

        buf.insert(itr, "\n{}: {}\n".format("HUMAN", widget.get_text()))
        buf.insert(itr, "{}: {}\n".format("AI", answer))

        widget.set_text("")
        self.console.scroll_mark_onscreen(buf.get_insert())

win = main()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

