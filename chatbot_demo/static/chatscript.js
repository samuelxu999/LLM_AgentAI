// This js code handle chatgpt prompt from UI and display response.
class ChatUI {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.userInput = document.getElementById('user-input');
        this.sendButton = document.getElementById('send-button');
        this.history = [];
        
        this.init();
    }

    init() {
        this.setupEventListeners();
    }

    displayMessage(text, sender, isTyping = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);

        const avatar = document.createElement('img');
        avatar.classList.add('avatar');
        avatar.src = `/static/images/${sender}.png`;
        messageDiv.appendChild(avatar);

        const content = document.createElement('div');
        content.classList.add('message-content');

        if (isTyping) {
            content.classList.add('typing-indicator');
        } else {
            content.innerHTML = marked.parse(text);
        }

        messageDiv.appendChild(content);
        this.container.appendChild(messageDiv);
        this.scrollToBottom();

        return messageDiv;
    }
     
   async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message) return;

        // Clear input and show user message
        this.userInput.value = '';
        this.displayMessage(message, 'user');

        // Show typing indicator
        const typingDiv = this.displayMessage('', 'bot', true);

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_message: message })
            });

            const data = await response.json();
            
            // Remove typing indicator and show response
            typingDiv.remove();
            this.displayMessage(data.bot_reply, 'bot');

        } catch (error) {
            console.error('Error:', error);
            typingDiv.remove();
            this.displayMessage('Error processing request', 'system');
        }
    }

    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    scrollToBottom() {
        this.container.scrollTo({
            top: this.container.scrollHeight,
            behavior: 'smooth'
        });
    }
}

// Initialize chat when document is ready
document.addEventListener('DOMContentLoaded', () => {
    const chatUI = new ChatUI('chat-container');
});