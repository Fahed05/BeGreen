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

        # Bouton d'analyse - Taille réduite
        analysis_button = tk.Button(main_content, text="🔍 ANALYSER LES FICHIERS",
                                    command=self._analyze_files,
                                    font=button_font,
                                    bg='#4CAF50', fg='white', pady=10, padx=20,
                                    relief=tk.RAISED, borderwidth=2)
        analysis_button.pack(pady=15)

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
        score_frame.pack(pady=(0, 20))  # Réduire l'espace en bas

        score = self.file_analyzer.calculate_green_score()
        color = self.file_analyzer.get_score_color(score)

        # Canvas pour le cercle - avec la même couleur de fond
        canvas = tk.Canvas(score_frame, width=250, height=250, highlightthickness=0, bg=bg_color)  # Taille réduite
        canvas.pack()

        # Cercle extérieur coloré
        canvas.create_oval(25, 25, 225, 225, fill=color, outline=color, width=4)  # Ajusté

        # Cercle intérieur
        canvas.create_oval(45, 45, 205, 205, fill=bg_color, outline=bg_color)  # Ajusté

        # Texte du score
        score_font = tkfont.Font(family=font_family, size=42, weight="bold")  # Taille réduite
        label_font = tkfont.Font(family=font_family, size=16)  # Taille réduite

        canvas.create_text(125, 100, text=f"{score}%", font=score_font, fill=color)  # Position ajustée
        canvas.create_text(125, 150, text="Score Green IT", font=label_font, fill=text_color)  # Position ajustée

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

        # Déterminer les couleurs selon le thème
        bg_color = "#1C1C1C" if self.current_theme == "sombre" else "#FFFFFF"
        fg_color = "#E0E0E0" if self.current_theme == "sombre" else "#000000"

        info_frame = tk.LabelFrame(parent, text="📊 Informations",
                                   font=section_font, padx=15, pady=15,
                                   bg=bg_color, fg=fg_color)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        info_frame.configure(height=300)
        info_frame.pack_propagate(False)

        # Créer un canvas et une scrollbar avec la bonne couleur de fond
        canvas = tk.Canvas(info_frame, bg=bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(info_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=bg_color)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        if not self.analyzed:
            tk.Label(scrollable_frame,
                     text="Aucune donnée disponible.\nFaites une analyse pour voir les statistiques.",
                     font=text_font, fg='#888888', bg=bg_color, justify=tk.CENTER).pack(pady=30)
        else:
            data = self.file_analyzer.get_analysis_data()

            # Statistiques avec des emojis et couleurs de thème
            tk.Label(scrollable_frame,
                     text=f"📁 Fichiers analysés: {data['total_files']}",
                     font=text_font, bg=bg_color, fg=fg_color).pack(anchor='w', pady=5)

            size_gb = data['total_size'] / (1024 ** 3) if data['total_size'] > 0 else 0
            tk.Label(scrollable_frame,
                     text=f"💾 Taille totale: {size_gb:.2f} GB",
                     font=text_font, bg=bg_color, fg=fg_color).pack(anchor='w', pady=5)

            duplicates_text = f"🔄 Doublons détectés: {len(data['duplicates'])}"
            duplicates_color = '#FF6B6B' if data['duplicates'] else '#4CAF50'  # Rouge ou vert adapté
            tk.Label(scrollable_frame,
                     text=duplicates_text,
                     font=text_font, fg=duplicates_color, bg=bg_color).pack(anchor='w', pady=5)

            # Points positifs
            tk.Label(scrollable_frame,
                     text="✅ Points positifs:",
                     font=text_font, fg='#4CAF50', bg=bg_color).pack(anchor='w', pady=(15, 5))

            if not data['duplicates']:
                tk.Label(scrollable_frame,
                         text="• Aucun doublon détecté 👍",
                         font=small_font, fg='#4CAF50', bg=bg_color).pack(anchor='w', padx=20)

            if data['total_files'] < 1000:
                tk.Label(scrollable_frame,
                         text="• Nombre de fichiers raisonnable 👌",
                         font=small_font, fg='#4CAF50', bg=bg_color).pack(anchor='w', padx=20)

            # Points à améliorer
            tk.Label(scrollable_frame,
                     text="❌ Points à améliorer:",
                     font=text_font, fg='#FF6B6B', bg=bg_color).pack(anchor='w', pady=(15, 5))

            if data['duplicates']:
                tk.Label(scrollable_frame,
                         text=f"• {len(data['duplicates'])} doublons à supprimer ⚠️",
                         font=small_font, fg='#FF6B6B', bg=bg_color).pack(anchor='w', padx=20)

            if size_gb > 10:
                tk.Label(scrollable_frame,
                         text="• Stockage important à optimiser 🗂️",
                         font=small_font, fg='#FF6B6B', bg=bg_color).pack(anchor='w', padx=20)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _create_advice_section(self, parent, font_family):
        """Crée la section conseils"""
        section_font = tkfont.Font(family=font_family, size=14, weight="bold")
        text_font = tkfont.Font(family=font_family, size=12)
        button_font = tkfont.Font(family=font_family, size=12, weight="bold")

        # Déterminer les couleurs selon le thème
        bg_color = "#1C1C1C" if self.current_theme == "sombre" else "#FFFFFF"
        fg_color = "#E0E0E0" if self.current_theme == "sombre" else "#000000"

        advice_frame = tk.LabelFrame(parent, text="💡 Conseils",
                                     font=section_font, padx=15, pady=15,
                                     bg=bg_color, fg=fg_color)
        advice_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        advice_frame.configure(height=300)
        advice_frame.pack_propagate(False)

        data = self.file_analyzer.get_analysis_data()

        if not data['duplicates']:
            tk.Label(advice_frame,
                     text="🎉 Parfait !\nAucun doublon détecté",
                     font=text_font, fg='green', bg=bg_color,
                     justify=tk.CENTER).pack(pady=30)
        else:
            tk.Label(advice_frame,
                     text=f"⚠️ {len(data['duplicates'])} doublons détectés\n"
                          f"Libérez de l'espace en les supprimant",
                     font=text_font, bg=bg_color, fg=fg_color,
                     justify=tk.CENTER).pack(pady=15)

            tk.Button(advice_frame,
                      text="🗑️ Supprimer les doublons",
                      command=self._remove_duplicates,
                      font=button_font,
                      bg='#f44336', fg='white',
                      pady=8, padx=15,
                      relief=tk.RAISED,
                      borderwidth=2).pack(pady=15)

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
