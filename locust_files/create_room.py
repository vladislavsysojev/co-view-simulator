import json
import random
import uuid

from locust import task, TaskSet, constant, HttpUser, events
import locust_files.locust_templates as temp

# from automation_infra.requests_api.rest_api_request_data import login_data, create_device_id

# @events.test_start.add_listener
# def on_test_start(environment, **kwargs):
#     global room_content_ids
#     room_content_ids = [str(uuid.uuid4()) for x in range(4)]
#     print("A new test is starting")

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
        create_room_data["content"]["id"] = str(random.randint(1, 4))
        self.response = self.client.post("/v1/users/connect", name="Connect",
                                         headers={"Content-Type": "application/json", "USER_ID": user_id,
                                                  "DEVICE_ID": device_id}, json=login_data)
        if self.response.status_code == 200:
            create_room_data["creator"]["id"] = user_id
            self.response = self.client.post("/v1/rooms", name="Create room host web app",
                                             headers={"Content-Type": "application/json", "USER_ID": user_id,
                                                      "DEVICE_ID": device_id},
                                             json=create_room_data)

    @task
    def keep_alive(self):
        pass


class CreateRoom(HttpUser):
    tasks = [CreteRoomUser]
    wait_time = constant(1)
    weight = 1
