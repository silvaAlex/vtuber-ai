from core.chatbot_engine import ChatbotEngine
from utils.applogger import AppLogger

class Skill:
    name = "respond"
    aliases = ["responder", "reply"]

    def __init__(self, logger: AppLogger):
        self.logger = logger or AppLogger(name="RespondAI")

    def run(self,chatbot: ChatbotEngine, text):
        response = chatbot.ask(text)
        self.logger.log("info", "respond_skill", f"Waifu respondeu: {response}")

        return response
