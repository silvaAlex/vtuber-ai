class MemoryManager:
    def __init__(self, short_limit=10):
        self.short_term = []
        self.long_term = {}
        self.short_limit = short_limit

    def inject_context(self, messages):
        context_msgs = []
        for msg in self.short_term[-self.short_limit:]:
            context_msgs.append({"role": "user", "content": msg["user"]})
            context_msgs.append({"role": "assistant", "content": msg["ai"]})
        return context_msgs + messages
    
    def update(self, user_text, ai_text):
        self.short_term.append({"user": user_text, "ai": ai_text})
        if len(self.short_term) > 10:
            self.short_term.pop(0)

    def remember(self, key, value):
        self.long_term[key] = value

    def recall(self, key):
        return self.long_term.get(key)