import subprocess
import random
import selectors
import string
import re
import time
# import StringIO

from multiprocessing import Pool
from gevent.lock import RLock
from functools import partial

from automation_infra.automation_log_config.automation_log import ILog

lock = RLock()
iterator = 1
log = ILog("Support Utils")
names_diff = []
single_unique_name = ""


def createUnigueName(name):
    with lock:
        if name not in names_diff:
            names_diff.append(name)
        else:
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
    result = ''
    output_str = ''
    error_str = ''
    if cmd:
        process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        sel = selectors.DefaultSelector()
        sel.register(process.stdout, selectors.EVENT_READ)
        sel.register(process.stderr, selectors.EVENT_READ)

        while True:
            for key, _ in sel.select():
                data = key.fileobj.read1().decode()
                if not data:
                    # exit()
                    return result
                if key.fileobj is process.stdout:
                    log.debug("\n" + data)
                    result += "\n" + data
                    # print(data, end="")
                else:
                    # print(data, end="", file=sys.stderr)
                    log.debug("\n" + data)
                    result += "\n" + data
                    # print(data, end="")
    #     error, output = process.communicate()
    #     if output:
    #         output_str = StringIO(output.decode('utf-8')).read()
    #     if error:
    #         error_str = StringIO(error.decode('utf-8')).read()
    #     log.debug(output_str)
    #     log.debug(error_str)
    #     result += output_str
    return result


def create_global_unique_name(name, length):
    """
    Creates unique name with random characters range at the end of name
    @param name: name
    @type name: str
    @param length: length of random characters
    @type length: int
    @return: unique name
    @rtype: str
    """
    unique_str = "".join(random.choice(string.ascii_letters) for x in range(length))
    return str.lower(f"{name}{unique_str}")


def create_global_unique_name_once(name, length):
    """
    Creates unique name with random characters range at the end of name
    @param name: name
    @type name: str
    @param length: length of random characters
    @type length: int
    @return: unique name
    @rtype: str
    """
    global single_unique_name
    if name not in names_diff:
        names_diff.append(name)
        unique_str = "".join(random.choice(string.ascii_letters) for x in range(length))
        single_unique_name = str.lower(f"{name}{unique_str}")
    return single_unique_name


def runMultipleCmdsAsync(cmds):
    process_list = []
    for cmd in cmds.split(";"):
        process_list.append(
            subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
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
