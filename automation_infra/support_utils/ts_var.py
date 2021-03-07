import threading
from gevent.lock import RLock

lock = RLock()


class Ts_Var(object):
    _instance = None
    _dataDict = {}

    @classmethod
    def Instance(cls):
        if cls._instance == None:
            cls._instance = Ts_Var()
        return cls._instance

    def __init__(self):
        if self._instance != None:
            raise ValueError("Ts_Var instance is already exist use 'TS_Var.Instance()'")

    def setTs_Var(self, key, value):
        with lock:
            self._dataDict[key] = value


    def getTs_Var(self, key):
        return self._dataDict[key]

    def print_all(self):
        for key, val in self._dataDict.items():
            print(str.format("{0} : {1}", key, self._dataDict[key]))
