"""
Analyseur de fichiers pour BeGreen!
Détection des doublons et calcul du score Green IT
"""

import os
import hashlib
from collections import defaultdict


class FileAnalyzer:
    def __init__(self):
        self.reset_analysis()

    def reset_analysis(self):
        """Réinitialise les données d'analyse"""
        self.file_analysis = {
            'total_files': 0,
            'total_size': 0,
            'duplicates': [],
            'large_files': [],
            'old_files': []
        }

    def analyze_directory(self, folder_path):
        """Analyse un dossier et détecte les doublons"""
        self.reset_analysis()
        file_hashes = defaultdict(list)

        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        if os.path.isfile(file_path):
                            size = os.path.getsize(file_path)
                            self.file_analysis['total_files'] += 1
                            self.file_analysis['total_size'] += size

                            # Détecter les gros fichiers (>100MB)
                            if size > 100 * 1024 * 1024:
                                self.file_analysis['large_files'].append((file_path, size))

                            # Calculer le hash pour détecter les doublons
                            if size < 500 * 1024 * 1024:  # Seulement pour les fichiers <500MB
                                file_hash = self._get_file_hash(file_path)
                                if file_hash:
                                    file_hashes[file_hash].append(file_path)
                    except (OSError, IOError):
                        continue

            # Identifier les doublons
            for file_hash, paths in file_hashes.items():
                if len(paths) > 1:
                    self.file_analysis['duplicates'].extend(paths[1:])

            return True

        except Exception as e:
            print(f"Erreur lors de l'analyse: {e}")
            return False

    def _get_file_hash(self, file_path):
        """Calcule le hash MD5 d'un fichier"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except (OSError, IOError):
            return None

    def calculate_green_score(self):
        """Calcule le score Green IT basé sur l'analyse des fichiers"""
        base_score = 100

        # Pénalités
        duplicate_penalty = len(self.file_analysis['duplicates']) * 2
        size_penalty = min(self.file_analysis['total_size'] / (1024 ** 3) * 5, 30)

        # Bonus pour peu de fichiers
        bonus = 5 if self.file_analysis['total_files'] < 1000 else 0

        score = max(0, min(100, base_score - duplicate_penalty - size_penalty + bonus))
        return int(score)

    def get_score_color(self, score):
        """Retourne la couleur en fonction du score"""
        if score >= 80:
            return "#4CAF50"  # Vert
        elif score >= 60:
            return "#FF9800"  # Orange
        elif score >= 40:
            return "#FF5722"  # Rouge orangé
        else:
            return "#F44336"  # Rouge

    def remove_duplicates(self):
        """Supprime les fichiers en double"""
        removed_count = 0
        for file_path in self.file_analysis['duplicates']:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    removed_count += 1
            except OSError:
                continue

        # Mettre à jour les données
        self.file_analysis['duplicates'] = []
        return removed_count

    def get_analysis_data(self):
        """Retourne les données d'analyse"""
        return self.file_analysis.copy()