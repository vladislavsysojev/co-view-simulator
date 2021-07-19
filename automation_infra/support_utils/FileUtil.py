import csv
import os
import shutil

import yaml

from automation_infra.automation_log_config.automation_log import ILog

log = ILog("File Util")


def getFullPath(folder):
    currentDirectory = os.getcwd()
    return os.path.join(currentDirectory, folder)


def cleanupFilesFromLocalDir(folder):
    full_path = getFullPath(folder)
    for filename in os.listdir(full_path):
        file_path = os.path.join(full_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            log.info('Failed to delete %s. Reason: %s' % (file_path, e))


def createLocalFileOrDir(name):
    full_path = getFullPath(name)
    if not os.path.isdir(full_path):
        os.mkdir(full_path)


def cleanupDir(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            log.info('Failed to delete %s. Reason: %s' % (file_path, e))


def parseCsvToObjectList(any_class, csv_file):
    my_list = []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            my_list.append(any_class(*row))
    return my_list


def replace_master_yaml_value(file_path, value, image):
    """
    TODO: to make function replace any yaml values
    """
    with open(file_path) as file:
        yaml_list = yaml.load(file, Loader=yaml.FullLoader)
    yaml_list["spec"]["template"]["spec"]["containers"][0]["env"][1]["value"] = value
    yaml_list["spec"]["template"]["spec"]["containers"][0]["image"] = image
    with open(file_path, 'w') as file:
        yaml.dump(yaml_list, file)


def replace_worker_yaml_value(file_path, host, expected_workers_num, image):
    """
    TODO: to make function replace any yaml values
    """
    with open(file_path) as file:
        yaml_list = yaml.load(file, Loader=yaml.FullLoader)
    yaml_list["spec"]["template"]["spec"]["containers"][0]["env"][2]["value"] = host
    yaml_list["spec"]["replicas"] = int(expected_workers_num)
    yaml_list["spec"]["template"]["spec"]["containers"][0]["image"] = image
    with open(file_path, 'w') as file:
        yaml.dump(yaml_list, file)


def create_text_file(file_path, text):
    file = open(file_path, "w")
    file.write(text)
    file.close()


def create_yml_file(file_path, text):
    with open(file_path, 'w') as file:
        yaml.dump(text, file)


def read_file_to_object_list(file_path):
    file = open(file_path, "r+")
    return file.read().split("\n")
