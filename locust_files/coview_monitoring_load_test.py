
import random
import uuid
from locust import task, TaskSet, HttpUser, between


class Monitoring(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.content_id = str(random.randint(9, 12))
        self.room_uuid = f'{str(random.randint(1, 3750))}alex'
    @task
    def host_monitoring(self):
        user_id = str(uuid.uuid4())
        device_id = f'{str(0)}{self.room_uuid}'
        content_id = self.content_id
        room_id = self.room_uuid
        group_id = str(uuid.uuid4())
        sync_state = ["OUT_OF_SYNC", "SYNC"]
        current_distance_ms = random.randint(-500, 500)
        is_give_up_meet_threshold = [True, False]
        avg_download_rate_bits_per_seconds = [3000, 15000]
        data = {"userId": user_id, "deviceId": device_id, "contentId": content_id, "roomId": room_id,
                "groupId": group_id, "syncState": sync_state[random.randint(0, 1)],
                "currentDistanceMs": current_distance_ms,
                "isGiveUpMeetThreshold": is_give_up_meet_threshold[random.randint(0, 1)],
                "avgDownloadRateBitsPerSeconds": avg_download_rate_bits_per_seconds[random.randint(0, 1)],
                "currentBitrateBitsPerSeconds": 300, "playbackSpeed": 5.5, "playerCurrentState": "STATE_READY",
                "playerCurrentPositionMs": 0, "currentNtpClientTimestamp": 123456789,
                "isUserInTransition": False, "errors": {}}
        response = self.client.post(f"/v1/report/devices/{device_id}", name="Monitoring host",
                                    headers={"Content-Type": "application/json", "USER_ID": user_id},
                                    json=data)
    @task
    def participant_monitoring_1(self):
        user_id = str(uuid.uuid4())
        device_id = f'{str(1)}{self.room_uuid}'
        content_id = self.content_id
        room_id = self.room_uuid
        group_id = str(uuid.uuid4())
        sync_state = ["OUT_OF_SYNC", "SYNC"]
        current_distance_ms = random.randint(-500, 500)
        is_give_up_meet_threshold = [True, False]
        avg_download_rate_bits_per_seconds = [3000, 15000]
        data = {"userId": user_id, "deviceId": device_id, "contentId": content_id, "roomId": room_id,
                "groupId": group_id, "syncState": sync_state[random.randint(0, 1)],
                "currentDistanceMs": current_distance_ms,
                "isGiveUpMeetThreshold": is_give_up_meet_threshold[random.randint(0, 1)],
                "avgDownloadRateBitsPerSeconds": avg_download_rate_bits_per_seconds[random.randint(0, 1)],
                "currentBitrateBitsPerSeconds": 300, "playbackSpeed": 5.5, "playerCurrentState": "STATE_READY",
                "playerCurrentPositionMs": 0, "currentNtpClientTimestamp": 123456789,
                "isUserInTransition": False, "errors": {}}
        response = self.client.post(f"/v1/report/devices/{device_id}", name="Monitoring participant 1",
                                    headers={"Content-Type": "application/json", "USER_ID": user_id},
                                    json=data)
    @task
    def participant_monitoring_2(self):
        user_id = str(uuid.uuid4())
        device_id = f'{str(2)}{self.room_uuid}'
        content_id = self.content_id
        room_id = self.room_uuid
        group_id = str(uuid.uuid4())
        sync_state = ["OUT_OF_SYNC", "SYNC"]
        current_distance_ms = random.randint(-500, 500)
        is_give_up_meet_threshold = [True, False]
        avg_download_rate_bits_per_seconds = [3000, 15000]
        data = {"userId": user_id, "deviceId": device_id, "contentId": content_id, "roomId": room_id,
                "groupId": group_id, "syncState": sync_state[random.randint(0, 1)],
                "currentDistanceMs": current_distance_ms,
                "isGiveUpMeetThreshold": is_give_up_meet_threshold[random.randint(0, 1)],
                "avgDownloadRateBitsPerSeconds": avg_download_rate_bits_per_seconds[random.randint(0, 1)],
                "currentBitrateBitsPerSeconds": 300, "playbackSpeed": 5.5, "playerCurrentState": "STATE_READY",
                "playerCurrentPositionMs": 0, "currentNtpClientTimestamp": 123456789,
                "isUserInTransition": False, "errors": {}}
        response = self.client.post(f"/v1/report/devices/{device_id}", name="Monitoring participant 2",
                                    headers={"Content-Type": "application/json", "USER_ID": user_id},
                                    json=data)
    @task
    def participant_monitoring_3(self):
        user_id = str(uuid.uuid4())
        device_id = f'{str(3)}{self.room_uuid}'
        content_id = self.content_id
        room_id = self.room_uuid
        group_id = str(uuid.uuid4())
        sync_state = ["OUT_OF_SYNC", "SYNC"]
        current_distance_ms = random.randint(-500, 500)
        is_give_up_meet_threshold = [True, False]
        avg_download_rate_bits_per_seconds = [3000, 15000]
        data = {"userId": user_id, "deviceId": device_id, "contentId": content_id, "roomId": room_id,
                "groupId": group_id, "syncState": sync_state[random.randint(0, 1)],
                "currentDistanceMs": current_distance_ms,
                "isGiveUpMeetThreshold": is_give_up_meet_threshold[random.randint(0, 1)],
                "avgDownloadRateBitsPerSeconds": avg_download_rate_bits_per_seconds[random.randint(0, 1)],
                "currentBitrateBitsPerSeconds": 300, "playbackSpeed": 5.5, "playerCurrentState": "STATE_READY",
                "playerCurrentPositionMs": 0, "currentNtpClientTimestamp": 123456789,
                "isUserInTransition": False, "errors": {}}
        response = self.client.post(f"/v1/report/devices/{device_id}", name="Monitoring participant 3",
                                    headers={"Content-Type": "application/json", "USER_ID": user_id},
                                    json=data)
class CretePinUser(HttpUser):
    tasks = [Monitoring]
    wait_time = between(1, 120)
    weight = 1