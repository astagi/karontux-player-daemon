import dbus, dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import gobject, signal, time, sys

BUS_NAME = "org.karon.tux"
PLAYER_PATH = "/org/karon/tux/player"

#DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
player_service = bus.get_object(BUS_NAME, PLAYER_PATH)

argc = len(sys.argv)

if argc > 1:
    action = sys.argv[1]
if argc > 2:
    file_path = sys.argv[2]

print "You selected %s action" % action

"""def handleWindowQuit():
    print "Window quit"

def handleSongFinished():
    print "Song finished"

player_service.connect_to_signal("windowQuit", handleWindowQuit)
player_service.connect_to_signal("songFinished", handleSongFinished)"""

if action == 'play':
    player_service.play(file_path)
elif action == 'stop':
    player_service.stop()
elif action == 'pause':
    player_service.pause()

"""mainloop = gobject.MainLoop()
mainloop.run()"""
