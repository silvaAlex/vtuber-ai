import asyncio

import cv2
import numpy
import pyautogui

from core.vtube import VTSAvatar
from utils.applogger import AppLogger

class Skill:
    name = "follow_mouse"
    aliases = ["mouse_look", "vts_follow_mouse"]

    def __init__(self, logger: AppLogger = None):
        self.logger = logger or AppLogger(name="FollowMouseSkill")
        self.running = False
        self.smooth_factor = 0.15
        self.img_scale = 1.0
        self.avatar = None

    async def run(self, avatar: VTSAvatar, duration: float = None):
        self.avatar = avatar
        self.running = True

        self.logger.log("info", "FollowMouseSkill", "Iniciando acompanhamento do mouse...")

        # Captura o event loop principal antes de criar a thread
        loop = asyncio.get_running_loop()

        try:
            # Passa o loop explicitamente para a thread
            await asyncio.to_thread(self.loop_follow_mouse, loop, duration)
        except Exception as e:
            self.logger.log("error", "FollowMouseSkill", f"Erro no loop: {e}")
            self.running = False

    def capture_screenshot(self):
        """
        Tira uma screenshot da tela e salva redimensionada.
        """
        try:
            image = pyautogui.screenshot()
            image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)

            maxwidth, maxheight = int(400 * self.img_scale), int(400 * self.img_scale)
            f1 = maxwidth / image.shape[1]
            f2 = maxheight / image.shape[0]
            f = min(f1, f2)
            dim = (int(image.shape[1] * f), int(image.shape[0] * f))

            image = cv2.resize(image, dim, interpolation=cv2.INTER_LANCZOS4)
            cv2.imwrite("LiveImage.png", image)
        except Exception as e:
            self.logger.log("error", "FollowMouseSkill", f"Erro ao capturar screenshot: {e}")


    def loop_follow_mouse(self, loop, duration: float = None):
        """Loop contínuo que move o olhar do avatar suavemente seguindo o mouse."""
        import time, pyautogui, random, cv2, numpy

        screen_width, screen_height = pyautogui.size()
        look_x, look_y = 0.0, 0.0

        time.sleep(3)
        start_time = time.time()

        while self.running:
            if duration and (time.time() - start_time) >= duration:
                self.logger.log("info", "FollowMouseSkill", "Tempo limite atingido, encerrando skill.")
                self.running = False
                break

            time.sleep(0.5)
            x, y = pyautogui.position()

            target_x = (x - screen_width / 2) / (screen_width / 2)
            target_y = (y - screen_height / 2) / (screen_height / 2)
            target_x = max(min(target_x, 1.0), -1.0)
            target_y = max(min(target_y, 1.0), -1.0)

            # Suavização
            look_x += (target_x - look_x) * self.smooth_factor
            look_y += (target_y - look_y) * self.smooth_factor

            # aplica escala para o range real do VTS
            scale = 30.0  # graus máximos suportados
            look_x_scaled = look_x * scale
            look_y_scaled = look_y * scale

            # Envia pro loop original (principal)
            try:
                asyncio.run_coroutine_threadsafe(
                    self.avatar.set_parameter_value("FaceAngleX", look_x_scaled),
                    loop
                )
                asyncio.run_coroutine_threadsafe(
                    self.avatar.set_parameter_value("FaceAngleY", look_y_scaled),
                    loop
                )
            except Exception as e:
                self.logger.log("error", "FollowMouseSkill", f"Erro ao enviar parâmetros: {e}")

            if random.random() > 0.9:
                self.capture_screenshot()
