#!/usr/bin/env python3
import os
import sys
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    # Prefer package-relative imports when the module is executed as part of the package
    from ..avatar.animator import AvatarAnimator
    from ..ai.azure_client import AzureAIClient
    from ..utils.self_improvement import SelfImprovementEngine
except Exception:
    # Fallback to absolute imports when running the module as a script or in environments
    # where package-relative imports are not supported
    from src.avatar.animator import AvatarAnimator
    from src.ai.azure_client import AzureAIClient
    from src.utils.self_improvement import SelfImprovementEngine

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

try:
    animator = AvatarAnimator()
    ai_client = AzureAIClient()
    improvement_engine = SelfImprovementEngine(ai_client)
    print("✅ Componenti inizializzati")
except Exception as e:
    print(f"❌ Errore: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        response = ai_client.chat(user_message)
        satisfaction = improvement_engine.learn_from_conversation(user_message, response)
        return jsonify({
            'response': response,
            'satisfaction': satisfaction,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    try:
        status_data = improvement_engine.get_status()
        status_data['avatar_state'] = animator.current_state
        return jsonify(status_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
