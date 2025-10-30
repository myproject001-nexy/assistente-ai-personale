import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from avatar.animator import AvatarAnimator
from ai.azure_client import AzureAIClient

def main():
    print("\n" + "="*60)
    print("🤖 ASSISTENTE AI - VERSIONE CLI")
    print("="*60 + "\n")
    
    try:
        animator = AvatarAnimator()
        ai_client = AzureAIClient()
        
        print("✅ Assistente pronto!\n")
        print("Scrivi 'exit' per uscire\n")
        
        while True:
            user_input = input("👤 Tu: ").strip()
            
            if user_input.lower() == "exit":
                print("\n👋 Arrivederci!")
                break
            
            if not user_input:
                continue
            
            print("\n🤔 Sto pensando...")
            animator.set_state("thinking")
            
            response = ai_client.chat(user_input)
            
            print(f"\n🤖 Assistente: {response}\n")
            animator.set_state("happy")
            
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
