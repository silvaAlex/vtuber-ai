from core.vtube_controller import VTubeController
from utils.applogger import AppLogger

class VTSAvatar:
    def __init__(self, controller=VTubeController, logger=AppLogger):
        self.vts = controller.vts
        self.logger = logger or AppLogger(name="VTSAvatar")

    async def set_expression(self, hotkey_index: int):
        try:
            response = await self.vts.request(self.vts.vts_request.requestHotKeyList())
            hotkeys = response["data"]["availableHotkeys"]
            name = hotkeys[hotkey_index]["name"]
            await self.vts.request(self.vts.vts_request.requestTriggerHotKey(name))
            self.logger.info(f"Expressão alterada: {name}")
        except Exception as e:
            self.logger.error(f"Erro ao mudar expressão: {e}")