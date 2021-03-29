import json
import random
import uuid

from locust import task, TaskSet, constant, HttpUser


# from automation_infra.requests_api.rest_api_request_data import login_data, create_device_id

class CreteRoomUser(TaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        # self.login_data = RequestData().login_data
        # self.create_device_id = RequestData().create_device_id

    def on_start(self):
        user_id = str(uuid.uuid4())
        device_id = str(uuid.uuid4())
        create_room_data = {
            "creator": {
                "id": ""
            },
            "initialState": "PLAY",
            "initialPosition": 0,
            "content": {
                "id": "1111",
                "playbackUrls": [
                    "https://svc43.main.sl.t-online.de/dlt3/out/u/hssfcbayern01_fm.m3u8",
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
        login_data = {
            "userId": user_id,
            "device": {
                "id": device_id,
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
        self.response = self.client.post("/v1/users/connect", name="Connect",
                                         headers={"Content-Type": "application/json"},
                                         json=login_data)
        if self.response.status_code == 200:
            create_room_data["creator"]["id"] = user_id
            self.response = self.client.post("/v1/rooms", name="Create room host web app",
                                             headers={"Content-Type": "application/json"},
                                             json=create_room_data)

    @task
    def keep_alive(self):
        pass


class CreateRoom(HttpUser):
    tasks = [CreteRoomUser]
    wait_time = constant(1)
    weight = 1
