"""
Fenêtre principale et interface utilisateur de BeGreen!
"""

import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
import webbrowser
from PIL import Image, ImageTk
from config import ConfigManager
from file_analyzer import FileAnalyzer
from ui.dashboard import DashboardPage
from ui.settings import SettingsPage


class BeGreenApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BeGreen!")
        self.root.geometry("1400x800")
        self.root.resizable(True, True)

        # Centrer la fenêtre sur l'écran
        self._center_window()

        # Essayer de charger des polices modernes
        self._setup_fonts()

        # Gestionnaires
        self.config_manager = ConfigManager()
        self.file_analyzer = FileAnalyzer()

        # Variables
        self.username = tk.StringVar()
        self.theme = tk.StringVar(value="clair")

        # Chargement configuration
        self._load_config()

        # Vérifier première utilisation
        if not self.username.get():
            self._show_welcome_dialog()

        # Interface
        self._setup_ui()
        self._apply_theme()

    def _setup_fonts(self):
        """Configure les polices disponibles"""
        # Liste des polices modernes à essayer
        modern_fonts = ['Segoe UI', 'Verdana', 'Tahoma', 'Calibri', 'Arial']

        # Vérifier les polices disponibles
        available_fonts = tkfont.families()

        # Trouver la première police moderne disponible
        self.font_family = 'Arial'  # Police par défaut
        for font in modern_fonts:
            if font in available_fonts:
                self.font_family = font
                break

    def _load_config(self):
        """Charge la configuration"""
        config = self.config_manager.load_config()
        self.username.set(config.get('username', ''))
        self.theme.set(config.get('theme', 'clair'))

    def _save_config(self):
        """Sauvegarde la configuration"""
        config = {
            'username': self.username.get(),
            'theme': self.theme.get()
        }
        return self.config_manager.save_config(config)

    def _show_welcome_dialog(self):
        """Dialogue de bienvenue pour saisir le nom"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Bienvenue dans BeGreen! 🌱")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 250, self.root.winfo_rooty() + 200))

        # Appliquer le style
        title_font = tkfont.Font(family=self.font_family, size=18, weight="bold")
        text_font = tkfont.Font(family=self.font_family, size=14)
        button_font = tkfont.Font(family=self.font_family, size=14, weight="bold")

        tk.Label(dialog, text="🌱 Bienvenue dans BeGreen!", font=title_font).pack(pady=25)
        tk.Label(dialog, text="Comment souhaitez-vous être appelé(e) ?", font=text_font).pack(pady=15)

        name_entry = tk.Entry(dialog, font=text_font, width=30)
        name_entry.pack(pady=15)
        name_entry.focus()

        def on_submit():
            name = name_entry.get().strip()
            if name:
                self.username.set(name)
                self._save_config()
                dialog.destroy()
            else:
                messagebox.showerror("Erreur", "⚠️ Veuillez saisir votre nom!")

        name_entry.bind('<Return>', lambda e: on_submit())

        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="✅ Valider",
                 command=on_submit,
                 font=button_font,
                 bg="#4CAF50", fg="white",
                 padx=20, pady=8).pack()

        dialog.wait_window()

    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self._setup_sidebar()

        # Zone de contenu
        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pages
        self.dashboard_page = DashboardPage(self.content_frame, self.file_analyzer)
        self.settings_page = SettingsPage(self.content_frame, self.username, self.theme, self._save_config,
                                          self._apply_theme, self._update_sidebar)

        # Afficher tableau de bord par défaut
        self.show_dashboard()

    def _setup_sidebar(self):
        """Configure la barre latérale"""
        if hasattr(self, 'sidebar'):
            self.sidebar.destroy()

        # Créer des polices stylées
        logo_font = tkfont.Font(family=self.font_family, size=28, weight="bold")
        app_name_font = tkfont.Font(family=self.font_family, size=20, weight="bold")
        greeting_font = tkfont.Font(family=self.font_family, size=14)
        user_font = tkfont.Font(family=self.font_family, size=16, weight="bold")
        button_font = tkfont.Font(family=self.font_family, size=13)

        self.sidebar = tk.Frame(self.main_frame, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.sidebar.pack_propagate(False)

        # Logo et nom
        logo_frame = tk.Frame(self.sidebar)
        logo_frame.pack(fill=tk.X, pady=15)
        tk.Label(logo_frame, text="🌱", font=logo_font).pack()
        tk.Label(logo_frame, text="BeGreen!", font=app_name_font).pack()

        # Salutation
        user_frame = tk.Frame(self.sidebar)
        user_frame.pack(fill=tk.X, pady=15)
        tk.Label(user_frame, text="Bonjour", font=greeting_font).pack()
        tk.Label(user_frame, text=f"{self.username.get()} !", font=user_font).pack()

        # Séparateur
        tk.Frame(self.sidebar, height=2, bg='gray').pack(fill=tk.X, pady=15)

        # Navigation
        nav_frame = tk.Frame(self.sidebar)
        nav_frame.pack(fill=tk.X, pady=5)

        self.nav_buttons = []

        # Boutons
        btn_home = tk.Button(nav_frame, text="🏠 Tableau de bord",
                             command=self.show_dashboard, font=button_font,
                             relief=tk.FLAT, anchor='w', padx=20, pady=12)
        btn_home.pack(fill=tk.X, pady=3)
        self.nav_buttons.append(btn_home)

        btn_settings = tk.Button(nav_frame, text="⚙️ Paramètres",
                                 command=self.show_settings, font=button_font,
                                 relief=tk.FLAT, anchor='w', padx=20, pady=12)
        btn_settings.pack(fill=tk.X, pady=3)
        self.nav_buttons.append(btn_settings)

        btn_help = tk.Button(nav_frame, text="❓ Aide",
                             command=self._show_help, font=button_font,
                             relief=tk.FLAT, anchor='w', padx=20, pady=12)
        btn_help.pack(fill=tk.X, pady=3)
        self.nav_buttons.append(btn_help)

        # Charger et redimensionner l'image
        image = Image.open('data/sub_BeGreen.png')  # Chemin vers l'image
        # Charger et redimensionner l'image
        resized_image = image.resize((200, 200), Image.Resampling.LANCZOS)  # Redimensionner à 100x100 pixels
        self.logo_image = ImageTk.PhotoImage(resized_image)

        # Créer un frame pour l'image en bas de la sidebar
        image_frame = tk.Frame(self.sidebar)
        image_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Ajouter l'image redimensionnée dans ce frame
        tk.Label(image_frame, image=self.logo_image).pack(pady=10)

    def _update_sidebar(self):
        """Met à jour la sidebar"""
        self._setup_sidebar()
        self._apply_theme()

    def show_dashboard(self):
        """Affiche le tableau de bord"""
        self._clear_content()
        # Passer le thème actuel au tableau de bord
        self.dashboard_page.set_theme(self.theme.get())
        self.dashboard_page.show()

    def show_settings(self):
        """Affiche les paramètres"""
        self._clear_content()
        self.settings_page.show()

    def _show_help(self):
        """Ouvre la page d'aide"""
        webbrowser.open("https://www.greenit.fr/")
        messagebox.showinfo("Aide", "🌐 La page d'aide s'ouvre dans votre navigateur!")

    def _apply_theme(self):
        """Applique le thème sélectionné à tous les éléments"""
        if self.theme.get() == "sombre":
            # Couleurs du thème sombre
            bg_color = "#1C1C1C"
            fg_color = "#E0E0E0"  # Texte plus lumineux pour meilleure lisibilité
            sidebar_color = "#2A2A2A"
            btn_bg = "#333333"
            btn_active = "#444444"
            entry_bg = "#2A2A2A"
            label_bg = "#1C1C1C"
            frame_bg = "#2A2A2A"
            radio_bg = "#1C1C1C"  # Arrière-plan des Radiobutton
            radio_fg = "#E0E0E0"  # Texte des Radiobutton
            canvas_bg = "#1C1C1C"  # Couleur de fond du canvas
        else:
            # Couleurs du thème clair
            bg_color = "#FFFFFF"
            fg_color = "#000000"
            sidebar_color = "#F5F5F5"
            btn_bg = "#E0E0E0"
            btn_active = "#D6D6D6"
            entry_bg = "#FFFFFF"
            label_bg = "#FFFFFF"
            frame_bg = "#F5F5F5"
            radio_bg = "#FFFFFF"
            radio_fg = "#000000"
            canvas_bg = "#FFFFFF"  # Couleur de fond du canvas

        # Configuration globale des styles
        self.root.configure(bg=bg_color)
        self.main_frame.configure(bg=bg_color)
        self.content_frame.configure(bg=bg_color)

        if hasattr(self, 'sidebar'):
            self.sidebar.configure(bg=sidebar_color)

        if hasattr(self, 'nav_buttons'):
            for btn in self.nav_buttons:
                btn.configure(
                    bg=btn_bg,
                    fg=fg_color,
                    activebackground=btn_active,
                    activeforeground=fg_color
                )

        def apply_theme_to_widgets(parent):
            for widget in parent.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=label_bg, fg=fg_color)
                elif isinstance(widget, tk.Button):
                    # Ne pas modifier les boutons d'action qui ont des couleurs spécifiques
                    if widget.cget('bg') not in ['#4CAF50', '#f44336', '#2196F3']:
                        widget.configure(
                            bg=btn_bg,
                            fg=fg_color,
                            activebackground=btn_active,
                            activeforeground=fg_color
                        )
                elif isinstance(widget, tk.Entry):
                    widget.configure(
                        bg=entry_bg,
                        fg=fg_color,
                        insertbackground=fg_color
                    )
                elif isinstance(widget, (tk.Frame, tk.LabelFrame)):
                    widget.configure(bg=frame_bg)
                    if isinstance(widget, tk.LabelFrame):
                        widget.configure(fg=fg_color)
                elif isinstance(widget, tk.Canvas):
                    widget.configure(bg=canvas_bg)
                elif isinstance(widget, tk.Radiobutton):
                    widget.configure(
                        bg=radio_bg,
                        fg=radio_fg,
                        selectcolor=btn_active
                    )
                apply_theme_to_widgets(widget)

        apply_theme_to_widgets(self.root)

        # Mettre à jour le thème dans le tableau de bord
        self.dashboard_page.set_theme(self.theme.get())

    def _clear_content(self):
        """Efface le contenu de la zone principale"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def run(self):
        """Lance l'application"""
        self.root.mainloop()

    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        # Obtenir les dimensions de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Dimensions de la fenêtre
        window_width = 1400  # Même valeur que dans geometry()
        window_height = 800  # Même valeur que dans geometry()

        # Calculer la position pour centrer la fenêtre
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2

        # Définir la taille et la position de la fenêtre
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")