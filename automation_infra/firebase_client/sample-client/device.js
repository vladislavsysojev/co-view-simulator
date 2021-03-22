const firebase = require('firebase');
const crypto = require('crypto');

class Device {
  constructor(deviceId, firestoreConfig) {
    const { basePath, token } = firestoreConfig;
    this.id = deviceId;
    this.firebaseApp = firebase.initializeApp(firestoreConfig, `device-${deviceId}`);
    this.dbRoot = basePath;

    firebase.auth(this.firebaseApp).signInWithCustomToken(token)
            .then((userCredential) => {
              this.user = userCredential.user;
              console.log(`Logged in to Firebase as: ${this.user.uid}`)

              this.db = firebase.firestore(this.firebaseApp);
              this.db.collection(`${this.dbRoot}/keepalive`).doc('server').onSnapshot(this.updateKeepalive);
            })
  }

  toString() {
    return `Device ${this.id} (FIREBASE project: ${this.firebaseApp.options.projectId})`
  }

  // Listens for snapshot updates on the server's keep-alive and updates our keep-alive document
  updateKeepalive = (_) => {
    if (!this.halted) {
      setTimeout(() => this.db.collection(`${this.dbRoot}/keepalive`)
                             .doc(this.id)
                             .set({ timestamp: firebase.firestore.FieldValue.serverTimestamp(),
                                    class: "DeviceNotification",
                                    type: "KeepAlive",
                                    version: "v1" }),
                 crypto.randomInt(60));
    }
  }

  defaultDeviceGroupLog = (msg) => {
    const fmtMsg = JSON.stringify(msg, null, '\t');
    console.log(`[${this.user.uid}] Receieved group notification for Device Group ${this.groupId}: ${fmtMsg}`);
  }

  joinDeviceGroup = (groupId, logFn) => {
    this.groupId = groupId;
    const groupLogFn = logFn === undefined ? this.defaultDeviceGroupLog : logFn;
    const messageHandler = this.handleDeviceGroupMessage(groupLogFn);
    this.haltDeviceGroupListener = this.db
                                       .collection(`${this.dbRoot}/deviceGroups`)
                                       .doc(groupId)
                                       .onSnapshot(messageHandler);
  }

  handleDeviceGroupMessage = (logFn) => (docSnapshot) => {
    const data = docSnapshot.data();
    if (data === undefined) return;
    if (data.state.roomId !== undefined && data.state.roomId !== this.roomId) {
      this.joinRoom(data.state.roomId);
    }
    logFn(data);
  }

  leaveDeviceGroup = () => {
    if (this.haltDeviceGroupListener) {
      this.haltDeviceGroupListener();
      this.haltDeviceGroupListener = null;
    }
    this.groupId = null;
  }

  defaultRoomLog = (msg) => {
    const fmtMsg = JSON.stringify(msg, null, '\t');
    console.log(`[${this.user.uid}] Received room notification for Room ${this.roomId}: ${fmtMsg}`);
  }

  joinRoom = (roomId, logFn) => {
    this.roomId = roomId;
    const roomLogFn = logFn === undefined ? this.defaultRoomLog : logFn;
    const messageHandler = this.handleRoomMessage(roomLogFn);
    this.haltRoomListener = this.db
                                .collection(`${this.dbRoot}/rooms`)
                                .doc(roomId)
                                .onSnapshot(messageHandler);
  }

  handleRoomMessage = (logFn) => (docSnapshot) => {
    const data = docSnapshot.data();
    if (data === undefined) return;
    logFn(data.state);
  }

  leaveRoom = () => {
    if (this.haltRoomListener) {
      this.haltRoomListener();
      this.haltRoomListener = null;
    }
    this.roomId = null;
  }

  halt = () => {
    this.halted = true;
    this.leaveDeviceGroup();
    this.leaveRoom();
  }

}

module.exports = Device;
