#!/usr/bin/env python3
"""
Auto-generatore di codice per Assistente AI
Crea automaticamente i file necessari e chiede risorse se mancanti
"""

import os
import json
import sys
import subprocess
from datetime import datetime

class AssistantBuilder:
    """Builder per generare automaticamente l'assistente"""
    
    def __init__(self):
        self.project_root = os.getcwd()
        self.required_files = {
            ".env": self.create_env_file,
            "src/web/app.py": self.create_web_app,
            "src/web/templates/index.html": self.create_html_template,
            "src/web/static/style.css": self.create_css,
            "src/web/static/script.js": self.create_javascript,
            "requirements.txt": self.create_requirements,
            "Dockerfile": self.create_dockerfile,
        }
        
        print("\n" + "="*70)
        print("🔨 AUTO-GENERATORE ASSISTENTE AI BETA")
        print("="*70 + "\n")
    
    def build(self):
        """Costruisce l'assistente completo"""
        print("🏗️ Inizio costruzione...\n")
        
        # Crea directory
        os.makedirs("src/web/templates", exist_ok=True)
        os.makedirs("src/web/static", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        
        # Controlla prerequisites
        self.check_prerequisites()
        
        # Genera file
        for file_path, generator in self.required_files.items():
            if not os.path.exists(file_path):
                print(f"📝 Generando {file_path}...")
                generator()
            else:
                print(f"✅ {file_path} già esiste")
        
        # Installa dipendenze
        print("\n📦 Installando dipendenze...")
        self.install_dependencies()
        
        # Commit su GitHub
        print("\n📤 Committando su GitHub...")
        self.commit_to_github()
        
        print("\n" + "="*70)
        print("✅ BETA PRONTA PER IL TEST!")
        print("="*70)
        print("\n🚀 Avvia con: python src/web/app.py")
        print("🌐 Accedi a: http://localhost:5000\n")
    
    def check_prerequisites(self):
        """Controlla prerequisiti"""
        print("🔍 Verifica prerequisiti...\n")
        
        required_env_vars = [
            "AZURE_AI_ENDPOINT",
            "AZURE_AI_KEY",
            "AZURE_AI_MODEL"
        ]
        
        missing = [var for var in required_env_vars if not os.getenv(var)]
        
        if missing:
            print(f"⚠️ Variabili d'ambiente mancanti: {missing}")
            print("\nCompilazione guidata:")
            
            for var in missing:
                value = input(f"  {var}: ").strip()
                os.environ[var] = value
                
                with open(".env", "a") as f:
                    f.write(f"{var}={value}\n")
        
        print("✅ Prerequisiti OK\n")
    
    def create_env_file(self):
        """Crea .env"""
        content = """# Azure AI Configuration
AZURE_AI_ENDPOINT=https://hub-assistente-ai.cognitiveservices.azure.com/
AZURE_AI_KEY=your-api-key-here
AZURE_AI_MODEL=gpt-4o-mini

# Flask Configuration
FLASK_ENV=production
FLASK_SECRET_KEY=your-secret-key-here

# Beta Configuration
BETA_MODE=True
AUTO_IMPROVE=True
"""
        with open(".env", "w") as f:
            f.write(content)
    
    def create_web_app(self):
        """Crea Flask app"""
        content = '''#!/usr/bin/env python3
import os
import sys
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Carica variabili
load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.avatar.animator import AvatarAnimator
from src.ai.azure_client import AzureAIClient
from src.utils.self_improvement import SelfImprovementEngine

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

# Inizializza componenti
try:
    animator = AvatarAnimator()
    ai_client = AzureAIClient()
    improvement_engine = SelfImprovementEngine(ai_client)
    print("✅ Componenti inizializzati")
except Exception as e:
    print(f"❌ Errore inizializzazione: {e}")

@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Ottieni risposta AI
        response = ai_client.chat(user_message)
        
        # Impara dalla conversazione
        satisfaction = improvement_engine.learn_from_conversation(
            user_message, 
            response
        )
        
        return jsonify({
            'response': response,
            'satisfaction': satisfaction,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """Ritorna status assistente"""
    try:
        status_data = improvement_engine.get_status()
        status_data['avatar_state'] = animator.current_state
        
        return jsonify(status_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/improve', methods=['POST'])
def improve():
    """Avvia auto-miglioramento"""
    try:
        improvements = improvement_engine.analyze_and_improve()
        report = improvement_engine.generate_improvement_report()
        improvement_engine.auto_update_github()
        
        return jsonify({
            'improvements': improvements,
            'report': report,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/task', methods=['POST'])
def execute_task():
    """Esegui task autonomo"""
    try:
        data = request.json
        task = data.get('task', '')
        
        plan = improvement_engine.execute_autonomous_task(task)
        
        return jsonify({
            'plan': plan,
            'status': 'executing'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
'''
        os.makedirs("src/web", exist_ok=True)
        with open("src/web/app.py", "w") as f:
            f.write(content)
    
    def create_html_template(self):
        """Crea HTML template"""
        content = '''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Assistente AI - Beta</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header>
            <h1>🤖 Assistente AI Personale</h1>
            <p>Beta Test v2.0 - Auto-miglioramento attivo</p>
        </header>
        
        <!-- Main Content -->
        <main>
            <!-- Avatar Section -->
            <section class="avatar-section">
                <div class="avatar-container">
                    <div class="avatar-placeholder">
                        <span id="avatar-emoji">😊</span>
                    </div>
                    <div class="status">
                        <p id="status-text">Pronto</p>
                    </div>
                </div>
            </section>
            
            <!-- Chat Section -->
            <section class="chat-section">
                <div class="chat-container">
                    <div id="messages" class="messages"></div>
                </div>
                
                <!-- Input -->
                <div class="input-section">
                    <textarea id="user-input" placeholder="Scrivi qui o descrivi un compito..." rows="3"></textarea>
                    <button id="send-btn" class="btn-primary">📤 Invia</button>
                </div>
                
                <!-- Actions -->
                <div class="actions">
                    <button id="improve-btn" class="btn-secondary">🔧 Migliora</button>
                    <button id="execute-btn" class="btn-secondary">🚀 Esegui Task</button>
                    <button id="status-btn" class="btn-secondary">📊 Statistiche</button>
                </div>
            </section>
        </main>
    </div>
    
    <!-- Stats Modal -->
    <div id="stats-modal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <h2>📊 Statistiche Assistente</h2>
            <div id="stats-content"></div>
        </div>
    </div>
    
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>'''
        os.makedirs("src/web/templates", exist_ok=True)
        with open("src/web/templates/index.html", "w") as f:
            f.write(content)
    
    def create_css(self):
        """Crea CSS"""
        content = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    text-align: center;
    color: white;
    margin-bottom: 30px;
}

header h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
}

main {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 20px;
    margin-bottom: 20px;
}

.avatar-section {
    background: white;
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.avatar-container {
    text-align: center;
}

.avatar-placeholder {
    font-size: 5em;
    margin-bottom: 20px;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.status {
    padding: 15px;
    background: #f0f0f0;
    border-radius: 10px;
}

.chat-section {
    background: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
}

.chat-container {
    flex: 1;
    overflow-y: auto;
    margin-bottom: 15px;
    min-height: 300px;
    border: 1px solid #eee;
    border-radius: 10px;
    padding: 15px;
}

.messages {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.message {
    padding: 12px 15px;
    border-radius: 10px;
    max-width: 80%;
    word-wrap: break-word;
}

.message.user {
    background: #667eea;
    color: white;
    align-self: flex-end;
}

.message.assistant {
    background: #f0f0f0;
    align-self: flex-start;
}

.input-section {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 10px;
    margin-bottom: 15px;
}

textarea {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-family: inherit;
    resize: none;
}

.btn-primary, .btn-secondary {
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1em;
    transition: all 0.3s;
}

.btn-primary {
    background: #667eea;
    color: white;
}

.btn-primary:hover {
    background: #5568d3;
}

.btn-secondary {
    background: #f0f0f0;
    color: #333;
    flex: 1;
}

.btn-secondary:hover {
    background: #e0e0e0;
}

.actions {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}

.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.4);
}

.modal-content {
    background-color: #fefefe;
    margin: 10% auto;
    padding: 30px;
    border-radius: 15px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}

.close {
    color: #aaa;
    float: right;
    font-size: 2em;
    cursor: pointer;
}

@media (max-width: 768px) {
    main {
        grid-template-columns: 1fr;
    }
    
    .actions {
        grid-template-columns: 1fr;
    }
}'''
        os.makedirs("src/web/static", exist_ok=True)
        with open("src/web/static/style.css", "w") as f:
            f.write(content)
    
    def create_javascript(self):
        """Crea JavaScript"""
        content = '''// Chat application
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
            
            this.addMessage('✨ Auto-miglioramento completato!\\n' + 
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
            this.addMessage('✅ Compito eseguito!\\nPiano: ' + 
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
});'''
        with open("src/web/static/script.js", "w") as f:
            f.write(content)
    
    def create_requirements(self):
        """Crea requirements.txt"""
        content = '''flask==2.3.2
python-dotenv==1.0.0
openai==2.6.1
Pillow==10.2.0
psutil==7.0.0
PyQt6==6.6.1
gunicorn==21.2.0
requests==2.31.0
'''
        with open("requirements.txt", "w") as f:
            f.write(content)
    
    def create_dockerfile(self):
        """Crea Dockerfile"""
        content = '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=src/web/app.py
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.web.app:app"]'''
        with open("Dockerfile", "w") as f:
            f.write(content)
    
    def install_dependencies(self):
        """Installa dipendenze"""
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, capture_output=True)
            print("✅ Dipendenze installate")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Errore installazione: {e}")
    
    def commit_to_github(self):
        """Commit su GitHub"""
        try:
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", 
                          "🚀 Beta Test - Interfaccia web e auto-miglioramento"],
                          check=True, capture_output=True)
            subprocess.run(["git", "push", "origin", "main"],
                          check=True, capture_output=True)
            print("✅ Committato su GitHub")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Git error: {e}")

if __name__ == "__main__":
    builder = AssistantBuilder()
    builder.build()
