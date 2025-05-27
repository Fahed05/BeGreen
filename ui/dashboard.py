"""
Page tableau de bord de BeGreen!
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.font as tkfont


class DashboardPage:
    def __init__(self, parent, file_analyzer):
        self.parent = parent
        self.file_analyzer = file_analyzer
        self.analyzed = False  # Nouvel attribut pour suivre si une analyse a été effectuée
        self.current_theme = "clair"  # Thème par défaut

    def set_theme(self, theme):
        """Définit le thème actuel"""
        self.current_theme = theme

    def show(self):
        """Affiche la page tableau de bord"""
        # Nettoyer les widgets existants
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Déterminer les couleurs en fonction du thème
        if self.current_theme == "sombre":
            bg_color = "#1C1C1C"
            text_color = "#E0E0E0"
        else:
            bg_color = "#FFFFFF"
            text_color = "#333333"

        # Vérifier les polices disponibles et choisir la meilleure
        available_fonts = tkfont.families()
        modern_fonts = ['Segoe UI', 'Verdana', 'Tahoma', 'Calibri', 'Arial']

        font_family = 'Arial'  # Police par défaut
        for font in modern_fonts:
            if font in available_fonts:
                font_family = font
                break

        # Créer des polices personnalisées avec la police choisie
        title_font = tkfont.Font(family=font_family, size=24, weight="bold")
        subtitle_font = tkfont.Font(family=font_family, size=18, weight="bold")
        button_font = tkfont.Font(family=font_family, size=16, weight="bold")
        text_font = tkfont.Font(family=font_family, size=12)
        small_text_font = tkfont.Font(family=font_family, size=10)

        # Configurer le fond du parent
        self.parent.configure(bg=bg_color)

        # Titre
        title_label = tk.Label(self.parent, text="📊 Tableau de bord",
                               font=title_font, bg=bg_color, fg=text_color)
        title_label.pack(pady=20)

        # Frame principal avec couleur de fond explicite
        main_content = tk.Frame(self.parent, bg=bg_color)
        main_content.pack(fill=tk.BOTH, expand=True, padx=20)

        # Bouton d'analyse - Plus grand et plus attractif
        analysis_button = tk.Button(main_content, text="🔍 ANALYSER LES FICHIERS",
                                    command=self._analyze_files,
                                    font=button_font,
                                    bg='#4CAF50', fg='white', pady=15, padx=30,
                                    relief=tk.RAISED, borderwidth=3)
        analysis_button.pack(pady=25)

        # Score (centré en haut)
        if self.analyzed:
            self._create_score_section(main_content, font_family)
        else:
            # Message indiquant qu'aucune analyse n'a été effectuée
            tk.Label(main_content, text="🔄 Aucune analyse effectuée",
                     font=subtitle_font, fg='#888888', bg=bg_color).pack(pady=40)

        # Sections informations et conseils
        if self.analyzed:
            self._create_info_sections(main_content, font_family)
        else:
            # Message explicatif
            instruction_frame = tk.Frame(main_content, bg=bg_color)
            instruction_frame.pack(fill=tk.BOTH, expand=True, pady=20)

            tk.Label(instruction_frame,
                     text="⬆️ Cliquez sur le bouton 'ANALYSER LES FICHIERS' pour démarrer l'analyse",
                     font=text_font, fg='#555555', bg=bg_color).pack(pady=15)

            tk.Label(instruction_frame,
                     text="✨ L'application analysera vos fichiers et affichera ici les résultats",
                     font=text_font, fg='#555555', bg=bg_color).pack(pady=10)

    def _create_score_section(self, parent, font_family):
        """Crée la section score avec cercle coloré"""
        # Déterminer les couleurs en fonction du thème
        if self.current_theme == "sombre":
            bg_color = "#1C1C1C"
            text_color = "#E0E0E0"
        else:
            bg_color = "#FFFFFF"
            text_color = "#333333"
        
        # Créer un frame avec la même couleur que le parent
        score_frame = tk.Frame(parent, bg=bg_color)
        score_frame.pack(pady=30)

        score = self.file_analyzer.calculate_green_score()
        color = self.file_analyzer.get_score_color(score)

        # Canvas pour le cercle - avec la même couleur de fond
        canvas = tk.Canvas(score_frame, width=300, height=300, highlightthickness=0, bg=bg_color)
        canvas.pack()

        # Cercle extérieur coloré
        canvas.create_oval(30, 30, 270, 270, fill=color, outline=color, width=4)

        # Cercle intérieur (même couleur que le fond)
        # Légèrement plus petit pour créer un anneau coloré
        canvas.create_oval(55, 55, 245, 245, fill=bg_color, outline=bg_color)

        # Texte du score - avec la police choisie
        score_font = tkfont.Font(family=font_family, size=48, weight="bold")
        label_font = tkfont.Font(family=font_family, size=18)

        canvas.create_text(150, 120, text=f"{score}%", font=score_font, fill=color)
        canvas.create_text(150, 180, text="Score Green IT", font=label_font, fill=text_color)

    def _create_info_sections(self, parent, font_family):
        """Crée les sections informations et conseils"""
        # Déterminer les couleurs en fonction du thème
        if self.current_theme == "sombre":
            bg_color = "#1C1C1C"
        else:
            bg_color = "#FFFFFF"
        
        bottom_frame = tk.Frame(parent, bg=bg_color)
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Section Informations (gauche)
        self._create_info_section(bottom_frame, font_family)

        # Section Conseils (droite)
        self._create_advice_section(bottom_frame, font_family)

    def _create_empty_advice_section(self, parent, font_family):
        """Crée une section de conseils vide avant analyse"""
        section_font = tkfont.Font(family=font_family, size=14, weight="bold")
        text_font = tkfont.Font(family=font_family, size=12)

        advice_frame = tk.LabelFrame(parent, text="💡 Conseils",
                                     font=section_font, padx=15, pady=15)
        advice_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        tk.Label(advice_frame,
                 text="Cliquez sur 'Analyser les fichiers'\npour obtenir des conseils personnalisés",
                 font=text_font, justify=tk.CENTER).pack(pady=30)

    def _create_info_section(self, parent, font_family):
        """Crée la section informations"""
        section_font = tkfont.Font(family=font_family, size=14, weight="bold")
        text_font = tkfont.Font(family=font_family, size=12)
        small_font = tkfont.Font(family=font_family, size=11)

        info_frame = tk.LabelFrame(parent, text="📊 Informations",
                                   font=section_font, padx=15, pady=15)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        if not self.analyzed:
            tk.Label(info_frame,
                     text="Aucune donnée disponible.\nFaites une analyse pour voir les statistiques.",
                     font=text_font, fg='#888888', justify=tk.CENTER).pack(pady=30)
            return

        data = self.file_analyzer.get_analysis_data()

        # Statistiques avec des emojis plus grands
        tk.Label(info_frame, text=f"📁 Fichiers analysés: {data['total_files']}",
                 font=text_font).pack(anchor='w', pady=5)

        size_gb = data['total_size'] / (1024 ** 3) if data['total_size'] > 0 else 0
        tk.Label(info_frame, text=f"💾 Taille totale: {size_gb:.2f} GB",
                 font=text_font).pack(anchor='w', pady=5)

        duplicates_text = f"🔄 Doublons détectés: {len(data['duplicates'])}"
        duplicates_color = 'red' if data['duplicates'] else 'green'
        tk.Label(info_frame, text=duplicates_text,
                 font=text_font, fg=duplicates_color).pack(anchor='w', pady=5)

        # Points positifs
        tk.Label(info_frame, text="✅ Points positifs:",
                 font=text_font, fg='green').pack(anchor='w', pady=(15, 5))

        if not data['duplicates']:
            tk.Label(info_frame, text="• Aucun doublon détecté 👍",
                     font=small_font, fg='green').pack(anchor='w', padx=20)

        if data['total_files'] < 1000:
            tk.Label(info_frame, text="• Nombre de fichiers raisonnable 👌",
                     font=small_font, fg='green').pack(anchor='w', padx=20)

        # Points à améliorer
        tk.Label(info_frame, text="❌ Points à améliorer:",
                 font=text_font, fg='red').pack(anchor='w', pady=(15, 5))

        if data['duplicates']:
            tk.Label(info_frame, text=f"• {len(data['duplicates'])} doublons à supprimer ⚠️",
                     font=small_font, fg='red').pack(anchor='w', padx=20)

        if size_gb > 10:
            tk.Label(info_frame, text="• Stockage important à optimiser 🗂️",
                     font=small_font, fg='red').pack(anchor='w', padx=20)

    def _create_advice_section(self, parent, font_family):
        """Crée la section conseils"""
        section_font = tkfont.Font(family=font_family, size=14, weight="bold")
        text_font = tkfont.Font(family=font_family, size=12)
        button_font = tkfont.Font(family=font_family, size=12, weight="bold")

        advice_frame = tk.LabelFrame(parent, text="💡 Conseils",
                                     font=section_font, padx=15, pady=15)
        advice_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        data = self.file_analyzer.get_analysis_data()

        if not data['duplicates']:
            tk.Label(advice_frame, text="🎉 Parfait !\nAucun doublon détecté",
                     font=text_font, fg='green', justify=tk.CENTER).pack(pady=30)
        else:
            tk.Label(advice_frame, text=f"⚠️ {len(data['duplicates'])} doublons détectés\n"
                                        f"Libérez de l'espace en les supprimant",
                     font=text_font, justify=tk.CENTER).pack(pady=15)

            tk.Button(advice_frame, text="🗑️ Supprimer les doublons",
                      command=self._remove_duplicates,
                      font=button_font,
                      bg='#f44336', fg='white',
                      pady=8, padx=15,
                      relief=tk.RAISED, borderwidth=2).pack(pady=15)

    def _analyze_files(self):
        """Lance l'analyse des fichiers"""
        folder = filedialog.askdirectory(title="Sélectionner le dossier à analyser")
        if not folder:
            return

        success = self.file_analyzer.analyze_directory(folder)
        if success:
            self.analyzed = True  # Marquer que l'analyse a été effectuée
            data = self.file_analyzer.get_analysis_data()
            messagebox.showinfo("Analyse terminée",
                                f"✅ Analyse terminée!\n\n"
                                f"📁 Fichiers analysés: {data['total_files']}\n"
                                f"🔄 Doublons trouvés: {len(data['duplicates'])}")
            # Rafraîchir l'affichage
            self.show()
        else:
            messagebox.showerror("Erreur", "❌ Erreur lors de l'analyse des fichiers!")

    def _remove_duplicates(self):
        """Supprime les fichiers en double"""
        data = self.file_analyzer.get_analysis_data()
        if not data['duplicates']:
            messagebox.showinfo("Info", "✅ Aucun doublon à supprimer!")
            return

        result = messagebox.askyesno("Confirmation",
                                     f"⚠️ Voulez-vous supprimer {len(data['duplicates'])} fichiers en double?")
        if result:
            removed_count = self.file_analyzer.remove_duplicates()
            messagebox.showinfo("Terminé", f"🎉 {removed_count} fichiers supprimés avec succès!")
            self.show()  # Rafraîchir l'affichage