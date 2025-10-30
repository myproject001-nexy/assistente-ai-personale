#!/usr/bin/env python3
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
