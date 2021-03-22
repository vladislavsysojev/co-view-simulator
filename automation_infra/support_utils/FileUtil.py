import csv
import os
import shutil

import yaml


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
            print('Failed to delete %s. Reason: %s' % (file_path, e))


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
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def parseCsvToObjectList(any_class, csv_file):
    my_list = []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            my_list.append(any_class(*row))
    return my_list


def replace_master_yaml_value(file_path, value):
    with open(file_path) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        yaml_list = yaml.load(file, Loader=yaml.FullLoader)
    yaml_list["spec"]["template"]["spec"]["containers"][0]["env"][1]["value"] = value
    with open(file_path, 'w') as file:
        yaml.dump(yaml_list, file)


def replace_worker_yaml_value(file_path, host, expected_workers_num):
    with open(file_path) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        yaml_list = yaml.load(file, Loader=yaml.FullLoader)
    yaml_list["spec"]["template"]["spec"]["containers"][0]["env"][2]["value"] = host
    yaml_list["spec"]["replicas"] = expected_workers_num
    with open(file_path, 'w') as file:
        yaml.dump(yaml_list, file)
