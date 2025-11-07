import os
from dotenv import load_dotenv
from murf import Murf
import requests
from utils.applogger import AppLogger
from playsound import playsound

class Skill:
    def __init__(self, logger: AppLogger):
        self.logger = logger or AppLogger(name="SpeakMurf")

        load_dotenv()

        self.api_key = os.getenv("MURF_API_KEY")
        self.voice_id = os.getenv("MURF_VOICE_ID", "en_female_emma")
        self.api_url= os.getenv("MURF_API_URL","https://api.murf.ai/v1/speech/generate")

        self.output_path = "output_audio.wav"
        
        if not self.api_key:
            self.logger.log("error", "SpeakMurf", "Chave MURF_API_KEY não encontrada")

        self.client = Murf(api_key=self.api_key)
    
    def run(self, text):
        try:
            self._speak(text)

        except Exception as e:
            self.logger.log("error", "SpeakMurf", f"Erro ao gerar fala: {e}")

    def _speak(self, text):
        self.logger.log("info", "SpeakMurf", f"Gerando fala para texto: '{text}'")

        if os.path.exists(self.output_path):
            os.remove(self.output_path)
            self.logger.log("debug", "SpeakMurf", "Áudio anterior removido")

            
        res = self.client.text_to_speech.stream(
                text=text,
                voice_id=self.voice_id
            )

        for audio_chunck in res:
            with open(self.output_path, 'ab') as f:
                f.write(audio_chunck)

            
        self.logger.log("info", "SpeakMurf", f"Áudio salvo em {self.output_path}")

            # Reproduz o áudio
        playsound(self.output_path)
        self.logger.log("info", "SpeakMurf", "Reprodução concluída")

            # Apaga após tocar
        os.remove(self.output_path)
        self.logger.log("debug", "SpeakMurf", "Áudio deletado após reprodução")