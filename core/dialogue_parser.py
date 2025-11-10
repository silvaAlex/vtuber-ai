import re

def parse_dialogue(response_text: str):
    """Separa fala e ações do texto da IA."""
    actions = re.findall(r"\*(.*?)\*", response_text)
    spoken_text = re.sub(r"\*.*?\*", "", response_text).strip()
    return spoken_text, actions