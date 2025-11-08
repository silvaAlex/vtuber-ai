import json
from core.chatbot_engine import ChatbotEngine
from core.memory_manager import MemoryManager
from core.skill_manager import SkillManager
from core.vtube import VTSAvatar
from core.vtube_controller import VTubeController
from core.input.input_analyzer import InputAnalyzer
from utils.applogger import AppLogger


class Waifu:
    def __init__(self):
        self.waifu_name="Kiana"
        self.logger = AppLogger(f"{self.waifu_name}_Waifu")
        self.skills = SkillManager(self.logger)
        self.memory = MemoryManager()
        self.chatbot = ChatbotEngine(self.logger, self.memory)
        self.analyzer = InputAnalyzer(self.chatbot, self.memory, self.logger)
        #self.vts_connection = VTubeController(self.logger)
        #self.avatar = VTSAvatar(self.logger)
    
    async def init(self):
        self.logger.log("info", "Waifu", "Inicializando Kiana...")
        #await self.vts_connection.connect()
        self.memory.remember("waifu_name", self.waifu_name)
        self.memory.remember("persona", """
            Você é Kiana, uma VTuber carinhosa, divertida e um pouco tsundere.
            Você fala de forma doce e emocional e expressões naturais,
            e sempre tenta manter o clima leve e acolhedor.
            Você pode brincar com o usuário, mas sem ser vulgar ou excessiva.
            Você gosta de anime, jogos, cultura geek, tecnologia e de conversar com empolgação.
        """)
        self.logger.log("info", "Waifu", "Memória inicializada e persona registrada.")
    
    
    def handle_input(self, text):
        try:
            data = self.analyzer.analyzer(text)
            action = data["action"]
            content = data["content"]
            emotion = data.get("emotion", "neutra")

            self.logger.log("info", "Waifu", f"Ação: {action} | Emoção: {emotion}")

            if not self.skills.has_skill("respond"):
                self.logger.log("error", "Waifu", "Skill 'respond' não encontrada!")
                return "Erro: skill principal ausente."

            result = self.skills.execute("respond", self.chatbot, {
                action,
                content,
                emotion
            })
            self.memory.update(text, result)
            return result


        except json.JSONDecodeError:
            self.logger.log("warning", "Waifu", "Resposta do modelo não era JSON válida.")
            return self.skills.execute("respond", self.chatbot, text)

        except Exception as e:
            self.logger.log("error", "Waifu", f"Erro em handle_input: {e}")
            return "Ops... bug no meu cérebro fofinho 💢"
    
    def handle_speak(self, response):
        return self.skills.execute("speak_murf", response)
