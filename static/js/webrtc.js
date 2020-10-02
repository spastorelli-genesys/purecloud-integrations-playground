class PureCloudWebRTC {
  constructor(accessToken) {
    this.sdk = new window.PureCloudWebrtcSdk({
      accessToken: accessToken
    });

    this.notifications = {};
  }

  createNotification(id, address) {
    const notification = document.createElement("div");
    notification.classList.add("notification", "is-info");
    notification.id = `webrtc-call-${id}-notification`;

    console.log("Received call from: ", address);

    const notificationMsg = `Incoming call from: ${address}`;
    const notificationContent = document.createElement("div");
    notificationContent.className = "content";
    notificationContent.textContent = notificationMsg;

    const acceptButton = document.createElement("button");
    acceptButton.classList.add("button", "is-primary");
    acceptButton.textContent = "Accept";
    acceptButton.addEventListener("click", () => {
      console.log("Accepting call: ", id);
      this.sdk.acceptPendingSession(id);
      notification.remove();
    });

    const rejectButton = document.createElement("button");
    rejectButton.classList.add("button", "is-danger");
    rejectButton.textContent = "Reject";
    rejectButton.addEventListener("click", () => {
      console.log("Accepting call: ", id);
      this.sdk.endSession({ id: id });
      notification.remove();
    });

    const controls = document.createElement("div");
    controls.classList.add("field", "is-grouped");
    controls.appendChild(acceptButton);
    controls.appendChild(rejectButton);

    notification.appendChild(notificationContent);
    notification.appendChild(controls);

    return notification;
  }

  discardNotification(id) {
    console.log("Discarding notification for Call ID: ", id);
    if (id in this.notifications) {
      const notificationId = this.notifications[id];
      const notification = document.querySelector(`#${notificationId}`);
      if (notification) {
        notification.remove();
      }
    }
  }

  handlePendingSession({ id, address, conversationId, autoAnswer }) {
    console.log("Call pending: ", id);
    if (!(id in this.notifications)) {
      const notification = this.createNotification(id, address);
      this.notifications[id] = notification.id;

      const notificationArea = document.querySelector("#webrtcNotications");
      notificationArea.appendChild(notification);
    }
  }

  handlePendingSessionHandled(id) {
    console.log(`Call ID ${id} handled by other client. Closing notification.`);
    this.discardNotification(id);
  }

  handlePendingSessionCancelled(id) {
    console.log(`Call ID ${id} was cancelled.`);
    this.discardNotification(id);
  }

  handleSessionStarted(session) {
    console.log("Call session started: ", session);
    const messageArea = document.querySelector("#messages");
    const message = document.createElement("div");
    message.classList.add("notification", "is-info", "message");
    // TODO: finish
  }

  handleSessionEnded(session, reason) {
    const id = session.id;
    console.log(`Call session ended ${id}: ${reason}`);

    // TODO: finish
  }

  setup() {
    this.sdk.on("pendingSession", this.handlePendingSession.bind(this));
    this.sdk.on(
      "handledPendingSession",
      this.handlePendingSessionHandled.bind(this)
    );
    this.sdk.on(
      "cancelPendingSession",
      this.handlePendingSessionCancelled.bind(this)
    );
    this.sdk.on("sessionStarted", this.handleSessionStarted.bind(this));
    this.sdk.on("sessionEnded", this.handleSessionEnded.bind(this));
  }

  start() {
    this.sdk.initialize();
    this.setup();
  }
}
