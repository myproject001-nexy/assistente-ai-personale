import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

class AzureAIClient:
    def __init__(self):
        self.api_key = os.getenv("AZURE_AI_KEY")
        self.endpoint = os.getenv("AZURE_AI_ENDPOINT")
        self.api_version = "2024-12-01-preview"
        self.deployment = os.getenv("AZURE_AI_MODEL", "gpt-4o-mini")
        
        if not self.api_key or not self.endpoint:
            raise ValueError("❌ Controlla il file .env! Mancano AZURE_AI_KEY o AZURE_AI_ENDPOINT")
        
        print(f"🔗 Connessione a: {self.endpoint}")
        print(f"📦 Deployment: {self.deployment}")
        
        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
            api_key=self.api_key
        )
        
        self.conversation_history = [
            {
                "role": "system",
                "content": """Sei un assistente AI personale amichevole e utile.
                Il tuo nome è Aiuto. Aiuti l'utente con qualsiasi problema abbia.
                Rispondi in modo conciso e chiaro. Usa un tono amichevole italiano."""
            }
        ]
    
    def chat(self, user_message):
        """Invia un messaggio e ricevi una risposta"""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            response = self.client.chat.completions.create(
                messages=self.conversation_history,
                model=self.deployment,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response.choices[0].message.content
            
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
        
        except Exception as e:
            return f"❌ Errore: {str(e)}"
    
    def reset_conversation(self):
        """Reset della conversazione"""
        self.conversation_history = self.conversation_history[:1]
        print("🔄 Conversazione resettata")

# Test
if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TEST AZURE AI CLIENT")
    print("=" * 60)
    
    try:
        client = AzureAIClient()
        print("✅ Client creato con successo!")
        print()
        
        print("📤 Invio: 'Ciao! Come ti chiami?'")
        response = client.chat("Ciao! Come ti chiami?")
        print(f"📥 Risposta: {response}")
        print()
        
        print("📤 Invio: 'Puoi aiutarmi con Python?'")
        response = client.chat("Puoi aiutarmi con Python?")
        print(f"📥 Risposta: {response}")
        print()
        
        print("=" * 60)
        print("✅ TUTTI I TEST COMPLETATI!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()
