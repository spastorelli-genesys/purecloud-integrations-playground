let customPlugin;
const chatButtonTemplate = "";
const chatWidgetConfig = {
  widgets: {
    webchat: {
      transport: {
        type: "purecloud-v2-sockets",
        dataURL: "https://api.mypurecloud.com",
        deploymentKey: "da0ba755-efcc-4e93-958a-fea3dea65fb2",
        orgGuid: "cc329c9f-a78c-4788-8808-6fdf739234f7",
        interactionData: {
          routing: {
            targetType: "QUEUE",
            targetAddress: "Steeve Test Queue 1",
            priority: 2,
          },
        },
      },
      chatButton: {
        enabled: true,
        template: chatButtonTemplate,
        openDelay: 5000,
      },
    },
  },
};

function configureChatWidget() {
  CXBus.configure({
    debug: true,
    pluginsPath: "https://apps.mypurecloud.com/widgets/9.0/plugins/",
  });
  CXBus.loadPlugin("widgets-core");
}

function getAdvancedConfig() {
  const inputWrapper = `
  <div class="field">
    <label class="label">{label}</label>
    <div class="control">{input}</div>
  </div>
  `;
  return {
    form: {
      autoSubmit: false,
      firstname: "",
      lastname: "",
      email: "",
      subject: "",
    },
    formJSON: {
      wrapper: "<form></form>",
      inputs: [
        {
          id: "cx_webchat_form_firstname",
          name: "firstname",
          maxlength: "100",
          placeholder: "Required",
          label: "First Name",
          wrapper: inputWrapper,
        },
        {
          id: "cx_webchat_form_lastname",
          name: "lastname",
          maxlength: "100",
          placeholder: "Required",
          label: "Last Name",
          wrapper: inputWrapper,
        },
        {
          id: "cx_webchat_form_email",
          name: "email",
          maxlength: "100",
          placeholder: "Optional",
          label: "Email",
          wrapper: inputWrapper,
        },
        {
          id: "cx_webchat_form_subject",
          name: "subject",
          maxlength: "100",
          placeholder: "Optional",
          label: "Subject",
          wrapper: inputWrapper,
        },
      ],
    },
  };
}

function startChat() {
  customPlugin.command("WebChat.open", getAdvancedConfig());
}

window.addEventListener("load", function () {
  window._genesys = chatWidgetConfig;
  customPlugin = CXBus.registerPlugin("Custom");
  customPlugin.subscribe("WebChatService.started", function (e) {
    console.log("Chat started", e);
  });
  customPlugin.subscribe("WebChatService.ended", function (e) {
    console.log("Chat ended", e);
  });
});
