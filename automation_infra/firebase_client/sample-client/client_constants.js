
const CMD_ACTIONS = {
  'CONNECT': 'Connect to the API',
  'CREATE_ROOM': 'Create a new room',
  'JOIN_ROOM': 'Join a pre-existing room',
  'HALT_DEVICE': '"Turn off" device (stop updating its keep-alive ping)'
};

const COMMANDS = {
  CONNECT: 'connect',
  CREATE_ROOM: 'create_room',
  JOIN_ROOM: 'join_room',
  LEAVE_ROOM: 'leave_room',
  JOIN_DEVICE_GROUP: 'join_device_group',
  LEAVE_DEVICE_GROUP: 'leave_device_group',
  HALT_DEVICE: 'halt_device',
};

LISTENING_PORT = 3000;

module.exports = {
  ACTIONS: CMD_ACTIONS,
  COMMANDS,
  LISTENING_PORT
}
