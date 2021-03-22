import os
from os import getenv as os_getenv
import logging
import sys
import time
import datetime
import requests
from locust import HttpUser, TaskSet, task, between, constant_pacing, tag, events
from locust.runners import MasterRunner, Runner
from locust.runners import WorkerRunner
from locust.runners import LocalRunner
from locust.contrib.fasthttp import FastHttpUser
import json
# import common.config
import uuid
import random

from automation_infra.automation_log_config.automation_log import LOGGER


def create_room_as_setup(environment, request_path, room_num):
    if isinstance(environment.runner, Runner or MasterRunner):
        LOGGER.info("Create rooms procces in progress...")
        time.sleep(1)
        for i in range(room_num):
            time.sleep(0.5)
            with requests.post(environment.host + "/coview/room", data=json.dumps({
                "creator": {
                    "id": str(uuid.uuid4()),
                    "name": "Automation User"
                },
                "initialState": "PLAY",
                "initialPosition": "0",
                "content": {
                    "id": common.config.CONTENT_ID,
                    "playbackUrls": common.config.PLAYBACK_URLS
                },
                "roomInformation": {}}), headers=common.config.HEADERS) as response:
                if response.status_code == 200:
                    LOGGER.info("Request url: {}".format(response.request.url) + "; Response code: {}".format(
                        response.status_code) + "; Response body: {}".format(response.content))
                else:
                    LOGGER.error("Request url: {}".format(response.request.url) + "; Response code: {}".format(
                        response.status_code) + "; Response body: {}".format(response.content))
                    requests.post(environment.host + "/coview/room", data=json.dumps({
                        "creator": {
                            "id": str(uuid.uuid4()),
                            "name": common.config.USER_NAME
                        },
                        "initialState": "PLAY",
                        "initialPosition": "0",
                        "content": {
                            "id": common.config.CONTENT_ID,
                            "playbackUrls": common.config.PLAYBACK_URLS
                        },
                        "roomInformation": {}}), headers=common.config.HEADERS)
        with requests.get(environment.host + "/coview/room", headers=common.config.HEADERS) as response:
            json_response_dict = response.json()
            room_number = json_response_dict['rooms']
            for room in room_number:
                common.config.rooms_list.append(room)
        LOGGER.info("Room list: {}".format(common.config.rooms_list))
        LOGGER.info("{} rooms are available".format(len(common.config.rooms_list)))
        if len(common.config.rooms_list) == common.config.NUMBER_OF_ROOMS:
            pass
        else:
            LOGGER.error("Wrong number of rooms, please restart!")
            quit()

    elif isinstance(environment.runner, WorkerRunner) and common.config.DISTRIBUTED_MODE == True:
        with requests.get(common.config.HOST + "/coview/room", headers=common.config.HEADERS) as response:
            json_response_dict = response.json()
            room_number = json_response_dict['rooms']
            for room in room_number:
                common.config.rooms_list.append(room)
        LOGGER.info("Room list: {}".format(common.config.rooms_list))
        LOGGER.info("{} rooms are available".format(len(common.config.rooms_list)))
        if len(common.config.rooms_list) == common.config.NUMBER_OF_ROOMS:
            pass
        else:
            LOGGER.error("Wrong number of rooms, please restart!")
            quit()
    else:
        LOGGER.error("Please set the parameter DISTRIBUTED_MODE to True in common/config.py")
        quit()