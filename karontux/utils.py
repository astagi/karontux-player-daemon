import threading

class AsyncAction(threading.Thread):

    def __init__(self, func, callback=None, *args, **kwargs):
        threading.Thread.__init__(self)
        self._result = None
        self._is_finished = False
        self._callback = callback
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self.start()

    def run(self):
        self._result = self._func(*self._args, **self._kwargs)
        self._is_finished = True
        if self._callback:
            self._callback(result)

    def is_finished(self):
        return self._is_finished

    def get_result(self):
        return self._result
