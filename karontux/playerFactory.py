from pykaraoke.pykar import midPlayer
from pykaraoke.pycdg import cdgPlayer
from pykaraoke.pympg import mpgPlayer

class playerFactory(object):
    
    def __init__(self, path, windowTitle = None,
                 errorNotifyCallback = None, doneCallback = None,
                 quitCallback = None):

        self.__path = path
        self.__errorNotifyCallback = errorNotifyCallback
        self.__doneCallback = doneCallback
        self.__quitCallback = quitCallback
        self.__windowTitle = windowTitle

    def create(self):
        if self.__path.endswith(".kar") or self.__path.endswith(".mid"):
            return midPlayer(self.__path, None,
                             self.__errorNotifyCallback, self.__doneCallback,
                             self.__windowTitle, self.__quitCallback)
        elif self.__path.endswith(".cdg"):
            return cdgPlayer(self.__path, None,
                             self.__errorNotifyCallback, self.__doneCallback,
                             self.__windowTitle, self.__quitCallback)
        else:
            return None
