import json
import random
import time
import uuid

from locust import events

from locust_files.infra.create_room_setup import create_room_as_setup

# @events.init.add_listener
# def on_locust_init(environment, **kwargs):
#     create_room_as_setup(environment)
#     environment.host


from locust import task, TaskSet, constant

from automation_infra.requests_api import rest_api_request_data as req_data
from locust_files.infra.locust_infra import LocustTestUser

# user_id_host = ""
# user_id_parcipian = ""
# device_id = ""

create_device_id = {
    "deviceId": "{0}",
}

login_data = {
    "userId": "{0}",
    "device": {
        "id": "{1}",
        "name": "TV APP",
        "platform": "ANDROID",
        "capabilities": {
            "MEDIA_SYNC": "READ"
        }
    },
    "clientProtocols": [
        "FIRESTORE"
    ]
}

pin_data = {
    "payload": {
        "userId": "{0}",
        "creator": {
            "id": "user_1"
        },
        "content": {
            "id": "1111",
            "playbackUrls": [
                "https://svc43.main.sl.t-online.de/dlt3/out/u/hssfcbayern01_m.mpd",
                "https://svc43.main.sl.t-online.de/dlt3/out/u/hssfcbayern01_m.m3u8"
            ]
        },
        "roomInformation": {
            "homeTeam": "FC Würzburger Kickers",
            "homeTeamLogoUrl": "https://stg-zeus-telekomsport-   de.laola1.at/images/editorial/Mataracan/Logos_neu/FWK200x200.png?time=1544545891822&h=150",
            "awayTeam": "FC Bayern München II",
            "awayTeamLogoUrl": "https://stg-zeus-telekomsport-de.laola1.at/images/editorial/Logos/Fussball/Bundesliga/01_fc_bayern_200x200.png?time=1562156010808&h=150",
            "eventName": "FSV Zwickau - FC Ingolstadt",
            "competitionName": "3. Liga Spieltag 15",
            "scheduledStartTime": 1563623100000
        }
    }
}

enter_pin_data = {
    "pin": "{0}"
}

create_room_data = {
    "creator": {
        "id": "{0}"
    },
    "initialState": "PLAY",
    "initialPosition": 0,
    "content": {
        "id": "1111",
        "playbackUrls": [
            "https://svc43.main.sl.t-online.de/dlt3/out/u/hssfcbayern01_fm.mpd",
            "https://svc43.main.sl.t-online.de/dlt3/out/u/hssfcbayern01_fm.m3u8"
        ]
    },
    "roomInformation": {
        "homeTeam": "FC Würzburger Kickers",
        "homeTeamLogoUrl": "https://stg-zeus-telekomsport-de.laola1.at/images/editorial/Mataracan/Logos_neu/FWK200x200.png?time=1544545891822&h=150",
        "awayTeam": "FC Bayern München II",
        "awayTeamLogoUrl": "https://stg-zeus-telekomsport-de.laola1.at/images/editorial/Logos/Fussball/Bundesliga/01_fc_bayern_200x200.png?time=1562156010808&h=150",
        "eventName": "FSV Zwickau - FC Ingolstadt",
        "competitionName": "3. Liga Spieltag 15",
        "scheduledStartTime": 1563623100000
    }
}

attach_data = {
    "deviceId": "{0}"
}

join_room_data = {
    "userId": "{0}",
    "deviceId": "{1}",
    "name": "Andrew"
}

register_channel_data = {
    "userId": "{0}",
    "deviceId": "{1}",
    "channels": {
        "MEDIA_SYNC": {
            "mode": "READ",
            "playbackUrl": "http://hfdsjkhf"
        }
    }
}


class CoViewEndToEnd(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        # self.login_data = RequestData().login_data
        # self.create_device_id = RequestData().create_device_id

    # def on_start(self):
    def on_start(self):
        # user_id = "23d23ff32" + str(random.randint(1, 100000))
        # device_id = "h783hd" + str(random.randint(1, 100000))
        room_id = self.host_tasks()
        for participant in range(5):
            time.sleep(1)
            self.participant_tasks(room_id, participant)

    # @task
    # def index(self):
    #     self.response = self.client.post("/v1/users/connect", headers={"Content-Type": "application/json"},
    #                                      json=login_data)
    #     self.response = self.client.post(f"/v1/users/{user_id}/deviceGroups",
    #                                      headers={"Content-Type": "application/json"}, json=create_device_id)
    def host_tasks(self):

        user_id = str(uuid.uuid4())
        # login_data["userId"] = user_id
        device_id = str(uuid.uuid4())
        response = self.client.post("/v1/users/connect", name="Connect host sdk",
                                    headers={"Content-Type": "application/json"},
                                    json=json.loads(str.format(json.dumps(login_data), user_id, device_id)))

        # create_device_id["userId"] = user_id
        response = self.client.post(f"/v1/users/{user_id}/deviceGroups", name="Create device group host sdk",
                                    headers={"Content-Type": "application/json"},
                                    json=json.loads(str.format(json.dumps(create_device_id), device_id)))
        device_group_id = ""
        if response.status == 200:
            device_group_id = response["deviceGroupId"]

        response = self.client.post("/v1/pin", name="Generate pin host sdk",
                                    headers={"Content-Type": "application/json"},
                                    json=json.loads(str.format(json.dumps(pin_data), user_id)))
        pin = ""
        if response.status == 200:
            pin = response["pin"]

        response = self.client.post("/v1/users/connect", name="Connect host web app",
                                    headers={"Content-Type": "application/json"},
                                    json=json.loads(str.format(json.dumps(login_data), user_id, device_id)))

        response = self.client.put("/v1/pin", name="Enter pin host web app",
                                   headers={"Content-Type": "application/json"},
                                   data=str.format(json.dumps(enter_pin_data), pin))

        response = self.client.post(f"/v1/users/{user_id}/deviceGroups/{device_group_id}/attach",
                                    name="Attach host web app", headers={"Content-Type": "application/json"},
                                    json=json.loads(str.format(json.dumps(attach_data), device_id)))

        response = self.client.post("/v1/rooms", name="Create room host web app",
                                    headers={"Content-Type": "application/json"},
                                    json=json.loads(str.format(json.dumps(create_room_data), user_id)))
        room_id = ""
        if response.status == 200:
            room_id = response["roomId"]

        response = self.client.post(f"/v1/rooms/{room_id}/join", name="Join room host web app",
                                    headers={"Content-Type": "application/json"},
                                    json=json.loads(str.format(json.dumps(join_room_data), user_id, device_group_id)))

        self.client.post(f"/v1/rooms/{room_id}/channels", name="Register channel host web app",
                         headers={"Content-Type": "application/json"},
                         json=json.loads(str.format(json.dumps(register_channel_data), user_id, device_id)))
        return room_id

    def participant_tasks(self, room_id, participant_num):
        user_id = str(uuid.uuid4())
        # login_data["userId"] = user_id
        device_id = str(uuid.uuid4())

        response = self.client.post("/v1/users/connect", name=f"Connect participant {participant_num} sdk",
                                    headers={"Content-Type": "application/json"},
                                    json=json.loads(str.format(json.dumps(login_data), user_id, device_id)))

        # create_device_id["userId"] = user_id
        response = self.client.post(f"/v1/users/{user_id}/deviceGroups",
                                    name=f"Create device group participant {participant_num} sdk",
                                    headers={"Content-Type": "application/json"},
                                    json=json.loads(str.format(json.dumps(create_device_id), device_id)))
        device_group_id = ""
        if response.status == 200:
            device_group_id = response["deviceGroupId"]

        response = self.client.post("/v1/pin", name=f"Generate pin participant {participant_num} sdk",
                                    headers={"Content-Type": "application/json"},
                                    json=json.loads(str.format(json.dumps(pin_data), user_id)))
        pin = ""
        if response.status == 200:
            pin = response["pin"]

        response = self.client.post("/v1/users/connect", name=f"Connect participant {participant_num} web app",
                                    headers={"Content-Type": "application/json"},
                                    json=json.loads(str.format(json.dumps(login_data), user_id, device_id)))

        response = self.client.put("/v1/pin", name=f"Enter pin participant {participant_num} web app",
                                   headers={"Content-Type": "application/json"},
                                   data=str.format(json.dumps(enter_pin_data), pin))

        response = self.client.post(f"/v1/users/{user_id}/deviceGroups/{device_group_id}/attach",
                                    name=f"Attach participant {participant_num} web app",
                                    headers={"Content-Type": "application/json"},
                                    json=json.loads(str.format(json.dumps(attach_data), device_id)))

        response = self.client.post(f"/v1/rooms/{room_id}/join",
                                    name=f"Join room participant {participant_num} web app",
                                    headers={"Content-Type": "application/json"},
                                    json=json.loads(str.format(json.dumps(join_room_data), user_id, device_group_id)))

        self.client.post(f"/v1/rooms/{room_id}/channels",
                         name=f"Register channel participant {participant_num} web app",
                         headers={"Content-Type": "application/json"},
                         json=json.loads(str.format(json.dumps(register_channel_data), user_id, device_id)))

        @task
        def keep_alive():
            pass


class CoViewEndToEndUser(LocustTestUser):
    tasks = [CoViewEndToEnd]
    wait_time = constant(2)
    weight = 1
