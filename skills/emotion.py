from core.vtube import VTSAvatar
from utils.applogger import AppLogger

EMOTION_TO_HOTKEY = {
    "alegria": "Remove Expressions",
    "tristeza": "Eyes Cry",
    "amor": "Heart Eyes",
    "raiva": "Angry Sign",
    "surpresa": "Shock Sign",
    "timidez": "Anim Shake",
    "neutra": "Remove Expressions"
}

class Skill:
    name = "emotion"
    aliases = ["express", "vts_emotion"]

    def __init__(self, logger: AppLogger):
        self.logger = logger or AppLogger(name="EmotionSkill")

    async def run(self, emotion: str, avatar: VTSAvatar):
        try:
            hotkey_name = EMOTION_TO_HOTKEY.get(emotion, "Remove Expressions")
            await avatar.trigger_hotkey(hotkey_name)
            self.logger.log("info", "EmotionSkill", f"Expressão '{emotion}' → Hotkey '{hotkey_name}'")
        except Exception as e:
            self.logger.log("error", "EmotionSkill", f"Erro ao trocar emoção: {e}")