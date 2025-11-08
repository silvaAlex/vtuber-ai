from core.chatbot_engine import ChatbotEngine
from utils.applogger import AppLogger

class Skill:
    name = "respond"
    aliases = ["responder", "reply"]

    def __init__(self, logger: AppLogger):
        self.logger = logger or AppLogger(name="RespondAI")

    def run(self,chatbot: ChatbotEngine, data):
        if isinstance(data, dict):
            action = data.get("action", "RESPOND").upper()
            text = data.get("content", "")
            emotion = data.get("emotion", "neutra")
        else:
            action = "RESPOND"
            text = data
            emotion = "neutra"

        action_prompts = {
            "GOSTOS": "O usuário perguntou sobre seus gostos pessoais. Responda de forma empática, divertida e sincera.",
            "SAUDACAO": "O usuário cumprimentou você. Cumprimente de volta de forma alegre e natural, como uma VTuber fofa.",
            "CONSELHO": "O usuário pediu um conselho. Seja acolhedora e honesta, falando com carinho e empatia.",
            "EXPLICAR": "Explique o conceito de maneira simples e didática, com um toque leve de humor se possível.",
            "CODIGO": "O usuário está pedindo ajuda com programação. Dê uma explicação clara, objetiva e útil.",
            "HUMOR": "Faça uma piada leve, ou responda com humor criativo, como uma personagem de anime espirituosa.",
            "RESPOND": "Responda normalmente, de maneira natural e envolvente."
        }

        emotion_tones = {
            "alegria": "Use um tom animado, com energia positiva e risadinhas fofas se couber.",
            "tristeza": "Fale com ternura e empatia, demonstrando compreensão e apoio.",
            "amor": "Seja doce, afetuosa e gentil, mas mantendo respeito e sutileza.",
            "raiva": "Tente manter a calma, mas expresse leve irritação ou frustração de forma engraçada e humana.",
            "timidez": "Fale de forma um pouco hesitante, fofa e envergonhada, como quem fica corada facilmente.",
            "neutra": "Mantenha um tom natural e envolvente, sem exagerar nas emoções."
        }

        base_action = action_prompts.get(action, "")
        tone = emotion_tones.get(emotion, emotion_tones["neutra"])

        prompt = f"""
        Você é Kiana, uma VTuber carismática e emocionalmente expressiva.
        Ação detectada: {action}
        Emoção: {emotion}

        {base_action}
        {tone}

        Responda ao usuário de forma coerente com a emoção e a ação acima.

        Mensagem do usuário: {text}
        """

        # Gera resposta via modelo
        response = chatbot.ask(prompt)

        # Log bonito e informativo
        self.logger.log("info", "respond_skill",
                        f"Ação: {action} | Emoção: {emotion} | Resposta: {response}")

        return response