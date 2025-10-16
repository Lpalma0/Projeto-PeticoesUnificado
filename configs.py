from pathlib import Path

class Config:
    @staticmethod
    def get_paths():
        return {
            "CWD": Config.CWD,
            "PATH_MODELO_DESISTENCIAS": Config.PATH_MODELO_DESISTENCIAS
        }