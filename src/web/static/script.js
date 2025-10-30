cat > src/web/static/script.js << 'EOF'
class AssistantApp {
    constructor() {
        this.messagesContainer = document.getElementById('messages');
        this.userInput = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        this.avatarEmoji = document.getElementById('avatar-emoji');
        this.statusText = document.getElementById('status-text');
        this.setupEventListeners();
        this.addWelcomeMessage();
    }
    setupEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) this.sendMessage();
        });
    }
    addWelcomeMessage() {
        this.addMessage('Ciao! Sono il tuo assistente AI. Come posso aiutarti? 😊', 'assistant');
    }
    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message) return;
        this.addMessage(message, 'user');
        this.userInput.value = '';
        this.setStatus('Penso...', '🤔');
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            this.addMessage(data.response, 'assistant');
            this.setStatus('Pronto', '😊');
        } catch (error) {
            this.addMessage('❌ Errore: ' + error.message, 'assistant');
        }
    }
    addMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        msgDiv.textContent = text;
        this.messagesContainer.appendChild(msgDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    setStatus(text, emoji) {
        this.statusText.textContent = text;
        this.avatarEmoji.textContent = emoji;
    }
}
document.addEventListener('DOMContentLoaded', () => { new AssistantApp(); });
EOF
