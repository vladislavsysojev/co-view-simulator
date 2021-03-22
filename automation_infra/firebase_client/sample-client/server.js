const express = require('express');
const health = require('@cloudnative/health-connect');
const cors = require('cors');
const client_constants = require('./client_constants');
const firebaseClient = require('./firebase_client');

const app = express();
app.use(cors());
const bodyParser = require('body-parser');
app.use(bodyParser.json());

const apiUrl = 'http://localhost:8080/coview/v1';
const client = new firebaseClient(apiUrl);
devices = {};

// TODO: For debugging purposes
app.get('/api/connect', function (req, res) {
    console.log("Start Connect")
    // payload = req.payload;
    payload = connect_payload;
    action = {command: client_constants.COMMANDS.CONNECT, payload: payload}
    return forwardRequest(action, res);
});

app.get('/api/create_device', function (req, _res) {
    // just update device object
    const device = new Device(req.payload.device.id, config)
    devices[action.payload.device.id] = device;
    return device.toString();
});

app.post('/api/join_room', function (req, res) {
    payload = req.body.payload;
    roomId = req.body.roomId;
    //payload = join_room_payload;
    action = {command: client_constants.COMMANDS.JOIN_ROOM, roomId: roomId, payload: payload}
    return forwardRequest(action, res);
});

app.post('/api/leave_room', function (req, res) {
    payload = req.body.payload;
    roomId = req.body.roomId;
    // payload = leave_room_payload;
    action = {command: client_constants.COMMANDS.LEAVE_ROOM, roomId: roomId, payload: payload}
    return forwardRequest(action, res);
});

app.put('/api/join_device_group', function (req, res) {
    payload = req.body.payload;
    userId = req.body.userId;
    deviceGroupId = req.body.deviceGroupId;
    // payload = join_device_group_payload;
    action = {command: client_constants.COMMANDS.JOIN_DEVICE_GROUP, userId: userId,  deviceGroupId: deviceGroupId, payload: payload}
    return forwardRequest(action, res);
});

app.delete('/api/leave_device_group', function (_req, res) {
    action = {command: client_constants.COMMANDS.LEAVE_DEVICE_GROUP, userId: userId, deviceGroupId: deviceGroupId, deviceId: deviceId, payload: {}}
    return forwardRequest(action, res);
});

function forwardRequest(action, res) {
    new Promise((_resolve, _reject) => {
        return client.run(action);
    })
        .then(response => {
            console.log('Response:', response);
            res.status(200).type('json').send(JSON.stringify(response));
        })
        .catch((error) => {
            if (error.response) {
                console.log(`Error making API call: ${error.response.data.message}`);
            } else {
                console.log(`Problem: ${error.message}`);
            }
            return res.status(404).type('json').send({ message: error.response, error: error.response });
        });
}

let healthCheck = new health.HealthChecker();

const livePromise = () =>
   new Promise((resolve, _reject) => {
      const appFunctioning = true;
      // You should change the above to a task to determine if your app is functioning correctly
      if (appFunctioning) {
         resolve();
      } else {
         _reject(new Error('App is not functioning correctly'));
      }
   });

let liveCheck = new health.LivenessCheck('LivenessCheck', livePromise);

healthCheck.registerLivenessCheck(liveCheck);

app.use('/live', health.LivenessEndpoint(healthCheck));
app.use('/ready', health.ReadinessEndpoint(healthCheck));
app.use('/health', health.HealthEndpoint(healthCheck));


app.listen(client_constants.LISTENING_PORT, function () {
    console.log(`Server is listening on port ${client_constants.LISTENING_PORT}!`);
 });



 // TODO: delete!
connect_payload = {
    "userId": "23d23ff32",
    "device": {
      "id": "h783hd",
      "name": "TV APP",
      "platform": "ANDROID",
      "capabilities": {
        "MEDIA_SYNC": "READ"
      }
    },
    "clientProtocols": [
      "FIRESTORE"
    ]
};
join_room_payload = {
    "userId": "2d23f3f",
    "deviceId": "1234",
    "name": "Andrew"
};
join_device_group_payload = {
    "deviceId": "h783hd"
  };
leave_room_payload = {
    "deviceId": "sdf78sd",
    "userId":"sdfsdf3"
};