
from pathlib import Path
import ollama
import requests

import yaml
from utils.applogger import AppLogger


class ChatbotEngine:
    def __init__(self, logger: AppLogger):
        self.logger = logger
        self.model = "kiana" #ollama-model
        self.client = ollama.Client(host="http://localhost:11434")
        self.context = []

    def ask(self, user_text, temperature=0.6):
        try:
            messages = self.context + [{"role": "user", "content": user_text}]
            response = self.client.chat(
                model= self.model,
                messages= messages,
                options={
                    "temperature": temperature
                }
            )
            message = response["message"]["content"]

            self.context = response.get("context", self.context)

            if not message:
                self.logger.log("warning","ChatbotEngine","Modelo não retornou conteúdo.")
                return "Hmmm... não consigo pensar em nada agora."

            return message.strip()
        except requests.exceptions.RequestException as e:
            self.logger.log("error","ChatbotEngine",f"Erro ao conectar com Ollama: {e}")
            return "Desculpe, perdi a conexão com meu cérebro eletrônico por um momento."
        
   