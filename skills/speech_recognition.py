import tempfile
import wave
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from utils.applogger import AppLogger
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

class Skill:
    name = "asr"
    aliases = ["fala", "speech", "voz"]
    description = "Capta a fala do usuário e converte em texto."

    def __init__(self, logger: AppLogger):
        self.logger = logger or AppLogger(name="ASRSkill")
        # carrega o modelo Whisper uma vez só
        self.model = WhisperModel("base", device="cpu", compute_type="int8")
        self.console = Console()


    def _record_audio(self, duration=5, sample_rate=16000):
        """Grava um trecho de áudio e mostra indicador visual."""
        self.logger.log("info", "ASR", f"Gravando áudio por {duration}s...")

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Gravando... Fale agora![/bold cyan]"),
            transient=True,  # some quando terminar
            console=self.console
        ) as progress:
            task = progress.add_task("recording", total=None)
            audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
            sd.wait()
            progress.remove_task(task)

        self.console.print("[green]✔ Gravação concluída![/green]")
        self.logger.log("info", "ASR", "Gravação concluída.")

        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with wave.open(temp_wav.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio.tobytes())

        return temp_wav.name

    def _transcribe(self, file_path):
        """Transcreve o áudio com Whisper."""
        segments, info = self.model.transcribe(file_path, language="pt", beam_size=5)
        text = " ".join([seg.text.strip() for seg in segments])
        self.logger.log("info", "ASR", f"Texto reconhecido: {text}")
        return text.strip()

    def run(self, data=None):
        """
        Captura a voz do usuário e devolve o texto transcrito.
        O parâmetro `data` pode conter configurações como duração.
        """

        print("Audio Escuta")
        try:
            duration = 5
            if isinstance(data, dict) and "duration" in data:
                duration = data["duration"]

            audio_path = self._record_audio(duration=duration)
            recognized_text = self._transcribe(audio_path)

            return recognized_text

        except Exception as e:
            self.logger.log("error", "ASRSkill", f"Erro: {e}")
            return "Erro ao processar áudio."