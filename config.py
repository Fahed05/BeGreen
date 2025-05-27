"""
Gestion de la configuration de l'application BeGreen!
"""

import os
import json


class ConfigManager:
    def __init__(self, config_file=None):
        # Définir le chemin par défaut dans le dossier `data`
        data_folder = os.path.join(os.getcwd(), "data")
        os.makedirs(data_folder, exist_ok=True)  # Crée le dossier `data` s'il n'existe pas
        self.config_file = config_file or os.path.join(data_folder, "begreen_config.json")
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