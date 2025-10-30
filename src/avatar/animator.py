import os
import time
from PIL import Image

class AvatarAnimator:
    """Gestisce le animazioni dell'avatar dell'assistente"""
    
    def __init__(self):
        self.current_state = "idle"
        self.states = {
            "idle": "assets/images/idle.png",
            "talking": "assets/images/talking.png",
            "thinking": "assets/images/thinking.png",
            "happy": "assets/images/happy.png"
        }
        
        self.images = {}
        self.load_images()
    
    def load_images(self):
        """Carica tutte le immagini degli stati"""
        print("🎨 Caricamento immagini avatar...")
        
        for state, path in self.states.items():
            if os.path.exists(path):
                try:
                    self.images[state] = Image.open(path)
                    print(f"✅ Caricato: {state} ({path})")
                except Exception as e:
                    print(f"❌ Errore nel caricamento di {path}: {e}")
            else:
                print(f"⚠️ File non trovato: {path}")
        
        if not self.images:
            print("❌ ERRORE: Nessuna immagine caricata!")
        else:
            print(f"✅ Immagini caricate: {list(self.images.keys())}")
    
    def set_state(self, state):
        """Cambia lo stato dell'avatar"""
        if state in self.states:
            self.current_state = state
            print(f"🔄 Stato cambiato: {state}")
        else:
            print(f"⚠️ Stato non valido: {state}")
    
    def get_current_image(self):
        """Ritorna l'immagine dello stato corrente"""
        return self.images.get(self.current_state)
    
    def animate_talking(self, duration=1.0):
        """Anima l'avatar mentre parla"""
        print(f"🗣️ Animazione talking per {duration} secondi...")
        self.set_state("talking")
        time.sleep(duration)
        self.set_state("idle")
    
    def animate_thinking(self, duration=2.0):
        """Anima l'avatar mentre pensa"""
        print(f"🤔 Animazione thinking per {duration} secondi...")
        self.set_state("thinking")
        time.sleep(duration)
        self.set_state("idle")
    
    def animate_happy(self, duration=1.5):
        """Anima l'avatar felice"""
        print(f"😊 Animazione happy per {duration} secondi...")
        self.set_state("happy")
        time.sleep(duration)
        self.set_state("idle")
    
    def get_available_states(self):
        """Ritorna gli stati disponibili"""
        return list(self.images.keys())


# Test dell'animator
if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TEST AVATAR ANIMATOR")
    print("=" * 60)
    
    # Crea animator
    animator = AvatarAnimator()
    
    # Verifica immagini caricate
    if animator.images:
        print(f"\n✅ Stati disponibili: {animator.get_available_states()}")
        
        # Test cambio stati
        print("\n🔄 Test cambio stati:")
        animator.set_state("idle")
        time.sleep(0.5)
        
        animator.set_state("talking")
        time.sleep(0.5)
        
        animator.set_state("thinking")
        time.sleep(0.5)
        
        animator.set_state("happy")
        time.sleep(0.5)
        
        animator.set_state("idle")
        
        print("\n✅ Test completato con successo!")
    else:
        print("\n❌ ERRORE: Immagini non caricate correttamente!")
        print("Verifica che le immagini siano in assets/images/")
    
    print("=" * 60)
