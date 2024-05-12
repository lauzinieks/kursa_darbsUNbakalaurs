(function() {
  // Create the df-messenger script tag
  var script = document.createElement('script');
  script.src = "https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js";
  script.defer = true;
  document.head.appendChild(script);

  script.onload = function() {
    // Upon loading, initialize the df-messenger element
    var dfMessenger = document.createElement("df-messenger");
    dfMessenger.setAttribute("project-id", "lumibakalaurs");
    dfMessenger.setAttribute("agent-id", "6de1182c-aca6-4e19-8a98-28300376f3a0");
    dfMessenger.setAttribute("language-code", "lv");
    dfMessenger.setAttribute("max-query-length", "-1");
    document.body.appendChild(dfMessenger);

    // Styling could be adjusted here as needed
    var style = document.createElement("style");
    style.type = 'text/css';
    style.innerHTML = `df-messenger {
      z-index: 999;
      position: fixed;
      --df-messenger-font-color: #000;
      --df-messenger-font-family: Google Sans;
      --df-messenger-chat-background: #f3f6fc;
      --df-messenger-message-user-background: #d3e3fd;
      --df-messenger-message-bot-background: #fff;
      bottom: 16px;
      right: 16px;
    }`;
    document.head.appendChild(style);
  };
})();