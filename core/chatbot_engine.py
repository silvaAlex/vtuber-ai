import ollama
import requests
from core.memory_manager import MemoryManager
from utils.applogger import AppLogger


class ChatbotEngine:
    def __init__(self, logger: AppLogger, memory_manager: MemoryManager):
        self.logger = logger
        self.model = "kiana" #ollama-model
        self.client = ollama.Client(host="http://localhost:11434")
        self.memory = memory_manager
        self.context = []

    def ask(self, user_text, temperature=0.6):
        try:
            base_msg = self.context + [{"role": "user", "content": user_text}]
            
            if self.memory:
                messages = self.memory.inject_context(base_msg)
            else:
                messages = base_msg
            
            
            response = self.client.chat(
                model= self.model,
                messages= messages,
                options={
                    "temperature": temperature
                }
            )
            
            ai_text = response["message"]["content"]

            if self.memory:
                self.memory.update(user_text, ai_text)

            if not ai_text:
                self.logger.log("warning","ChatbotEngine","Modelo não retornou conteúdo.")
                return "Hmmm... não consigo pensar em nada agora."
        
            return ai_text.strip()
        except requests.exceptions.RequestException as e:
            self.logger.log("error","ChatbotEngine",f"Erro ao conectar com Ollama: {e}")
            return "Desculpe, perdi a conexão com meu cérebro eletrônico por um momento."
        
   