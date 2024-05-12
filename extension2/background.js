chrome.webRequest.onHeadersReceived.addListener(
    function(details) {
      for (var i = 0; i < details.responseHeaders.length; i++) {
        if ('content-security-policy' === details.responseHeaders[i].name.toLowerCase()) {
          details.responseHeaders[i].value = "script-src 'self' https://www.gstatic.com;";
        }
      }
      return {responseHeaders: details.responseHeaders};
    }, {
      urls: ["*://www.lu.lv/*"],
      types: ["main_frame"]
    }, ["blocking", "responseHeaders", "extraHeaders"]
  );