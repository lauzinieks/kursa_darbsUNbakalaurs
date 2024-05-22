// Inject Dialogflow Messenger script
const script = document.createElement('script');
script.src = 'http://localhost:8000/df-messenger.js';
document.body.appendChild(script);

// Wait for script to load
script.addEventListener('load', () => {
  // Create Dialogflow Messenger instance
  const messenger = new dfMessenger({
    projectId: 'lumibakalaurs',
    agentId: '6de1182c-aca6-4e19-8a98-28300376f3a0',
    languageCode: 'en',
    maxQueryLength: -1,
  });

  // Create chat bubble
  const chatBubble = new dfMessengerChatBubble({
    chatTitle: '',
  });

  // Add chat bubble to messenger
  messenger.addChatBubble(chatBubble);

  // Display messenger
  messenger.show();
});
