"""
Gestion de la configuration de l'application BeGreen!
"""

import json
import os


class ConfigManager:
    def __init__(self, config_file="begreen_config.json"):
        self.config_file = config_file
        self.default_config = {
            'username': '',
            'theme': 'clair'
        }

    def load_config(self):
        """Charge la configuration depuis le fichier"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self.default_config.copy()
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
            return self.default_config.copy()

    def save_config(self, config):
        """Sauvegarde la configuration dans le fichier"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la configuration: {e}")
            return False