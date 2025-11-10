import os
import uuid
import tempfile
import threading
from dotenv import load_dotenv
from murf import Murf
from playsound import playsound
from utils.applogger import AppLogger


class Skill:
    name = "speak_murf"
    aliases = ["falar", "voz"]

    def __init__(self, logger: AppLogger):
        self.logger = logger or AppLogger(name="SpeakMurf")

        load_dotenv()

        self.api_key = os.getenv("MURF_API_KEY")
        self.voice_id = os.getenv("MURF_VOICE_ID", "en_female_emma")
        self.output_dir = tempfile.gettempdir()

        if not self.api_key:
            self.logger.log("error", "SpeakMurf", "Chave MURF_API_KEY não encontrada no .env")
            raise ValueError("MURF_API_KEY ausente.")

        self.client = Murf(api_key=self.api_key)

    def run(self, text: str):
        """Executa a fala em thread separada, sem travar a aplicação principal."""
        threading.Thread(target=self._speak, args=(text,), daemon=True).start()

    def _speak(self, text: str):
        """Gera fala com Murf e reproduz o áudio."""
        if not text or not text.strip():
            self.logger.log("warning", "SpeakMurf", "Texto vazio recebido, ignorando.")
            return

        # Cria nome temporário para o arquivo de áudio
        temp_file = os.path.join(self.output_dir, f"murf_{uuid.uuid4().hex}.wav")

        try:
            self.logger.log("info", "SpeakMurf", f"Gerando fala para: '{text}'")

            # Geração do áudio em stream
            audio_stream = self.client.text_to_speech.stream(
                text=text,
                voice_id=self.voice_id
            )

            with open(temp_file, 'ab') as f:
                for chunk in audio_stream:
                    f.write(chunk)

            self.logger.log("info", "SpeakMurf", f"Áudio gerado: {temp_file}")

            # Reprodução do áudio
            playsound(temp_file)
            self.logger.log("info", "SpeakMurf", "Reprodução concluída.")

        except Exception as e:
            self.logger.log("error", "SpeakMurf", f"Erro ao gerar/reproduzir fala: {e}")

        finally:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    self.logger.log("debug", "SpeakMurf", f"Áudio temporário removido: {temp_file}")
            except Exception as cleanup_error:
                self.logger.log("warning", "SpeakMurf", f"Falha ao limpar arquivo temporário: {cleanup_error}")