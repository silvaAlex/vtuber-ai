import importlib

from utils.applogger import AppLogger

class SkillManager:
    def __init__(self, logger: AppLogger):
        self.logger = logger or AppLogger(name="SkillManager")
        self.skills = {}
    
    def load_skill(self, skill_name):
        try:
            module = importlib.import_module(f"skills.{skill_name}")
            skill_class = getattr(module, "Skill")
            self.skills[skill_name] = skill_class(self.logger)
            self.logger.log("info", "SkillManager", f"Skill '{skill_name}' carregada com sucesso")
        except Exception as e:
            self.logger.log("error", "SkillManager", f"Erro ao carregar skill {skill_name}: {e}")

    def execute(self, skill_name, *args, **kwargs):
        if skill_name in self.skills:
            return self.skills[skill_name].run(*args, **kwargs)
        else:
            self.logger.log("warning", "SkillManager", f"Skill '{skill_name} não encontrada.")
