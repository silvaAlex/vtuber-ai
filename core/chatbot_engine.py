import json
import os
import random
from dotenv import load_dotenv
import ollama
import requests
from core.memory_manager import MemoryManager
from utils.applogger import AppLogger


class ChatbotEngine:
    def __init__(self, logger: AppLogger, memory_manager: MemoryManager):

        load_dotenv()
        
        self.logger = logger
        self.model = os.getenv("MODEL_IA", "llama")
        self.client = ollama.Client(host="http://localhost:11434")
        self.memory = memory_manager
        self.context = []

        with open("config/ollama_model.json", 'r') as openfile:
            self.model_configs = json.load(openfile)

        self._max_tokens = 300
        self._max_context = int(os.environ.get("TOKEN_LIMIT"))
        self._stop = ["[System", "\nUser:", "---", "<|", "###"]
        self._newline_cut = os.getenv("NEWLINE_CUT_BOOT") == "ON"
        self._asterisk_ban = False

        if self._newline_cut:
            self._stop.append("\n")
        if self._asterisk_ban:
            self._stop.append("*")

    def ask(self, user_text):
        try:
            base_msg = self.context + [{"role": "user", "content": user_text}]
            
            if self.memory:
                messages = self.memory.inject_context(base_msg)
            else:
                messages = base_msg

            temp_level = random.randint(0, len(self.model_configs) - 1)

            self.logger.log("debug", "ChatbotEngine", f"Temperatura sorteada: nível {temp_level}")

            options = self._get_temperature_options(temp_level=temp_level)
            
            response = self.client.chat(
                model= self.model,
                messages= messages,
                options= options
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
        
    def update_context(self, role, content, max_length=15):
        self.context.append({"role": role, "content": content})
        if len(self.context) > max_length:
            self.context = self.context[-max_length:]

    def _get_temperature_options(self,temp_level=1):
        """Retorna as opções de geração de texto de acordo com o nível de temperatura."""
        if temp_level == -1:
            return None
        
        # Protege contra índice inválido
        if temp_level < 0 or temp_level >= len(self.model_configs):
            temp_level = 1  # fallback seguro

        config = self.model_configs[temp_level]

        # Log detalhado de parâmetros
        self.logger.log(
            "debug",
            "ChatbotEngine",
            f"Usando config: temp={config['temperature']} | top_p={config['top_p']} | top_k={config['top_k']}"
        )

        return {
            "temperature": config["temperature"],
            "min_p": config["min_p"],
            "top_p": config["top_p"],
            "top_k": config["top_k"],
            "num_ctx": self._max_context,
            "repeat_penalty": config["repeat_penalty"],
            "stop": self._stop,
            "num_predict": self._max_tokens ,
            "repeat_last_n": config["repeat_last_n"],
            "frequency_penalty": config["frequency_penalty"],
            "presence_penalty": config["presence_penalty"]
        }

