# BeGreen! 🌱

**LA solution pour réduire la pollution numérique en entreprise**

BeGreen! analyse la consommation des fichiers sur les ordinateurs et propose des solutions pour améliorer l'empreinte écologique numérique.

## 🚀 Fonctionnalités

- **Score Green IT** : Calcul automatique basé sur l'analyse des fichiers
- **Détection de doublons** : Identification et suppression des fichiers dupliqués
- **Conseils personnalisés** : Recommandations pour optimiser le stockage
- **Interface intuitive** : Design simple pour tous les employés
- **Thèmes** : Mode clair et sombre

## 📦 Installation

### Prérequis
- Python 3.7+
- Pillow (bibliothèque pour le traitement des images)
- Tkinter (inclus avec Python)

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Lancement
```bash
# Cloner ou télécharger le projet
cd BeGreen

# Lancer l'application
python main.py
```

## 📁 Structure du projet

```
BeGreen/
├── main.py              # Point d'entrée
├── config.py            # Gestion configuration
├── file_analyzer.py     # Analyse des fichiers
├── ui/
│   ├── __init__.py
│   ├── dashboard.py     # Tableau de bord
│   ├── main_window.py   # Interface principale
│   └── settings.py      # Paramètres
├── data/
│   ├── sub_BeGreen.png  # Logo
└── README.md
```

## 🎯 Utilisation

1. **Premier lancement** : Saisissez votre nom
2. **Analyse** : Cliquez sur "Analyser les fichiers" et sélectionnez un dossier
3. **Score** : Consultez votre score Green IT (0-100%)
4. **Action** : Supprimez les doublons détectés pour améliorer votre score
5. **Paramètres** : Personnalisez le thème et vos informations

## 📊 Calcul du Score

Le score Green IT est calculé selon :
- **Base** : 100 points
- **Pénalités** : -2 points par doublon, -5 points par GB de stockage
- **Bonus** : +5 points si moins de 1000 fichiers

## 🛠️ Développement

Développé en Python avec Pillow et Tkinter pour Windows 11, architecture modulaire pour faciliter la maintenance.