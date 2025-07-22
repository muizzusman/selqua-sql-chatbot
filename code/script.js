const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const newChatBtn = document.getElementById('new-chat');
const logo = document.getElementById('logo');
const darkModeToggle = document.getElementById('dark-mode-toggle');

// Typing animation for bot responses
async function typeMessage(message, sender) {
  const msgDiv = document.createElement('div');
  msgDiv.classList.add('chat-message', sender);
  chatContainer.appendChild(msgDiv);

  for (let i = 0; i < message.length; i++) {
    msgDiv.textContent += message[i];
    await new Promise(r => setTimeout(r, 20));
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }
}

// Send message and fetch response
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  // Display user message
  const userMsg = document.createElement('div');
  userMsg.classList.add('chat-message', 'user');
  userMsg.textContent = text;
  chatContainer.appendChild(userMsg);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  userInput.value = '';

  // Show typing loader
  const loadingMsg = document.createElement('div');
  loadingMsg.classList.add('chat-message', 'bot');
  loadingMsg.textContent = "Typing";
  chatContainer.appendChild(loadingMsg);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  // Animate loading dots
  let dotCount = 0;
  const loadingInterval = setInterval(() => {
    dotCount = (dotCount + 1) % 4;
    loadingMsg.textContent = "Typing" + ".".repeat(dotCount);
  }, 400);

  // Fetch response from backend
  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await response.json();

    clearInterval(loadingInterval);
    loadingMsg.remove();

    const answer = data.answer || data.error || "Something went wrong.";
    await typeMessage(answer, 'bot');
  } catch (error) {
    clearInterval(loadingInterval);
    loadingMsg.remove();
    await typeMessage("❌ Cannot reach backend. Is Flask running?", 'bot');
  }
}

// Toggle dark mode
darkModeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark');
});

// Reset chat
newChatBtn.addEventListener('click', () => {
  chatContainer.innerHTML = '<div class="chat-message bot">What can I help with?</div>';
});

// Reload on logo click
logo.addEventListener('click', () => {
  location.reload();
});

// Button click and enter key
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', e => {
  if (e.key === 'Enter') sendMessage();
});