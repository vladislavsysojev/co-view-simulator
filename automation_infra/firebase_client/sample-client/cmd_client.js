const axios = require('axios');
const crypto = require('crypto');
const faker = require('faker');
const client_constants = require('./client_constants');
const firebaseClient = require('./firebase_client');

class CmdClient {
  constructor(apiUrl, role) {
    console.log(`Creating cmd client for API at ${apiUrl}.`);
    this.apiUrl = apiUrl;
    this.devices = {};
    this.client = new firebaseClient(apiUrl);
  }

  prompt = async (rl, finish) => {
    console.log('Type \'?\' for help...')
    rl.setPrompt(`Co-View @ ${this.apiUrl} > `);

    let cmds = Object.keys(client_constants.CMD_ACTIONS);
    cmds.unshift('?');
    cmds.push('quit');
    rl.setCompletion(cmds);

    rl.on('line', (cmd) => {
      switch(cmd) {
        case '?':
          console.log("\nChoose one of the following actions:\n");
          for (const cmd of Object.keys(client_constants.CMD_ACTIONS)) { console.log(`${cmd}: ${client_constants.CMD_ACTIONS[cmd]}`) }
          console.log("quit: End this session")
          console.log("");
          break;
        case 'quit':
          console.log('Quitting...');
          for (const device of Object.values(this.devices)) { device.halt(); }
          for (const room of Object.values(this.rooms)) { room.disconnect(); }
          if (this.firebaseApp) { this.firebaseApp.delete(); }
          finish();
          break;
        default:
          if (!client_constants.CMD_ACTIONS[cmd]) {
            console.log(`Unknown command: ${cmd}`);
          } else {
            new Promise(resolve => this[cmd].call(cmd, rl, resolve))
              .then(action => {
                return this.client.run(action);
              })
              .then(response => {
                console.log('Response:', response)
              })
              .catch((error) => {
                if (error.response) {
                  console.log(`Error making API call: ${error.response.data.message}`);
                } else {
                  console.log(`Problem: ${error.message}`);
                }
                return;
              });
          }
      }
    });
  }

  connect = (rl, ret) => {
    rl.question('Pick a username (or <enter> for a random one): ', (answer) => {
      let name = answer;
      if (name.length === 0) {
        name = faker.internet.userName();
      }
      const deviceId = crypto.randomUUID();
      console.log(`Connecting as: ${name}, with device ID: ${deviceId}`);
      ret({
        command: 'connect',
        payload: {
          userId: name,
          device: {
            id: deviceId,
            platform: 'web',
            name: 'Host TV',
            capabilities: [{
              'MEDIA_SYNC': 'READ'
            }]
          },
          clientProtocols: ['FIRESTORE']
        }});
    });
  }

  create_room = (rl, ret) => {
    let playbackUrl = 'http://edge1.il.kab.tv/rtplive/tv66-heb-high.stream/playlist.m3u8'
    rl.question('For which user? ', (answer) => {
      // TODO: Since playback URL might 301 redirect, and since the API server
      // doesn't resolve redirects, we need to do it here by making the request and using the response URL:
      axios.get(playbackUrl)
           .then(({ request: { res: { responseUrl } } }) => {
             ret({
               command: 'create_room',
               payload: {
                 creator: {
                   id: answer
                 },
                 initialState: "PLAY",
                 initialPosition: 0,
                 content: {
                   id: "1",
                   playbackUrls: [
                     responseUrl
                   ]
                 }
               }
             });
           });
    });
  }

  join_room = (rl, ret) => {
    rl.question('Join which room? ', (room) => {
      rl.question('As which user? ', (user) => {
        rl.question('With which device or device group ID? ', (device) => {
          ret({
            command: 'join_room',
            path: {
              roomId: room
            },
            payload: {
              userId: user,
              deviceId: device,
              name: user
            }
          });
        });
      });
    });
  }

  create_group = (rl, ret) => {
    rl.question('For which user? ', (user) => {
      rl.question('With which device? ', (device) => {
        ret({
          command: 'create_device_group',
          path: {
            userId: user
          },
          payload: {
            deviceId: device
          }
        });
      });
    });
  }

  join_group = (rl, ret) => {
    rl.question('Join which group? ', (group) => {
      rl.question('As which user? ', (user) => {
        rl.question('Which device to join? ', (device) => {
          ret({
            command: 'join_device_group',
            path: {
              userId: user,
              groupId: group
            },
            payload: {
              deviceId: device
            }
          });
        });
      });
    });
  }

  halt_device = (rl, ret) => {
    rl.question('Which device ID? ', (device) => {
      ret({
        command: 'halt_device',
        args: {
          deviceId: device
        }
      });
    });
  }
}

module.exports = CmdClient
