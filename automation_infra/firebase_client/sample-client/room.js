const firebase = require('firebase');

class Room {
  constructor(roomId, firestore) {
    this.roomId = roomId;
    this.listener = firestore.db
                             .collection(`${firestore.dbRoot}/rooms/${this.roomId}/notifications`)
                             .onSnapshot(this)
  }

  toString() {
    return `Room ${this.roomId} (FIREBASE project: ${firebase.app().options.projectId})`
  }

  // Used for the snapshot listener
  next(query) {
    for (const docChange of query.docChanges()) {
      if (docChange.type === 'added') {
        console.log(`Got a room notification for room ID ${this.roomId}: ${JSON.stringify(docChange.doc.data(), null, '\t')}`)
      }
    }
  }

  disconnect = () => {
    this.listener();
  }
}

module.exports = Room;
