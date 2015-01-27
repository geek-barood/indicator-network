# @Author Aniruddha Hazra
# @Date 27-Jan-2014
#

from gi.repository import Gtk, GLib
import os
try:
       from gi.repository import AppIndicator3 as AppIndicator  
except:
       from gi.repository import AppIndicator

class IndicatorNetwork:

    REMOTE_SERVER = "www.google.com"
    connection_status = "Disconnected"
    icon_path = os.getcwd() + "/icons/"
    icon_disconnected = icon_path + "icon-disconnected.svg"
    icon_connected = icon_path + "icon-connected.svg"
    def __init__(self):
        # @param1: identifier of this indicator
        # @param2: name of icon. this will be searched for in the standard theme
        # dirs or the given path
        # @param3: category of the indicator
        self.ind = AppIndicator.Indicator.new(
                            "indicator-network", 
                            self.icon_disconnected,
                            AppIndicator.IndicatorCategory.SYSTEM_SERVICES)

        # need to set this for indicator to be shown
        self.ind.set_status (AppIndicator.IndicatorStatus.ACTIVE)

        # have to give indicator a menu
        self.menu = Gtk.Menu()

        # menu item for showing the readable text 
        item = Gtk.MenuItem()
        item.set_label(self.connection_status)
        # item.connect("activate", self.handler_menu_method)
        item.show()
        self.menu.append(item)

        # this is for exiting the app
        item = Gtk.MenuItem()
        item.set_label("Quit")
        item.connect("activate", self.handler_menu_exit)
        item.show()
        self.menu.append(item)

        self.menu.show()
        self.ind.set_menu(self.menu)

        # update every 2 seconds
        GLib.timeout_add_seconds(3, self.handler_timeout)

    def is_connected(self):
        print_debug("trying to connect...")
        resp = os.system("ping -c 1 -w 2 " + self.REMOTE_SERVER +
                " > /dev/null 2>&1")
        if resp == 0:
            return True
        return False

    def handler_menu_exit(self, evt):
        Gtk.main_quit()

    def handler_timeout(self):

        connected = self.is_connected()
        if connected is True:
            self.ind.set_icon(self.icon_connected)
            self.connection_status = "Connected"
        else:
            self.ind.set_icon(self.icon_disconnected)
            self.connection_status = "Disconnected"

        for i in self.menu.get_children():
            if i.get_label() == "Disconnected" or i.get_label() == "Connected":
                i.set_label(self.connection_status)
                break

        # return True so that we get called again
        # returning False will make the timeout stop
        return True

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    ind = IndicatorNetwork()
    if not __debug__:
        def print_debug(message): pass
    else:
        def print_debug(message): print message
    ind.main()
