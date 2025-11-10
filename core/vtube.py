from core.vtube_controller import VTubeController
from utils.applogger import AppLogger

class VTSAvatar:
    def __init__(self, logger=AppLogger, controller=VTubeController):
        self.vts = controller.vts
        self.logger = logger or AppLogger(name="VTSAvatar")

    async def trigger_hotkey(self, name: str):
        try:
            await self.vts.request(self.vts.vts_request.requestTriggerHotKey(name))
            self.logger.log("info", "VTSAvatar", f"Hotkey '{name}' acionada com sucesso!")
        except Exception as e:
            self.logger.log("error", "VTSAvatar", f"Erro ao acionar hotkey '{name}': {e}")