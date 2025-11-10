import json
import re
import random

class InputAnalyzer:
    def __init__(self, chatbot, memory, logger):
        self.chatbot = chatbot
        self.memory = memory
        self.logger = logger

    def _detect_emotion(self, text: str):
        text_lower = text.lower()

        emotions = {
            "amor": ["te amo", "gosto de você", "❤", "💕", "😍", "😘", "linda", "fofa"],
            "alegria": ["haha", "kk", "feliz", "yay", "uhul", "😄", "😂", "😁"],
            "tristeza": ["triste", "😢", "😭", "infeliz", "solitário", "sozinho", "decepcionado"],
            "raiva": ["raiva", "ódio", "irritado", "puto", "🤬", "😠"],
            "timidez": ["😳", "😅", "hehe", "🙈", "envergonhado", "tímido"],
        }

        for emotion, patterns in emotions.items():
            if any(p in text_lower for p in patterns):
                return emotion

        # Se nada foi detectado → chance de emoção aleatória leve
        emotions_list = list(emotions.keys()) + ["neutra"]
        emotion = random.choices(
            emotions_list,
            weights=[10, 15, 8, 6, 8, 53],  # 53% neutra, resto distribuído
            k=1
        )[0]
        return emotion

    def _detect_intent(self, text: str):
        text_lower = text.lower()

        if re.search(r"\b(oi|olá|ola|hey|eai|salve|bom dia|boa tarde|boa noite)\b", text_lower):
            return "SAUDACAO"

        if re.search(r"\b(tchau|falou|até mais|ate logo|fui|durma bem|boa noite)\b", text_lower):
            return "DESPEDIDA"

        if re.search(r"\b(gosta|prefere|curte|seu anime favorito|jogo favorito|comida favorita)\b", text_lower):
            return "GOSTOS"

        if re.search(r"\b(o que faço|me ajuda|tô mal|to mal|não sei|aconteceu|conselho|preciso de ajuda)\b", text_lower):
            return "CONSELHO"

        if re.search(r"\b(piada|haha|kkk|engraçado|meme|zoar|trolar)\b", text_lower):
            return "HUMOR"

        if re.search(r"\b(código|bug|programa|erro|python|js|typescript|java|c#|api|backend|frontend)\b", text_lower):
            return "CODIGO"

        return "DESCONHECIDO"

    def analyze(self, text):
        """Decide a ação e emoção a partir do texto."""
        emotion = self._detect_emotion(text)
        intent = self._detect_intent(text)

        # Ajusta emoção por contexto de intenção (ex: piada → alegria)
        emotion_hint = {
            "SAUDACAO": "alegria",
            "GOSTOS": "alegria",
            "CONSELHO": "tristeza",
            "HUMOR": "alegria",
            "CODIGO": "neutra",
            "DESPEDIDA": "tristeza",
        }

        if intent in emotion_hint and (emotion == "neutra" or random.random() < 0.3):
            emotion = emotion_hint[intent]

        self.logger.log("debug", "InputAnalyzer", f"Intenção: {intent}, Emoção: {emotion}")

        # Se houver intenção clara, retorna diretamente
        if intent != "DESCONHECIDO":
            content = text if intent != "DESPEDIDA" else "Foi um prazer conversar com você, até logo!"
            return {"action": intent, "content": content, "emotion": emotion}

        # Caso ambíguo → pede ajuda ao modelo
        persona = self.memory.recall("persona") or ""
        actions_definition = """
        Ações possíveis:
        - "RESPOND": conversa normal.
        - "SAUDACAO": cumprimentos.
        - "GOSTOS": perguntas sobre preferências.
        - "CONSELHO": pedido de ajuda emocional.
        - "CODIGO": perguntas de programação.
        - "HUMOR": piadas ou brincadeiras.
        """

        prompt = f"""
        {persona}

        Analise a mensagem do usuário e determine a ação e emoção mais adequadas.

        {actions_definition}

        Retorne SOMENTE um JSON válido no formato:
        {{
            "action": "NOME_DA_ACAO",
            "content": "Texto da resposta",
            "emotion": "emoção_detectada"
        }}

        Mensagem do usuário: {text}
        """

        response = self.chatbot.ask(prompt)

        # Tenta decodificar o JSON com tolerância
        try:
            json_match = re.search(r"\{.*\}", response, re.S)
            if json_match:
                data = json.loads(json_match.group(0))
            else:
                raise json.JSONDecodeError("No JSON found", response, 0)
        except Exception as e:
            self.logger.log("warning", "InputAnalyzer", f"Falha ao interpretar resposta: {e} | {response}")
            data = {"action": "RESPOND", "content": text, "emotion": emotion}

        # Emoção fallback
        if not data.get("emotion"):
            data["emotion"] = emotion

        return data