const axios = require('axios');
const client_constants = require('./client_constants');

const Device = require('./device');
const Room = require('./room');

class FirebaseClient {
  constructor(apiUrl, role) {
    console.log(`Creating client for API at ${apiUrl}.`);
    this.apiUrl = apiUrl;
    this.devices = {};
  }

  run (action) {
    console.log("Firebase Client - run")
    switch(action.command) {
      case client_constants.COMMANDS.CONNECT:
        console.log("Firebase Client - connect")
        return axios.post(`${this.apiUrl}/users/connect`, action.payload)
                    .then(({ data: { asyncProtocol: { config } } }) => {
                      console.log("success - config = ")
                      console.log(config)
                      const device = new Device(action.payload.device.id, config)
                      this.devices[action.payload.device.id] = device;
                      return device.toString();
                    });

      case client_constants.COMMANDS.CREATE_ROOM:
        console.log("Firebase Client - CREATE_ROOM")
        return axios.post(`${this.apiUrl}/rooms`, action.payload)
                    .then(({ data: { roomId } }) => {
                      const room = new Room(roomId, this.firestore);
                      this.rooms[roomId] = room;
                      return `Created room ID: ${roomId}`;
                    });

      case client_constants.COMMANDS.JOIN_ROOM:
        console.log("Firebase Client - JOIN_ROOM")
        return axios.post(`${this.apiUrl}/rooms/${action.roomId}/join`, action.payload)
                    .then(({ data }) => {
                      const { payload: { deviceId }, path: { roomId } } = action;
                      const device = this.devices[deviceId];
                      if (device && !device.groupId) { // If the device is connected to a group, it'll connect to the room via the group
                        device.joinRoom(roomId, logFn);
                      }
                      console.log('Data', data);
                      return `Joined room!`;
                    });
      case client_constants.COMMANDS.LEAVE_ROOM:
        console.log("Firebase Client - LEAVE_ROOM")
        return axios.post(`${this.apiUrl}/rooms/${action.roomId}/leave`, action.payload)
                    .then(({ data }) => {
                      console.log('Data', data);
                      return `Left room!`;
                    });
      case client_constants.COMMANDS.JOIN_DEVICE_GROUP:
        console.log("Firebase Client - JOIN_DEVICE_GROUP")
        return axios.put(`${this.apiUrl}/users/${action.userId}/deviceGroups/${action.deviceGroupId}`, action.payload)
                    .then(({ data }) => {
                      console.log('Data', data);
                      const { payload: { deviceId }, path: { groupId } } = action;
                      const device = this.devices[deviceId];
                      if (device) {
                        device.joinDeviceGroup(groupId, logFn);
                      }
                      return `Joined device group!`;
                    });
      case client_constants.COMMANDS.LEAVE_DEVICE_GROUP:
        console.log("Firebase Client - LEAVE_DEVICE_GROUP")
        return axios.delete(`${this.apiUrl}/users/${action.userId}/deviceGroups/${action.deviceGroupId}/${action.deviceId}`, action.payload)
                    .then(({ data }) => {
                      console.log('Data', data);
                      return `Left device group!`;
                    });

      case client_constants.COMMANDS.HALT_DEVICE:
        this.devices[action.args.deviceId].halt();
        return Promise.resolve('Device halted.')
    }
  }
}
  
module.exports = FirebaseClient
