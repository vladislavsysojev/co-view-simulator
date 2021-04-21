login_data = {
            "userId": "",
            "device": {
                "id": "",
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

create_device_id = {
            "deviceId": "",
        }

create_room_data = {
            "creator": {
                "id": ""
            },
            "initialState": "PLAY",
            "initialPosition": 0,
            "content": {
                "id": "",
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

enter_pin_data = {"pin": ""}

pin_data = {"payload": ""}

pin_data_full = {
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

attach_data = {
    "deviceId": ""
}

join_room_data = {
    "userId": "",
    "deviceId": "",
    "name": "Vlad"
}

register_channel_data = {
    "userId": "",
    "deviceId": "",
    "channels": {
        "MEDIA_SYNC": {
            "mode": "READ",
            "playbackUrl": "https://svc43.main.sl.t-online.de/dlt3/out/u/hssfcbayern01_fm.m3u8"
        }
    }
}

leave_room_data = {
     "deviceId": "",
     "userId": ""
}

disconnect_data = {
  "userId": "",
  "deviceId": ""
}


access_token_data = {
  # "applicationKey": "b8082613-c01c-4b21-b500-7f18a06d8ca6",
  "applicationKey": "some-uuid",
  "userId": "",
  "deviceId": ""
}

room_content_ids = []