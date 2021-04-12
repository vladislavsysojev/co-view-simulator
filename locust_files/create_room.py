import copy
import json
import random
import uuid

from locust import task, TaskSet, between, constant, HttpUser, events
from locust.contrib.fasthttp import FastHttpUser
from locust.env import Environment
from locust.runners import MasterRunner

import locust_files.locust_templates as temp

room_content_ids = [str(uuid.uuid4()) for x in range(4)]
temp.room_content_ids = room_content_ids


class CreteRoomUser(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    def on_start(self):
        user_id = str(uuid.uuid4())
        device_id = str(uuid.uuid4())
        login_data = temp.login_data.copy()
        login_data["userId"] = user_id
        login_data["device"]["id"] = device_id
        create_room_data = temp.create_room_data.copy()
        create_room_data["creator"]["id"] = user_id
        create_room_data["content"]["id"] = temp.room_content_ids[random.randint(0, 3)]
        access_token_data = copy.deepcopy(temp.access_token_data)
        access_token_data["userId"] = user_id
        access_token_data["deviceId"] = device_id
        response = self.client.post("/v1/auth/generateEngagementToken", name="Generate access token",
                                    headers={"Content-Type": "application/json", "USER_ID": user_id},
                                    json=access_token_data)
        if response.status_code == 200:
            access_token = json.loads(response.text)["auth"]["accessToken"]
            self.response = self.client.post("/v1/users/connect", name="Connect",
                                             headers={"Content-Type": "application/json",
                                                      "Authorization": access_token, "USER_ID": user_id,
                                                      "DEVICE_ID": device_id}, json=login_data)
            if self.response.status_code == 200:
                create_room_data["creator"]["id"] = user_id
                self.response = self.client.post("/v1/rooms", name="Create room host web app",
                                                 headers={"Content-Type": "application/json",
                                                          "Authorization": access_token, "USER_ID": user_id,
                                                          "DEVICE_ID": device_id},
                                                 json=create_room_data)

    @task
    def keep_alive(self):
        pass


class CreateRoom(FastHttpUser):
    tasks = [CreteRoomUser]
    wait_time = constant(1)
    weight = 1
