import importlib
import pkgutil
import traceback
from utils.applogger import AppLogger
import skills 

class SkillManager:
    def __init__(self, logger: AppLogger):
        self.logger = logger or AppLogger(name="SkillManager")
        self.skills = {}
        self._discover_skills()
    
    def _discover_skills(self):
        for _, module_name, _ in pkgutil.iter_modules(skills.__path__):
            self.load_skill(module_name)

    def load_skill(self, skill_name):
        try:
            module = importlib.import_module(f"skills.{skill_name}")
            skill_class = getattr(module, "Skill", None)

            if not skill_class:
                self.logger.log("warning", "SkillManager", f"Skill '{skill_name}' não tem classe Skill.")
                return

            skill_instance = skill_class(self.logger)

            # Metadados opcionais
            name = getattr(skill_instance, "name", skill_name)
            aliases = getattr(skill_instance, "aliases", [])
            
            # Registra por nome e por alias
            self.skills[name] = skill_instance
            for alias in aliases:
                self.skills[alias] = skill_instance

            self.logger.log("info", "SkillManager", f"Skill '{name}' carregada com sucesso.")
        except Exception as e:
            self.logger.log("error", "SkillManager", f"Erro ao carregar skill '{skill_name}': {e}")
            self.logger.log("debug", "SkillManager", traceback.format_exc())

    def execute(self, skill_name, *args, **kwargs):
        try:
            skill = self.skills.get(skill_name)
            if not skill:
                self.logger.log("warning", "SkillManager", f"Skill '{skill_name}' não encontrada.")
                return f"Desculpe, não conheço a habilidade '{skill_name}'."

            if not hasattr(skill, "run"):
                self.logger.log("error", "SkillManager", f"Skill '{skill_name}' não possui método run().")
                return f"A habilidade '{skill_name}' está mal configurada."

            self.logger.log("info", "SkillManager", f"Executando skill '{skill_name}'...")
            return skill.run(*args, **kwargs)

        except Exception as e:
            self.logger.log("error", "SkillManager", f"Erro ao executar skill '{skill_name}': {e}")
            self.logger.log("debug", "SkillManager", traceback.format_exc())
            return f"A habilidade '{skill_name}' teve um pequeno colapso mental."

    def list_skills(self):
        """Retorna uma lista formatada de todas as skills registradas."""
        listed = []
        for name, skill in self.skills.items():
            listed.append({
                "name": name,
                "description": getattr(skill, "description", "Sem descrição."),
                "aliases": getattr(skill, "aliases", [])
            })
        return listed

    def has_skill(self, name: str) -> bool:
        """Verifica se uma skill existe."""
        return name in self.skills