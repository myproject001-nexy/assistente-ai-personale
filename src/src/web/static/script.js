// Chat application
class AssistantApp {
    constructor() {
        this.messagesContainer = document.getElementById('messages');
        this.userInput = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        this.improveBtn = document.getElementById('improve-btn');
        this.executeBtn = document.getElementById('execute-btn');
        this.statusBtn = document.getElementById('status-btn');
        this.avatarEmoji = document.getElementById('avatar-emoji');
        this.statusText = document.getElementById('status-text');
        this.statsModal = document.getElementById('stats-modal');
        
        this.setupEventListeners();
        this.addWelcomeMessage();
    }
    
    setupEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) this.sendMessage();
        });
        
        this.improveBtn.addEventListener('click', () => this.improve());
        this.executeBtn.addEventListener('click', () => this.executeTask());
        this.statusBtn.addEventListener('click', () => this.showStatus());
        
        document.querySelector('.close').addEventListener('click', () => {
            this.statsModal.style.display = 'none';
        });
    }
    
    addWelcomeMessage() {
        this.addMessage('Ciao! Sono il tuo assistente AI personale. Come posso aiutarti? 😊', 'assistant');
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
            this.setStatus('Errore', '⚠️');
        }
    }
    
    async improve() {
        this.setStatus('Miglioramento...', '🔧');
        
        try {
            const response = await fetch('/api/improve', { method: 'POST' });
            const data = await response.json();
            
            this.addMessage('✨ Auto-miglioramento completato!\n' + 
                          'Miglioramenti: ' + data.improvements.improvements.join(', '), 
                          'assistant');
            this.setStatus('Migliorato', '✨');
        } catch (error) {
            this.addMessage('❌ Errore miglioramento', 'assistant');
        }
    }
    
    async executeTask() {
        const task = prompt('Descrivi il compito:');
        if (!task) return;
        
        this.setStatus('Esecuzione...', '🚀');
        
        try {
            const response = await fetch('/api/task', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task })
            });
            
            const data = await response.json();
            this.addMessage('✅ Compito eseguito!\nPiano: ' + 
                          data.plan.actions.join(', '), 
                          'assistant');
            this.setStatus('Completato', '✅');
        } catch (error) {
            this.addMessage('❌ Errore esecuzione', 'assistant');
        }
    }
    
    async showStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            const statsHtml = `
                <p><strong>Conversazioni:</strong> ${data.conversations}</p>
                <p><strong>Success Rate:</strong> ${data.success_rate}</p>
                <p><strong>Autonomia:</strong> ${data.autonomy}</p>
                <p><strong>Skills:</strong> ${data.skills}</p>
                <p><strong>Status:</strong> ${data.status}</p>
            `;
            
            document.getElementById('stats-content').innerHTML = statsHtml;
            this.statsModal.style.display = 'block';
        } catch (error) {
            alert('Errore caricamento statistiche');
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

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    new AssistantApp();
});