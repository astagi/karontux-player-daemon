from karontux.playerFactory import playerFactory
from pykaraoke.pykmanager import manager
from pykaraoke.pykconstants import *
from karontux.daemon import Daemon
from karontux.utils import *

import dbus, dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import gobject, signal, time, sys

BUS_NAME = "org.karon.tux"
PLAYER_PATH = "/org/karon/tux/player"

class KarontuxPlayer(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName(BUS_NAME, bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, PLAYER_PATH)
        self.player = None
        self.mutex = threading.Semaphore(1)
        self.elab = True

        def elaborate():
            while self.elab:
                if self.player and self.player.State != STATE_CLOSED:
                    self.mutex.acquire()
                    manager.Poll()
                    self.mutex.release()

        AsyncAction(elaborate)

    @dbus.service.method(BUS_NAME)
    def play(self, path):
        if self.player != None:
            self.stop()
        self.mutex.acquire()
        self.player = playerFactory(path, "Karontux", None,
                                    self.songFinished, self.windowQuit).create()
        self.mutex.release()

        if self.player == None:
            return

        def play_async():
            self.mutex.acquire()
            self.player.Play()
            self.mutex.release()

        AsyncAction(play_async)

    @dbus.service.signal(BUS_NAME)
    def windowQuit(self):
        self.close()
        manager.Quit()
        self.shutdown()

    @dbus.service.signal(BUS_NAME)
    def songFinished(self):
        pass

    @dbus.service.method(BUS_NAME)
    def stop(self):
        if self.player == None:
            return
        self.mutex.acquire()
        self.player.Stop()
        self.mutex.release()

    @dbus.service.method(BUS_NAME)
    def pause(self):
        if self.player == None:
            return
        self.mutex.acquire()
        self.player.Pause()
        self.mutex.release()

    def close(self):
        self.elab = False
 
    def shutdown(self):
        self.player = None

 
class KarontuxDaemon(Daemon):

    def __init__(self, path, stderr=None):
        Daemon.__init__(self, path, stderr=stderr)
        self.quit = False

    def stop(self):
        Daemon.stop(self)

    def run(self):
        mainloop = None
        player_service = None
        DBusGMainLoop(set_as_default=True)

        def quitMainLoop(arg1, arg2):
            player_service.close()
            manager.Quit()
            mainloop.quit()

        player_service = KarontuxPlayer()

        signal.signal(signal.SIGTERM, quitMainLoop)

        gobject.threads_init()
        dbus.mainloop.glib.threads_init()
        mainloop = gobject.MainLoop()
        mainloop.run()
 
if __name__ == "__main__":

    daemon = KarontuxDaemon('/tmp/karontux-daemon.pid', '/home/andrea/w/daemon')

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
