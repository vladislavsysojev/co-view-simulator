"""
Engagement cloud longevity end to end load test locust file
"""

import json
import random
import time
import uuid
import copy

from locust import task, TaskSet, constant, HttpUser
import locust_files.locust_templates as temp


class CoViewEndToEndLongevity(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.register_channel_data = copy.deepcopy(temp.register_channel_data)
        self.join_room_data = copy.deepcopy(temp.join_room_data)
        self.create_room_data = copy.deepcopy(temp.create_room_data)
        self.attach_data = copy.deepcopy(temp.attach_data)
        self.enter_pin_data = copy.deepcopy(temp.enter_pin_data)
        self.create_device_id = copy.deepcopy(temp.create_device_id)
        self.login_data_sdk = copy.deepcopy(temp.login_data)
        self.login_data_web_app = copy.deepcopy(temp.login_data)
        self.pin_data = copy.deepcopy(temp.pin_data)
        self.leave_room_data = copy.deepcopy(temp.leave_room_data)
        self.disconnect_data = copy.deepcopy(temp.disconnect_data)
        self.access_token_data = copy.deepcopy(temp.access_token_data)

        self.users_dict = {}

    def on_start(self):
        self.create_requests_data()
        room_id = self.host_tasks()
        for participant in range(3):
            self.create_requests_data()
            time.sleep(1)
            self.participant_tasks(room_id, participant)
        time.sleep(120)
        self.leave_room(room_id)

    def leave_room(self, room_id):
        participant_counter = 0
        is_host = True
        for access_token, user_data in self.users_dict.items():
            self.leave_room_data["userId"] = user_data["userId"]
            self.leave_room_data["deviceId"] = user_data["deviceId"]
            self.disconnect_data["userId"] = user_data["userId"]
            self.disconnect_data["deviceId"] = user_data["deviceId"]
            if is_host:
                is_host = False
                name_leave = "Leave room host web app"
                name_disconnect = "Disconnect user host web app"
            else:
                name_leave = f"Leave room participant {str(participant_counter)} web app"
                name_disconnect = f"Disconnect user participant {str(participant_counter)} web app "
                participant_counter += 1
            if room_id:
                self.client.post(f"/v1/rooms/{room_id}/leave", name=name_leave,
                                 headers={"Content-Type": "application/json",
                                          "Authorization": access_token, "USER_ID": self.user_id,
                                          "DEVICE_ID": self.device_id_sdk}, json=self.leave_room_data)

            self.client.post(f"/v1/users/disconnect", name=name_disconnect,
                             headers={"Content-Type": "application/json",
                                      "Authorization": access_token, "USER_ID": self.user_id,
                                      "DEVICE_ID": self.device_id_sdk}, json=self.disconnect_data)

    def create_requests_data(self):
        self.user_id = str(uuid.uuid4())
        self.device_id_sdk = str(uuid.uuid4())
        self.device_id_web_app = str(uuid.uuid4())
        self.login_data_sdk["userId"] = self.user_id
        self.login_data_sdk["device"]["id"] = self.device_id_sdk
        self.login_data_web_app["userId"] = self.user_id
        self.login_data_web_app["device"]["id"] = self.device_id_web_app
        self.create_device_id["deviceId"] = self.device_id_sdk
        self.pin_data["payload"] = self.user_id
        self.attach_data["deviceId"] = self.device_id_web_app
        self.create_room_data["creator"]["id"] = self.user_id
        self.create_room_data["content"]["id"] = str(random.randint(5, 8))
        self.join_room_data["userId"] = self.user_id
        self.join_room_data["deviceId"] = self.device_id_web_app
        self.register_channel_data["userId"] = self.user_id
        self.register_channel_data["deviceId"] = self.device_id_web_app
        self.access_token_data["applicationKey"] = temp.read_file("/locust_files/app_key.txt")
        self.access_token_data["userId"] = self.user_id
        self.access_token_data["deviceId"] = self.device_id_sdk

    def host_tasks(self):
        room_id = ""
        response = self.client.post("/v1/auth/generateEngagementToken", name="Generate access token host",
                                    headers={"Content-Type": "application/json", "USER_ID": self.user_id},
                                    json=self.access_token_data)
        if response.status_code == 200:
            access_token = json.loads(response.text)["auth"]["accessToken"]
            self.users_dict[access_token] = {"userId": self.user_id, "deviceId": self.device_id_web_app}
            response = self.client.post("/v1/users/connect", name="Connect host sdk",
                                        headers={"Content-Type": "application/json",
                                                 "Authorization": access_token, "USER_ID": self.user_id,
                                                 "DEVICE_ID": self.device_id_sdk},
                                        json=self.login_data_sdk)
            if response.status_code == 200:
                response = self.client.post(f"/v1/users/{self.user_id}/deviceGroups",
                                            name="Create device group host sdk",
                                            headers={"Content-Type": "application/json",
                                                     "Authorization": access_token, "USER_ID": self.user_id,
                                                     "DEVICE_ID": self.device_id_sdk}, json=self.create_device_id)
                device_group_id = ""
                if response.status_code == 200:
                    device_group_id = json.loads(response.text)["deviceGroupId"]

                response = self.client.post("/v1/pin", name="Generate pin host sdk",
                                            headers={"Content-Type": "application/json",
                                                     "Authorization": access_token, "USER_ID": self.user_id}
                                            , json=self.pin_data)
                time.sleep(random.randint(1, 3))
                if response.status_code == 200:
                    self.enter_pin_data["pin"] = json.loads(response.text)["pin"]
                    response = self.client.post("/v1/users/connect", name="Connect host web app",
                                                headers={"Content-Type": "application/json",
                                                         "Authorization": access_token,
                                                         "USER_ID": self.user_id,
                                                         "DEVICE_ID": self.device_id_web_app},
                                                json=self.login_data_web_app)

                    if response.status_code == 200:
                        self.client.put("/v1/pin", name=f"Enter pin host web app",
                                        headers={"Content-Type": "application/json",
                                                 "Authorization": access_token},
                                        data=json.dumps(self.enter_pin_data))
                        if device_group_id:
                            self.client.post(
                                f"/v1/users/{self.user_id}/deviceGroups/{device_group_id}/attach",
                                name="Attach host web app",
                                headers={"Content-Type": "application/json", "Authorization": access_token,
                                         "DEVICE_ID": self.device_id_web_app},
                                json=self.attach_data)

                        response = self.client.post("/v1/rooms", name="Create room host web app",
                                                    headers={"Content-Type": "application/json",
                                                             "Authorization": access_token,
                                                             "USER_ID": self.user_id,
                                                             "DEVICE_ID": self.device_id_web_app},
                                                    json=self.create_room_data)

                        if response.status_code == 200:
                            room_id = json.loads(response.text)["roomId"]
                            response = self.client.post(f"/v1/rooms/{room_id}/join", name="Join room host web app",
                                                        headers={"Content-Type": "application/json",
                                                                 "USER_ID": self.user_id,
                                                                 "Authorization": access_token,
                                                                 "DEVICE_ID": self.device_id_web_app,
                                                                 "ROOM_ID": room_id},
                                                        json=self.join_room_data)

                            if response.status_code == 200:
                                self.client.post(f"/v1/rooms/{room_id}/channels",
                                                 name="Register channel host web app",
                                                 headers={"Content-Type": "application/json",
                                                          "USER_ID": self.user_id,
                                                          "Authorization": access_token,
                                                          "DEVICE_ID": self.device_id_web_app},
                                                 json=self.register_channel_data)

        return room_id

    def participant_tasks(self, room_id, participant_num):
        if room_id:
            response = self.client.post("/v1/auth/generateEngagementToken",
                                        name=f"Generate access token participant {str(participant_num)}",
                                        headers={"Content-Type": "application/json", "USER_ID": self.user_id},
                                        json=self.access_token_data)
            if response.status_code == 200:
                access_token = json.loads(response.text)["auth"]["accessToken"]
                self.users_dict[access_token] = {"userId": self.user_id, "deviceId": self.device_id_web_app}
                response = self.client.post("/v1/users/connect",
                                            name="Connect participant " + str(participant_num) + " sdk",
                                            headers={"Content-Type": "application/json", "USER_ID": self.user_id,
                                                     "Authorization": access_token,
                                                     "DEVICE_ID": self.device_id_sdk}, json=self.login_data_sdk)
                if response.status_code == 200:
                    response = self.client.post(f"/v1/users/{self.user_id}/deviceGroups",
                                                name="Create device group participant sdk " + str(participant_num),
                                                headers={"Content-Type": "application/json", "USER_ID": self.user_id,
                                                         "Authorization": access_token,
                                                         "DEVICE_ID": self.device_id_sdk}, json=self.create_device_id)
                    device_group_id = ""
                    if response.status_code == 200:
                        device_group_id = json.loads(response.text)["deviceGroupId"]

                    response = self.client.post("/v1/pin", name="Generate pin participant sdk " + str(participant_num),
                                                headers={"Content-Type": "application/json", "USER_ID": self.user_id,
                                                         "Authorization": access_token},
                                                json=self.pin_data)
                    if response.status_code == 200:
                        self.enter_pin_data["pin"] = json.loads(response.text)["pin"]
                        response = self.client.post("/v1/users/connect",
                                                    name="Connect participant " + str(participant_num) + " web app",
                                                    headers={"Content-Type": "application/json",
                                                             "USER_ID": self.user_id,
                                                             "Authorization": access_token,
                                                             "DEVICE_ID": self.device_id_web_app},
                                                    json=self.login_data_web_app)

                        if response.status_code == 200:
                            self.client.put("/v1/pin",
                                            name=f"Enter pin participant web app" + str(participant_num),
                                            headers={"Content-Type": "application/json",
                                                     "Authorization": access_token},
                                            data=json.dumps(self.enter_pin_data))
                            if device_group_id:
                                self.client.post(
                                    f"/v1/users/{self.user_id}/deviceGroups/{device_group_id}/attach",
                                    name="Attach participant web app" + str(participant_num),
                                    headers={"Content-Type": "application/json",
                                             "Authorization": access_token,
                                             "DEVICE_ID": self.device_id_web_app}, json=self.attach_data)

                                response = self.client.post(f"/v1/rooms/{room_id}/join",
                                                            name="Join room participant web app " + str(
                                                                participant_num),
                                                            headers={"Content-Type": "application/json",
                                                                     "Authorization": access_token,
                                                                     "USER_ID": self.user_id,
                                                                     "DEVICE_ID": self.device_id_web_app,
                                                                     "ROOM_ID": room_id},
                                                            json=self.join_room_data)
                                if response.status_code == 200:
                                    self.client.post(f"/v1/rooms/{room_id}/channels",
                                                     name="Register channel participant web app" + str(participant_num),
                                                     headers={"Content-Type": "application/json",
                                                              "Authorization": access_token,
                                                              "USER_ID": self.user_id,
                                                              "DEVICE_ID": self.device_id_web_app},
                                                     json=self.register_channel_data)

    @task
    def keep_alive(self):
        pass


class CoViewEndToEndLongevityUser(HttpUser):
    tasks = [CoViewEndToEndLongevity]
    wait_time = constant(2)
    weight = 1
