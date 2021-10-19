import threading
import ctypes

class Thread(threading.Thread):

    def __init__(self, routine, *args):
        threading.Thread.__init__(self)
        self.routine = routine

    def Run(self, *args):
        self.routine(*args)

    def GetID(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def Kill(self):
        threadID = self.GetID()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(threadID,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(threadID, 0)
            print('[ERREUR] Impossible de tuer le Thread ', threadID)