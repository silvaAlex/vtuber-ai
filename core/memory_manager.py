import json

class MemoryManager:
    def __init__(self, short_limit=10):
        self.short_term = []
        self.long_term = {}
        self.short_limit = short_limit

    def inject_context(self, messages):
        """Injeta memórias recentes, persona e resumo no contexto do modelo."""
        context_msgs = []

        # Memória curta (últimas interações)
        for msg in self.short_term[-self.short_limit:]:
            context_msgs.append({"role": "user", "content": msg["user"]})
            context_msgs.append({"role": "assistant", "content": msg["ai"]})

        # Persona fixa (identidade da VTuber)
        persona = self.long_term.get("persona")
        if persona:
            context_msgs.insert(0, {"role": "system", "content": persona})

        # Resumo de sessões anteriores
        summary = self.long_term.get("summary")
        if summary:
            context_msgs.insert(1, {
                "role": "system",
                "content": f"Resumo das conversas anteriores: {summary}"
            })

        return context_msgs + messages

    def update(self, user_text, ai_text, chatbot=None):
        """Atualiza a memória de curto prazo e gera resumo se estiver cheia."""
        if self.short_term and self.short_term[-1]["user"] == user_text:
            return  # evita duplicar mensagens idênticas

        self.short_term.append({"user": user_text, "ai": ai_text})

        if len(self.short_term) > self.short_limit:
            # Se o chatbot for fornecido, cria um resumo antes de limpar
            if chatbot:
                self.summarize_short_term(chatbot)
            self.short_term.pop(0)

    def remember(self, key, value):
        """Guarda dados persistentes (memória longa)."""
        self.long_term[key] = value

    def recall(self, key):
        """Recupera dados persistentes."""
        return self.long_term.get(key)

    def save(self, path="memory.json"):
        """Salva memórias em disco."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump({
                "short_term": self.short_term,
                "long_term": self.long_term
            }, f, ensure_ascii=False, indent=2)

    def load(self, path="memory.json"):
        """Carrega memórias salvas (caso existam)."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.loads(f)
                self.short_term = data.get("short_term", [])
                self.long_term = data.get("long_term", {})
        except FileNotFoundError:
            pass

    def summarize_short_term(self, chatbot):
        """Cria um resumo emocional e semântico das últimas conversas."""
        if not self.short_term:
            return None

        # Monta um pequeno log das conversas recentes
        log = ""
        for msg in self.short_term[-self.short_limit:]:
            log += f"Usuário: {msg['user']}\n"
            log += f"Kiana: {msg['ai']}\n"

        prompt = f"""
        Você é uma assistente que resume conversas de forma breve e emocional.
        Abaixo está um trecho de diálogo entre o usuário e Kiana (uma VTuber expressiva e divertida).
        Gere um pequeno resumo (até 100 palavras) explicando:
        - o principal tema das conversas
        - o clima emocional (brincalhão, técnico, carinhoso, etc.)
        - como Kiana se comportou e como o usuário reagiu.
        Escreva de modo natural, como uma nota de diário curta.

        Conversa recente:
        {log}
        """

        try:
            summary = chatbot.ask(prompt, temperature=0.5)
            if summary:
                self.long_term["summary"] = summary.strip()
                return summary
        except Exception as e:
            print(f"[MemoryManager] Erro ao resumir memória: {e}")
            return None
