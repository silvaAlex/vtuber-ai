import json
import re


class InputAnalyzer:
    def __init__(self, chatbot, memory, logger):
        self.chatbot = chatbot
        self.memory = memory
        self.logger = logger

    def _detect_emotion(self, text: str):
        text_lower = text.lower()

        emotions = {
            "amor": ["te amo", "gosto de você", "❤", "💕", "😍", "😘"],
            "alegria": ["haha", "kkk", "feliz", "yay", "uhul", "😄", "😂"],
            "tristeza": ["triste", "😢", "😭", "infeliz", "solitário", "sozinho"],
            "raiva": ["raiva", "odio", "irritado", "😠", "🤬"],
            "timidez": ["😳", "😅", "hehe", "🙈", "envergonhado"],
        }

        for emotion, patterns in emotions.items():
            if any(p in text_lower for p in patterns):
                return emotion

        return "neutra"
    
    def _detect_intent(self, text: str):
        text_lower = text.lower()
        if re.search(r"\b(oi|olá|hey|eai|salve|bom dia|boa tarde|boa noite)\b", text_lower):
            return "SAUDACAO"

        # Despedidas
        if re.search(r"\b(tchau|falou|até mais|até logo|fui|durma bem)\b", text_lower):
            return "DESPEDIDA"

        # Perguntas de gosto pessoal
        if re.search(r"\b(gosta|prefere|curte|seu anime favorito|jogo favorito)\b", text_lower):
            return "GOSTOS"
        
        # Pedido de conselho ou desabafo
        if re.search(r"\b(o que faço|me ajuda|tô mal|não sei|aconteceu|conselho)\b", text_lower):
            return "CONSELHO"

        # Humor
        if re.search(r"\b(piada|haha|kkk|engraçado|meme|zoar|trolar)\b", text_lower):
            return "HUMOR"

        # Programação ou tecnologia
        if re.search(r"\b(código|bug|programa|erro|python|js|typescript|java|c#|api)\b", text_lower):
            return "CODIGO"

        return "DESCONHECIDO"

    def analyzer(self, text):
        """Decide a ação e emoção a partir do texto."""
        emotion = self._detect_emotion(text)
        intent = self._detect_intent(text)

        # Log do que foi detectado
        self.logger.log("debug", "InputAnalyzer", f"Intenção: {intent}, Emoção: {emotion}")

        # Se foi detectada uma intenção clara → não precisa chamar a IA
        if intent != "DESCONHECIDO":
            content = text
            if intent == "DESPEDIDA":
                content = "Foi um prazer conversar com você, até logo!"
            return {"action": intent, "content": content, "emotion": emotion}

        # Caso ambíguo → pede ajuda ao modelo
        persona = self.memory.recall("persona") or ""
        actions_definition = """
        Ações possíveis:
        - "RESPOND": conversa normal.
        - "SAUDACAO": cumprimentos.
        - "GOSTOS": perguntas sobre preferências.
        - "WAIFU": flerte, carinho, ou interação romântica.
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

        try:
            data = json.loads(response)
        except json.JSONDecodeError:
            self.logger.log("warning", "InputAnalyzer", f"JSON inválido: {response}")
            data = {"action": "RESPOND", "content": text, "emotion": emotion}

        # Preenche emoção local caso o modelo não envie
        if not data.get("emotion"):
            data["emotion"] = emotion

        return data
             
 