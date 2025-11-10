import os
import pyvts
from utils.applogger import AppLogger

class VTubeController:
    def __init__(self, logger: AppLogger):
        self.logger = logger or AppLogger(name="VTubeController")

        self.plugin_info = {
            "plugin_name": "AIWaifu",
            "developer": "AlexJR",
            "authentication_token_path": "./token.txt",
        }

        self.vts = pyvts.vts(
            plugin_info=self.plugin_info,
            vts_api_info= {
                "version": "1.0",
                "name" : "VTubeStudioPublicAPI",
                "port": int(os.environ.get("VTUBE_STUDIO_API_PORT", 8001))
            }
        )
      
    async def connect(self):
        try:
            await self.vts.connect()
            await self.vts.request_authenticate_token()
            await self.vts.request_authenticate()
            self.logger.log("info", "VTube Studio", "Conectado ao VTube Studio")
        except Exception as e:
            self.logger.log("error", "VTube Studio", "erro ao Conectar ao VTube Studio - {e}")
    

    async def close(self):
       await self.vts.close()
       self.logger.log("info", "VTube Studio", "Conexão ao VTube Studio encerrada")
    