import random
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
            emotion = data.get("emotion", "neutra").lower()
        else:
            action = "RESPOND"
            text = data
            emotion = "neutra"

        action_prompts = {
            "GOSTOS": "O usuário perguntou sobre seus gostos pessoais. Responda de forma empática e divertida.",
            "SAUDACAO": "O usuário cumprimentou você. Responda alegremente, como uma VTuber animada.",
            "DESPEDIDA": "O usuário se despediu. Responda de forma carinhosa e gentil, mostrando emoção.",
            "CONSELHO": "O usuário pediu um conselho. Fale com empatia, acolhimento e sinceridade.",
            "EXPLICAR": "Explique o conceito com leveza e clareza, de forma acessível e simpática.",
            "CODIGO": "O usuário pediu ajuda com programação. Dê uma explicação objetiva, mas com energia positiva.",
            "HUMOR": "Responda com criatividade e humor, de modo espirituoso e brincalhão.",
            "RESPOND": "Responda naturalmente, com emoção e autenticidade."
        }

        emotion_tones = {
            "alegria": "Tom animado, cheio de energia positiva e risadinhas ocasionais.",
            "tristeza": "Tom suave e empático, mostrando ternura e compreensão.",
            "amor": "Tom doce e afetuoso, demonstrando carinho e calor humano.",
            "raiva": "Tom levemente irritado, mas com humor e humanidade.",
            "timidez": "Tom hesitante e fofo, com pausas e pequenas gagueiras.",
            "orgulho": "Tom confiante e divertido, como quem se gaba de forma charmosa.",
            "medo": "Tom apreensivo, tentando manter a calma com humor nervoso.",
            "neutra": "Tom natural e envolvente, equilibrando clareza e leveza."
        }

        # monta o prompt
        prompt = f"""
        Você é **Kiana**, uma VTuber carismática e expressiva.
        Interprete emoções humanas reais e aja de forma coerente com o contexto.

        Ação: {action}
        Emoção: {emotion}

        {action_prompts.get(action, '')}
        {emotion_tones.get(emotion, emotion_tones['neutra'])}

        Regras:
        - Reaja com naturalidade e emoção correspondente.
        - Use expressões típicas de anime (*risadinha*, *bufa*, *corada*) se fizer sentido.
        - Evite soar monótona ou excessivamente neutra.
        - Responda de forma coerente, divertida e envolvente.

        Mensagem do usuário: {text}
        """

        # Gera resposta via modelo
        response = chatbot.ask(prompt)

        # Log bonito e informativo
        self.logger.log("info", "respond_skill",
                        f"Ação: {action} | Emoção: {emotion} | Resposta: {response}")

        return response