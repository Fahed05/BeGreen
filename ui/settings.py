"""
Page paramètres de BeGreen!
"""

import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox


class SettingsPage:
    def __init__(self, parent, username_var, theme_var, save_callback, apply_theme_callback, update_sidebar_callback):
        self.parent = parent
        self.username_var = username_var
        self.theme_var = theme_var
        self.save_callback = save_callback
        self.apply_theme_callback = apply_theme_callback
        self.update_sidebar_callback = update_sidebar_callback

    def show(self):
        """Affiche la page des paramètres"""
        # Nettoyer les widgets existants
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Vérifier les polices disponibles et choisir la meilleure
        available_fonts = tkfont.families()
        modern_fonts = ['Segoe UI', 'Verdana', 'Tahoma', 'Calibri', 'Arial']

        font_family = 'Arial'  # Police par défaut
        for font in modern_fonts:
            if font in available_fonts:
                font_family = font
                break

        # Créer des polices personnalisées
        title_font = tkfont.Font(family=font_family, size=24, weight="bold")
        section_font = tkfont.Font(family=font_family, size=16, weight="bold")
        text_font = tkfont.Font(family=font_family, size=14)
        button_font = tkfont.Font(family=font_family, size=14, weight="bold")

        tk.Label(self.parent, text="⚙️ Paramètres",
                 font=title_font).pack(pady=25)

        settings_frame = tk.Frame(self.parent)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)

        # Section Thème
        self._create_theme_section(settings_frame, section_font, text_font)

        # Section Utilisateur
        self._create_user_section(settings_frame, section_font, text_font)

        # Bouton de sauvegarde
        save_button = tk.Button(settings_frame, text="💾 Sauvegarder",
                                command=self._save_settings,
                                font=button_font,
                                bg='#2196F3', fg='white',
                                pady=10, padx=25,
                                relief=tk.RAISED, borderwidth=2)
        save_button.pack(pady=30)

    def _create_theme_section(self, parent, section_font, text_font):
        """Crée la section choix du thème"""
        theme_frame = tk.LabelFrame(parent, text="🎨 Apparence",
                                    font=section_font, padx=25, pady=25)
        theme_frame.pack(fill=tk.X, pady=15)

        tk.Label(theme_frame, text="Thème:", font=text_font).pack(anchor='w', pady=5)

        self.theme_selection = tk.StringVar(value=self.theme_var.get())

        theme_option_frame = tk.Frame(theme_frame)
        theme_option_frame.pack(fill=tk.X, pady=10)

        # Options de thème avec plus d'espace
        tk.Radiobutton(theme_option_frame, text="☀️ Thème clair",
                       variable=self.theme_selection,
                       value="clair", font=text_font).pack(anchor='w', padx=25, pady=5)

        tk.Radiobutton(theme_option_frame, text="🌙 Thème sombre",
                       variable=self.theme_selection,
                       value="sombre", font=text_font).pack(anchor='w', padx=25, pady=5)

    def _create_user_section(self, parent, section_font, text_font):
        """Crée la section utilisateur"""
        user_frame = tk.LabelFrame(parent, text="👤 Utilisateur",
                                   font=section_font, padx=25, pady=25)
        user_frame.pack(fill=tk.X, pady=15)

        tk.Label(user_frame, text="Nom d'utilisateur:", font=text_font).pack(anchor='w', pady=5)

        self.name_var = tk.StringVar(value=self.username_var.get())
        name_entry = tk.Entry(user_frame, textvariable=self.name_var, font=text_font, width=30)
        name_entry.pack(anchor='w', padx=25, pady=10)

    def _save_settings(self):
        """Sauvegarde les paramètres"""
        # Mettre à jour les variables
        self.theme_var.set(self.theme_selection.get())
        self.username_var.set(self.name_var.get())

        # Sauvegarder
        if self.save_callback():
            # Appliquer les changements
            self.apply_theme_callback()
            self.update_sidebar_callback()
            messagebox.showinfo("Paramètres", "✅ Paramètres sauvegardés avec succès!")
        else:
            messagebox.showerror("Erreur", "❌ Erreur lors de la sauvegarde!")