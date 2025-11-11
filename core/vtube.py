import asyncio
import time
from core.vtube_controller import VTubeController
from utils.applogger import AppLogger

class VTSAvatar:
    def __init__(self, logger=AppLogger, controller=VTubeController):
        self.vts = controller.vts
        self.logger = logger or AppLogger(name="VTSAvatar")
        self._lock = asyncio.Lock()
        self._last_log = 0
        self._log_interval = 2.0  # log a cada 2 segundos, por exemplo

    async def trigger_hotkey(self, name: str):
        try:
            await self.vts.request(self.vts.vts_request.requestTriggerHotKey(name))
            self.logger.log("info", "VTSAvatar", f"Hotkey '{name}' acionada com sucesso!")
        except Exception as e:
            self.logger.log("error", "VTSAvatar", f"Erro ao acionar hotkey '{name}': {e}")
    
    async def set_parameter_value(self, name: str, value: float):
        async with self._lock:
            try:
                request = self.vts.vts_request.requestSetParameterValue(name, value)
                await self.vts.request(request)
                new_parameter_value = await self.vts.request(
                    self.vts.vts_request.requestParameterValue(name)
                )
                now = time.time()
                if now - self._last_log >= self._log_interval:
                    self._last_log = now
                    self.logger.log("debug", "VTSAvatar", f"{new_parameter_value['data']}")
            except Exception as e:
                self.logger.log("error", "VTSAvatar", f"Erro ao atualizar parametro '{name}': {e}")