
from core.chatbot_engine import ChatbotEngine
from core.skill_manager import SkillManager
from core.vtube import VTSAvatar
from core.vtube_controller import VTubeController
from utils.applogger import AppLogger


class Waifu:
    def __init__(self):
        self.waifu_name="Kiana"
        self.logger = AppLogger(f"{self.waifu_name}_Waifu")
        self.skills = SkillManager(self.logger)
        self.chatbot = ChatbotEngine(self.logger)
        #self.vts_connection = VTubeController(self.logger)
        #self.avatar = VTSAvatar(self.logger)
    
    async def init(self):
        #await self.vts_connection.connect()
        self.skills.load_skill("respond")
        self.skills.load_skill("speak_murf")
    
    def handle_input(self, text):
        return self.skills.execute("respond",self.chatbot, text)
    
    def handle_speak(self, response):
        return self.skills.execute("speak_murf", response)
