import sys
import os
import json
import time
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QTextEdit, 
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage, QFont
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from avatar.animator import AvatarAnimator
from ai.azure_client import AzureAIClient

class ChatWindow(QMainWindow):
    """Finestra di chat interattiva con avatar animato"""
    
    def __init__(self):
        super().__init__()
        
        try:
            print("🎨 Inizializzazione avatar...")
            self.animator = AvatarAnimator()
            print("✅ Avatar pronto!")
            
            print("🧠 Inizializzazione AI...")
            self.ai_client = AzureAIClient()
            print("✅ AI pronto!")
        except Exception as e:
            print(f"❌ Errore: {e}")
            return
        
        self.setup_ui()
        self.show()
    
    def setup_ui(self):
        """Crea l'interfaccia grafica"""
        self.setWindowTitle("💬 Assistente AI - Chat")
        self.setGeometry(100, 100, 900, 600)
        
        # Widget principale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout()
        
        # SEZIONE SINISTRA: Avatar
        left_layout = QVBoxLayout()
        self.avatar_label = QLabel()
        self.update_avatar()
        left_layout.addWidget(self.avatar_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Status
        self.status_label = QLabel("😊 Pronto!")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: green; font-weight: bold; font-size: 14px;")
        left_layout.addWidget(self.status_label)
        
        # SEZIONE DESTRA: Chat
        right_layout = QVBoxLayout()
        
        # Chat display
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.addStretch()
        self.chat_container.setLayout(self.chat_layout)
        
        scroll_area.setWidget(self.chat_container)
        right_layout.addWidget(scroll_area)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(80)
        self.input_field.setPlaceholderText("Scrivi qui...")
        input_layout.addWidget(self.input_field)
        
        send_btn = QPushButton("📤 Invia")
        send_btn.clicked.connect(self.send_message)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #1565C0; }
        """)
        input_layout.addWidget(send_btn)
        
        right_layout.addLayout(input_layout)
        
        # Aggiungi sezioni
        left_container = QWidget()
        left_container.setLayout(left_layout)
        left_container.setMaximumWidth(350)
        
        right_container = QWidget()
        right_container.setLayout(right_layout)
        
        layout.addWidget(left_container)
        layout.addWidget(right_container)
        
        central_widget.setLayout(layout)
        
        # Messaggio di benvenuto
        self.add_message("Ciao! Sono il tuo assistente AI. Come posso aiutarti? 😊", "assistant")
    
    def send_message(self):
        """Invia messaggio"""
        user_text = self.input_field.toPlainText().strip()
        
        if not user_text:
            return
        
        # Mostra messaggio utente
        self.add_message(user_text, "user")
        self.input_field.clear()
        
        # Status: pensiero
        self.status_label.setText("🤔 Penso...")
        self.animator.set_state("thinking")
        self.update_avatar()
        
        try:
            # Ottieni risposta AI
            response = self.ai_client.chat(user_text)
            
            # Status: parlando
            self.status_label.setText("🗣️ Parlo...")
            self.animator.set_state("talking")
            self.update_avatar()
            
            # Mostra risposta
            self.add_message(response, "assistant")
            
            # Status: felice
            self.animator.set_state("happy")
            self.update_avatar()
            time.sleep(0.5)
            
        except Exception as e:
            self.add_message(f"❌ Errore: {str(e)}", "assistant")
        
        # Ritorna a idle
        self.animator.set_state("idle")
        self.update_avatar()
        self.status_label.setText("😊 Pronto!")
    
    def add_message(self, text, speaker):
        """Aggiunge messaggio al chat"""
        label = QLabel(text)
        label.setWordWrap(True)
        label.setMaximumWidth(400)
        
        if speaker == "user":
            label.setStyleSheet("""
                QLabel {
                    background-color: #F3E5F5;
                    border: 2px solid #7B1FA2;
                    border-radius: 10px;
                    padding: 10px;
                    color: #000;
                }
            """)
            self.chat_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignRight)
        else:  # assistant
            label.setStyleSheet("""
                QLabel {
                    background-color: #E3F2FD;
                    border: 2px solid #1976D2;
                    border-radius: 10px;
                    padding: 10px;
                    color: #000;
                }
            """)
            self.chat_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Scroll down
        self.chat_container.adjustSize()
    
    def update_avatar(self):
        """Aggiorna avatar display"""
        try:
            image = self.animator.get_current_image()
            if image:
                img_array = np.array(image.convert('RGBA'))
                height, width, channel = img_array.shape
                bytes_per_line = 4 * width
                
                q_image = QImage(
                    img_array.tobytes(),
                    width,
                    height,
                    bytes_per_line,
                    QImage.Format.Format_RGBA8888
                )
                
                pixmap = QPixmap.fromImage(q_image)
                pixmap = pixmap.scaledToWidth(300, Qt.TransformationMode.SmoothTransformation)
                self.avatar_label.setPixmap(pixmap)
        except Exception as e:
            print(f"❌ Errore avatar: {e}")

def main():
    app = QApplication(sys.argv)
    window = ChatWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()