import multiprocessing
import selectors
import subprocess

import re
import time
# import StringIO

from multiprocessing import Pool
from gevent.lock import RLock
from functools import partial

from automation_infra.automation_log_config.automation_log import ILog

lock = RLock()
iterator = 0
log = ILog("Support Utils")


def createUnigueName(name):
    with lock:
        global iterator
        iterator += 1
        return str.format("{0}{1}", name, iterator)


def parseTime(time):
    if isinstance(time, str):
        l = list(map(int, re.split('[hms]', time)[:-1]))
        if len(l) == 3:
            return l[0] * 3600 + l[1] * 60 + l[2]
        elif len(l) == 2:
            return l[0] * 60 + l[1]
        else:
            return l[0]
    else:
        return time


def runCmd(cmd):
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # output, error = process.communicate()
    # log.debug(StringIO(output))
    sel = selectors.DefaultSelector()
    sel.register(process.stdout, selectors.EVENT_READ)
    sel.register(process.stderr, selectors.EVENT_READ)
    while True:
        for key, _ in sel.select():
            data = key.fileobj.read1().decode()
            if not data:
                # exit()
                return
            if key.fileobj is process.stdout:
                log.debug("\n" + data)
                # print(data, end="")
            else:
                # print(data, end="", file=sys.stderr)
                log.debug("\n" + data)
                # print(data, end="")


def runMultipleCmdsAsync(cmds):
    process_list = []
    for cmd in cmds.split(";"):
        process_list.append(subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
    main_process = process_list[0]

    sel = selectors.DefaultSelector()
    sel.register(main_process.stdout, selectors.EVENT_READ)
    sel.register(main_process.stderr, selectors.EVENT_READ)
    while True:
        for key, _ in sel.select():
            data = key.fileobj.read1().decode()
            if not data:
                # exit()
                return
            if key.fileobj is main_process.stdout:
                print(data, end="")
            else:
                # print(data, end="", file=sys.stderr)
                print(data, end="")

# l = multiprocessing.Lock()
# def runMultipleCmds(cmds):
#     pool = multiprocessing.Pool(initializer=init, initargs=(l,))
#     pool.map(runCmdInMultiprocess, cmds.split(";"))
#     pool.close()
#     pool.join()
#
#
# def init(l):
#     global lock
#     lock = l
