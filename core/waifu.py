import json
from core.chatbot_engine import ChatbotEngine
from core.memory_manager import MemoryManager
from core.skill_manager import SkillManager
from core.vtube import VTSAvatar
from core.vtube_controller import VTubeController
from utils.applogger import AppLogger


class Waifu:
    def __init__(self):
        self.waifu_name="Kiana"
        self.logger = AppLogger(f"{self.waifu_name}_Waifu")
        self.skills = SkillManager(self.logger)
        self.memory = MemoryManager()
        self.chatbot = ChatbotEngine(self.logger, self.memory)
        #self.vts_connection = VTubeController(self.logger)
        #self.avatar = VTSAvatar(self.logger)
    
    async def init(self):
        self.logger.log("info", "Waifu", "Inicializando Kiana...")
        #await self.vts_connection.connect()
        self.memory.remember("waifu_name", self.waifu_name)
        self.logger.log("info", "Waifu", "Memória inicializada.")
    
    
    def handle_input(self, text):
        try:
            response = self.chatbot.ask(
                f"""
                    Analise a seguinte mensagem do usuário e decida:
                    1. Qual ação executar (skill registrada)
                    2. O conteúdo a ser falado

                    Retorne APENAS em um JSON no formato:
                    {{
                        "action": "nome_skill",
                        "content": "texto da resposta"
                    }}

                    Mensagem: {text}
                """
            )

            data = json.loads(response)
            action = data.get("action", "respond")
            content = data.get("content", "")

            self.logger.log("info", "Waifu", f"Ação decidida: {action}")

            if not self.skills.has_skill(action):
                self.logger.log("warning", "Waifu", f"Skill '{action}' não encontrada. Usando 'respond'.")
                action = "respond"

            result =  self.skills.execute(action, self.chatbot, content)

            self.memory.update(text, result)

            return result

        except json.JSONDecodeError:
            self.logger.log("warning", "Waifu", "Resposta do modelo não era JSON válida.")
            return self.skills.execute("respond", self.chatbot, text)

        except Exception as e:
            self.logger.log("error", "Waifu", f"Erro em handle_input: {e}")
            return "Houve um erro interno na minha central de processamento fofinho."
    
    def handle_speak(self, response):
        return self.skills.execute("speak_murf", response)
