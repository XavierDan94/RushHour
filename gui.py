# gui.py
import tkinter as tk
from tkinter import messagebox, ttk
import time
import os
import random
from PIL import Image, ImageTk, ImageDraw, ImageFilter


class GameGUI:
    def __init__(self, root, game):
        """
        Initialisation de l'interface graphique

        Args:
            root (tk.Tk): Fenêtre principale
            game (Game): Instance du jeu
        """
        self.root = root
        self.game = game
        self.cell_size = 80
        self.selected_vehicle = None
        self.animation_speed = 400

        # Flag pour indiquer si une animation est en cours
        self.animation_in_progress = False

        # Palette de couleurs inspirée d'Apple avec des touches modernes
        self.colors = {
            # Couleurs de base
            'background': '#F5F5F7',  # Gris très clair
            'foreground': '#1D1D1F',  # Noir presque pur
            'accent': '#0071E3',  # Bleu Apple
            'success': '#34C759',  # Vert Apple
            'warning': '#FF9500',  # Orange Apple
            'danger': '#FF3B30',  # Rouge Apple
            'button': '#E0E0E0',  # Gris clair pour les boutons
            'button_active': '#F0F0F0',  # Gris très clair pour les boutons actifs

            # Couleurs des véhicules
            'X': '#FF3B30',  # Rouge pour la voiture principale
            'car': '#34C759',  # Vert pour les voitures
            'truck': '#0071E3',  # Bleu pour les camions
        }

        # Police de caractères
        self.fonts = {
            'large': ('SF Pro Display', 16, 'bold'),
            'medium': ('SF Pro Text', 12),
            'small': ('SF Pro Text', 10),
            'tiny': ('SF Pro Text', 9),
        }

        # Pour les systèmes sans SF Pro, utiliser une police de fallback
        try:
            tk.font.Font(family='SF Pro Display', size=12)
        except:
            self.fonts = {
                'large': ('Helvetica', 16, 'bold'),
                'medium': ('Helvetica', 12),
                'small': ('Helvetica', 10),
                'tiny': ('Helvetica', 9),
            }

        # Configuration de la fenêtre
        self.root.title("Rush Hour")
        self.root.configure(bg=self.colors['background'])
        self.root.resizable(False, False)

        # Dimensionnement de l'interface
        board_size = self.cell_size * self.game.board.size
        control_width = 240  # Largeur de la zone de contrôle

        # Frame principale
        self.main_frame = tk.Frame(root, bg=self.colors['background'], padx=20, pady=20)
        self.main_frame.pack(fill='both', expand=True)

        # Frame pour le plateau de jeu
        self.board_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        self.board_frame.grid(row=0, column=0, padx=10, pady=10)

        # Canvas pour dessiner le plateau
        self.canvas = tk.Canvas(self.board_frame, width=board_size, height=board_size,
                                bg='#E5E5EA', highlightthickness=0)
        self.canvas.pack()

        # Frame pour les contrôles avec style épuré
        self.control_frame = tk.Frame(self.main_frame, bg=self.colors['background'], width=control_width)
        self.control_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')
        self.control_frame.grid_propagate(False)  # Maintient la largeur fixe

        # Titre du jeu
        title_label = tk.Label(self.control_frame, text="Rush Hour",
                               font=self.fonts['large'],
                               fg=self.colors['foreground'], bg=self.colors['background'])
        title_label.pack(pady=(0, 15), anchor='w')

        # Affichage du niveau
        self.level_frame = tk.Frame(self.control_frame, bg=self.colors['background'])
        self.level_frame.pack(fill='x', pady=5)

        self.level_label = tk.Label(self.level_frame, text="Niveau : 1 - Facile",
                                    font=self.fonts['medium'],
                                    fg=self.colors['foreground'], bg=self.colors['background'])
        self.level_label.pack(anchor='w')

        # Séparateur pour plus d'élégance
        self.add_separator(self.control_frame)

        # Section des niveaux prédéfinis
        predef_title = tk.Label(self.control_frame, text="Niveaux prédéfinis",
                                font=self.fonts['medium'],
                                fg=self.colors['foreground'], bg=self.colors['background'])
        predef_title.pack(anchor='w', pady=(10, 5))

        # Frame pour les boutons de niveaux prédéfinis
        predef_frame = tk.Frame(self.control_frame, bg=self.colors['background'])
        predef_frame.pack(fill='x', pady=5)

        # Boutons pour les niveaux prédéfinis avec lambda directe
        self.level1_button = self.create_button(predef_frame, "Niveau 1",
                                                lambda: self.load_level_wrapper(1))
        self.level1_button.pack(side='left', padx=(0, 5), fill='x', expand=True)

        self.level2_button = self.create_button(predef_frame, "Niveau 2",
                                                lambda: self.load_level_wrapper(2))
        self.level2_button.pack(side='left', padx=5, fill='x', expand=True)

        self.level3_button = self.create_button(predef_frame, "Niveau 3",
                                                lambda: self.load_level_wrapper(3))
        self.level3_button.pack(side='left', padx=5, fill='x', expand=True)

        # Séparateur
        self.add_separator(self.control_frame)

        # Section des niveaux aléatoires
        random_title = tk.Label(self.control_frame, text="Niveaux aléatoires",
                                font=self.fonts['medium'],
                                fg=self.colors['foreground'], bg=self.colors['background'])
        random_title.pack(anchor='w', pady=(10, 5))

        # Frame pour les boutons de niveaux aléatoires
        random_frame = tk.Frame(self.control_frame, bg=self.colors['background'])
        random_frame.pack(fill='x', pady=5)

        # Boutons pour les niveaux aléatoires
        self.random_easy_button = self.create_button(random_frame, "Facile",
                                                     lambda: self.generate_random_level_wrapper('easy'))
        self.random_easy_button.pack(side='left', padx=(0, 5), fill='x', expand=True)

        self.random_medium_button = self.create_button(random_frame, "Moyen",
                                                       lambda: self.generate_random_level_wrapper('medium'))
        self.random_medium_button.pack(side='left', padx=5, fill='x', expand=True)

        self.random_hard_button = self.create_button(random_frame, "Difficile",
                                                     lambda: self.generate_random_level_wrapper('hard'))
        self.random_hard_button.pack(side='left', padx=5, fill='x', expand=True)

        # Séparateur
        self.add_separator(self.control_frame)

        # Boutons d'action
        actions_title = tk.Label(self.control_frame, text="Actions",
                                 font=self.fonts['medium'],
                                 fg=self.colors['foreground'], bg=self.colors['background'])
        actions_title.pack(anchor='w', pady=(10, 5))

        # Bouton pour donner la solution
        self.solution_button = self.create_button(self.control_frame, "Afficher la solution",
                                                  lambda: self.show_solution_wrapper())
        self.solution_button.pack(fill='x', pady=5)

        # Bouton pour réinitialiser
        self.reset_button = self.create_button(self.control_frame, "Réinitialiser",
                                               lambda: self.reset_level_wrapper())
        self.reset_button.pack(fill='x', pady=5)

        # Séparateur
        self.add_separator(self.control_frame)

        # Compteur de mouvements
        stats_frame = tk.Frame(self.control_frame, bg=self.colors['background'])
        stats_frame.pack(fill='x', pady=10)

        stats_title = tk.Label(stats_frame, text="Statistiques",
                               font=self.fonts['medium'],
                               fg=self.colors['foreground'], bg=self.colors['background'])
        stats_title.pack(anchor='w')

        moves_frame = tk.Frame(self.control_frame, bg=self.colors['background'])
        moves_frame.pack(fill='x')

        tk.Label(moves_frame, text="Mouvements:",
                 font=self.fonts['small'],
                 fg=self.colors['foreground'], bg=self.colors['background']).pack(side='left')

        self.moves_label = tk.Label(moves_frame, text="0",
                                    font=self.fonts['small'],
                                    fg=self.colors['accent'], bg=self.colors['background'])
        self.moves_label.pack(side='right')

        # Évènements sur le canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        # Configure la barre de menu
        self.setup_menu()

        # Précharge les images des véhicules
        self.vehicle_images = self.preload_vehicle_images()

        # Dessine le plateau initial
        self.draw_board()

    # Fonctions wrapper pour les boutons pour s'assurer qu'ils fonctionnent toujours
    def load_level_wrapper(self, level):
        """Wrapper pour charger un niveau avec gestion des erreurs."""
        try:
            self.change_level(level)
        except Exception as e:
            print(f"Erreur lors du chargement du niveau {level}: {e}")
            messagebox.showerror("Erreur", f"Impossible de charger le niveau {level}. Réessayez.")

    def generate_random_level_wrapper(self, difficulty):
        """Wrapper pour générer un niveau aléatoire avec gestion des erreurs."""
        try:
            self.generate_random_level(difficulty)
        except Exception as e:
            print(f"Erreur lors de la génération du niveau {difficulty}: {e}")
            messagebox.showerror("Erreur", f"Impossible de générer un niveau {difficulty}. Réessayez.")

    def show_solution_wrapper(self):
        """Wrapper pour afficher la solution avec gestion des erreurs."""
        try:
            self.show_solution()
        except Exception as e:
            print(f"Erreur lors de l'affichage de la solution: {e}")
            messagebox.showerror("Erreur", "Impossible d'afficher la solution. Réessayez.")

    def reset_level_wrapper(self):
        """Wrapper pour réinitialiser le niveau avec gestion des erreurs."""
        try:
            self.reset_level()
        except Exception as e:
            print(f"Erreur lors de la réinitialisation du niveau: {e}")
            messagebox.showerror("Erreur", "Impossible de réinitialiser le niveau. Réessayez.")

    def create_button(self, parent, text, command, width=None, icon=None):
        """
        Crée un bouton gris simple avec une meilleure réactivité.

        Args:
            parent: Le widget parent
            text: Le texte du bouton
            command: La fonction à exécuter lors du clic
            width: Largeur optionnelle du bouton
            icon: Texte d'icône à afficher avant le texte principal (optionnel)

        Returns:
            Le bouton
        """
        # Texte avec ou sans icône
        display_text = text
        if icon:
            display_text = f"{icon} {text}"

        # Crée un bouton standard avec des paramètres améliorés pour la réactivité
        button = tk.Button(
            parent,
            text=display_text,
            command=command,
            fg="#333333",  # Texte gris foncé
            padx=15,
            pady=8,
            font=self.fonts['medium'],
            cursor="hand2",  # Curseur main au survol
            relief="raised",  # Style du bouton
            bd=1,  # Bordure plus visible
            highlightthickness=0,  # Pas de surbrillance supplémentaire
            takefocus=1  # Permet de prendre le focus
        )

        if width:
            button.config(width=width)

        # Ajoute des gestionnaires d'événements pour améliorer la réactivité
        button.bind("<Enter>", lambda e: button.config(relief="raised", bg="#F0F0F0"))
        button.bind("<Leave>", lambda e: button.config(relief="raised", bg="#E0E0E0"))

        return button

    def add_separator(self, parent):
        """Ajoute un séparateur élégant."""
        separator = tk.Frame(parent, height=1, bg='#E5E5EA')
        separator.pack(fill='x', pady=10)

    def preload_vehicle_images(self):
        """Précharge les images des véhicules ou génère des représentations stylisées."""
        images = {}

        try:
            # Essaie de charger des images si elles existent
            path = os.path.join(os.path.dirname(__file__), 'assets')
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.endswith('.png'):
                        img = Image.open(os.path.join(path, file))
                        images[file.split('.')[0]] = img
        except:
            pass

        # Si aucune image n'est chargée, crée des représentations stylisées
        if not images:
            # Crée les images stylisées pour les véhicules
            images = self.create_stylized_vehicles()

        return images

    def create_stylized_vehicles(self):
        """Crée des représentations stylisées des véhicules."""
        images = {}

        # Taille de base des images des véhicules
        car_width = int(self.cell_size * 1.8)
        car_height = int(self.cell_size * 0.8)
        truck_width = int(self.cell_size * 2.8)
        truck_height = int(self.cell_size * 0.8)

        # Voiture principale (rouge)
        main_car = Image.new('RGBA', (car_width, car_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(main_car)

        # Corps de la voiture
        draw.rounded_rectangle([(10, 5), (car_width - 10, car_height - 5)],
                               radius=15, fill=self.colors['X'])

        # Fenêtres
        draw.rounded_rectangle([(car_width // 4, 15), (car_width // 4 * 3, car_height - 15)],
                               radius=5, fill='#FFFFFF')

        # Roues
        wheel_size = 12
        wheel_margin = 20
        draw.ellipse([(wheel_margin, car_height - wheel_size - 5),
                      (wheel_margin + wheel_size, car_height - 5)], fill='#333333')
        draw.ellipse([(car_width - wheel_margin - wheel_size, car_height - wheel_size - 5),
                      (car_width - wheel_margin, car_height - 5)], fill='#333333')
        draw.ellipse([(wheel_margin, 5),
                      (wheel_margin + wheel_size, 5 + wheel_size)], fill='#333333')
        draw.ellipse([(car_width - wheel_margin - wheel_size, 5),
                      (car_width - wheel_margin, 5 + wheel_size)], fill='#333333')

        images['car_h_X'] = main_car

        # Voiture normale horizontale
        normal_car = Image.new('RGBA', (car_width, car_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(normal_car)

        # Corps de la voiture
        draw.rounded_rectangle([(10, 5), (car_width - 10, car_height - 5)],
                               radius=15, fill=self.colors['car'])

        # Fenêtres
        draw.rounded_rectangle([(car_width // 4, 15), (car_width // 4 * 3, car_height - 15)],
                               radius=5, fill='#FFFFFF')

        # Roues (même code que pour la voiture principale)
        draw.ellipse([(wheel_margin, car_height - wheel_size - 5),
                      (wheel_margin + wheel_size, car_height - 5)], fill='#333333')
        draw.ellipse([(car_width - wheel_margin - wheel_size, car_height - wheel_size - 5),
                      (car_width - wheel_margin, car_height - 5)], fill='#333333')
        draw.ellipse([(wheel_margin, 5),
                      (wheel_margin + wheel_size, 5 + wheel_size)], fill='#333333')
        draw.ellipse([(car_width - wheel_margin - wheel_size, 5),
                      (car_width - wheel_margin, 5 + wheel_size)], fill='#333333')

        images['car_h'] = normal_car

        # Voiture verticale (rotation de la voiture horizontale)
        images['car_v'] = normal_car.rotate(90, expand=True)
        images['car_v_X'] = main_car.rotate(90, expand=True)

        # Camion horizontal
        truck = Image.new('RGBA', (truck_width, truck_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(truck)

        # Corps du camion
        draw.rounded_rectangle([(10, 5), (truck_width - 10, truck_height - 5)],
                               radius=10, fill=self.colors['truck'])

        # Cabine
        draw.rounded_rectangle([(10, 5), (truck_width // 3, truck_height - 5)],
                               radius=10, fill=self.colors['truck'])

        # Fenêtre
        draw.rounded_rectangle([(20, 15), (truck_width // 3 - 10, truck_height - 15)],
                               radius=5, fill='#FFFFFF')

        # Roues
        wheel_positions = [
            wheel_margin,
            truck_width // 3 + wheel_margin,
            truck_width - wheel_margin - wheel_size
        ]

        for x in wheel_positions:
            draw.ellipse([(x, truck_height - wheel_size - 5),
                          (x + wheel_size, truck_height - 5)], fill='#333333')
            draw.ellipse([(x, 5),
                          (x + wheel_size, 5 + wheel_size)], fill='#333333')

        images['truck_h'] = truck

        # Camion vertical (rotation du camion horizontal)
        images['truck_v'] = truck.rotate(90, expand=True)

        return images

    def setup_menu(self):
        """Configure la barre de menu de style moderne."""
        menubar = tk.Menu(self.root)

        # Menu Fichier
        filemenu = tk.Menu(menubar, tearoff=0)

        # Sous-menu pour les niveaux prédéfinis
        levelsmenu = tk.Menu(filemenu, tearoff=0)
        levelsmenu.add_command(label="Niveau 1", command=lambda: self.load_level_wrapper(1))
        levelsmenu.add_command(label="Niveau 2", command=lambda: self.load_level_wrapper(2))
        levelsmenu.add_command(label="Niveau 3", command=lambda: self.load_level_wrapper(3))
        filemenu.add_cascade(label="Niveaux prédéfinis", menu=levelsmenu)

        # Sous-menu pour les niveaux aléatoires
        randommenu = tk.Menu(filemenu, tearoff=0)
        randommenu.add_command(label="Facile", command=lambda: self.generate_random_level_wrapper('easy'))
        randommenu.add_command(label="Moyen", command=lambda: self.generate_random_level_wrapper('medium'))
        randommenu.add_command(label="Difficile", command=lambda: self.generate_random_level_wrapper('hard'))
        filemenu.add_cascade(label="Niveaux aléatoires", menu=randommenu)

        filemenu.add_separator()
        filemenu.add_command(label="Réinitialiser", command=lambda: self.reset_level_wrapper())
        filemenu.add_separator()
        filemenu.add_command(label="Quitter", command=self.root.quit)
        menubar.add_cascade(label="Fichier", menu=filemenu)

        # Menu Aide
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Règles", command=self.show_rules)
        helpmenu.add_command(label="Solution", command=lambda: self.show_solution_wrapper())
        menubar.add_cascade(label="Aide", menu=helpmenu)

        # Menu Options
        optionsmenu = tk.Menu(menubar, tearoff=0)

        # Sous-menu pour la vitesse d'animation
        speedmenu = tk.Menu(optionsmenu, tearoff=0)
        self.speed_var = tk.IntVar(value=self.animation_speed)

        speedmenu.add_radiobutton(label="Lente", variable=self.speed_var, value=800,
                                  command=lambda: self.set_animation_speed(800))
        speedmenu.add_radiobutton(label="Moyenne", variable=self.speed_var, value=400,
                                  command=lambda: self.set_animation_speed(400))
        speedmenu.add_radiobutton(label="Rapide", variable=self.speed_var, value=200,
                                  command=lambda: self.set_animation_speed(200))

        optionsmenu.add_cascade(label="Vitesse d'animation", menu=speedmenu)

        menubar.add_cascade(label="Options", menu=optionsmenu)

        self.root.config(menu=menubar)

    def set_animation_speed(self, speed):
        """Définit la vitesse d'animation."""
        self.animation_speed = speed

    def draw_board(self):
        """Dessine le plateau de jeu et les véhicules stylisés."""
        # Efface le canvas
        self.canvas.delete("all")

        # Taille du plateau
        board_size = self.cell_size * self.game.board.size

        # Dessine l'arrière-plan
        self.canvas.create_rectangle(0, 0, board_size, board_size,
                                     fill='#E5E5EA', outline='')

        # Dessine la grille subtile
        for i in range(self.game.board.size + 1):
            # Lignes horizontales
            self.canvas.create_line(
                0, i * self.cell_size,
                   self.game.board.size * self.cell_size, i * self.cell_size,
                fill="#D1D1D6", width=1
            )
            # Lignes verticales
            self.canvas.create_line(
                i * self.cell_size, 0,
                i * self.cell_size, self.game.board.size * self.cell_size,
                fill="#D1D1D6", width=1
            )

        # Dessine la sortie (à droite en position y=2)
        exit_x, exit_y = self.game.board.exit_pos
        self.canvas.create_rectangle(
            exit_x * self.cell_size, exit_y * self.cell_size,
            (exit_x + 1) * self.cell_size, (exit_y + 1) * self.cell_size,
            fill="#FFD426", outline="", stipple="gray50"
        )

        # Dessine une flèche pour indiquer la sortie
        arrow_x = exit_x * self.cell_size + self.cell_size * 0.5
        arrow_y = exit_y * self.cell_size + self.cell_size * 0.5
        self.canvas.create_line(
            arrow_x - 20, arrow_y,
            arrow_x + 20, arrow_y,
            arrow='last', width=3, fill="#333333"
        )

        # Dessine les véhicules
        for vehicle in self.game.board.vehicles.values():
            # Coordonnées du véhicule
            x1 = vehicle.x * self.cell_size
            y1 = vehicle.y * self.cell_size

            if vehicle.orientation == 'H':
                x2 = (vehicle.x + vehicle.length) * self.cell_size
                y2 = (vehicle.y + 1) * self.cell_size
            else:  # Vertical
                x2 = (vehicle.x + 1) * self.cell_size
                y2 = (vehicle.y + vehicle.length) * self.cell_size

            # Détermine le type d'image à utiliser
            vehicle_type = 'car' if vehicle.length == 2 else 'truck'
            orientation = 'h' if vehicle.orientation == 'H' else 'v'
            image_key = f"{vehicle_type}_{orientation}"

            if vehicle.is_main:
                image_key = f"{image_key}_X"

            # Utilise l'image stylisée ou crée un rectangle de base si l'image n'existe pas
            if image_key in self.vehicle_images:
                # Redimensionne l'image selon la taille du véhicule
                img_width = x2 - x1
                img_height = y2 - y1
                img = self.vehicle_images[image_key].resize((img_width, img_height))

                # Convertit en format PhotoImage pour Tkinter
                photo = ImageTk.PhotoImage(img)

                # Stocke la référence (important pour Tkinter)
                setattr(self, f"photo_{vehicle.id}", photo)

                # Affiche l'image
                self.canvas.create_image(x1, y1, anchor='nw', image=photo,
                                         tags=("vehicle", vehicle.id))
            else:
                # Fallback: crée un rectangle coloré si l'image n'est pas disponible
                color = self.colors['X'] if vehicle.is_main else (
                    self.colors['car'] if vehicle.length == 2 else self.colors['truck'])

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color, outline="#000000", width=2,
                    tags=("vehicle", vehicle.id)
                )

            # Ajoute l'identifiant au centre du véhicule
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            self.canvas.create_text(
                center_x, center_y,
                text=vehicle.id, fill="#FFFFFF", font=self.fonts['medium']
            )

        # Met à jour le compteur de mouvements
        self.moves_label.config(text=str(self.game.moves_count))

        # Met à jour le niveau affiché
        difficulty, moves = self.game.get_level_difficulty()

        # Vérifie si le niveau est une chaîne de caractères (aléatoire) ou un nombre (prédéfini)
        if isinstance(self.game.current_level, str):
            level_text = f"Niveau : {self.game.current_level}"
        else:
            level_text = f"Niveau : {self.game.current_level} - {difficulty}"

        self.level_label.config(text=level_text)

        # Force la mise à jour de l'interface
        self.root.update()

    def on_canvas_click(self, event):
        """Gère les clics sur le canvas."""
        # Si une animation est en cours, ignore les clics
        if self.animation_in_progress:
            return

        # Convertit les coordonnées du clic en coordonnées de cellule
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        # Vérifie si un véhicule est à cette position
        vehicle = self.game.board.get_vehicle_at(x, y)
        if vehicle:
            self.selected_vehicle = vehicle

            # Enregistre la position initiale pour le déplacement
            self.start_drag_pos = (event.x, event.y)

            # Effet visuel de sélection
            coords = vehicle.get_coordinates()
            for cx, cy in coords:
                x1 = cx * self.cell_size
                y1 = cy * self.cell_size
                x2 = (cx + 1) * self.cell_size
                y2 = (cy + 1) * self.cell_size

                # Crée un effet de brillance autour de la cellule
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline=self.colors['accent'],
                    width=2,
                    tags="selection"
                )

    def on_canvas_drag(self, event):
        """Gère le glisser-déposer d'un véhicule avec animation fluide."""
        # Si une animation est en cours ou aucun véhicule n'est sélectionné, ignore
        if self.animation_in_progress or not self.selected_vehicle:
            return

        # Efface les effets de sélection précédents
        self.canvas.delete("selection")

        # Convertit les coordonnées du clic en coordonnées de cellule
        current_x = event.x
        current_y = event.y

        # Calcule le déplacement depuis le début du glisser
        delta_x = current_x - self.start_drag_pos[0]
        delta_y = current_y - self.start_drag_pos[1]

        # Détermine la direction du mouvement
        if self.selected_vehicle.orientation == 'H':
            if abs(delta_x) > self.cell_size / 2:  # Suffisamment déplacé horizontalement
                if delta_x > 0:
                    direction = 'right'
                else:
                    direction = 'left'

                # Tente de déplacer le véhicule
                if self.game.move_vehicle(self.selected_vehicle.id, direction):
                    # Réinitialise la position de départ du glisser
                    self.start_drag_pos = (current_x, current_y)
                    # Redessine le plateau
                    self.draw_board()

        else:  # Vertical
            if abs(delta_y) > self.cell_size / 2:  # Suffisamment déplacé verticalement
                if delta_y > 0:
                    direction = 'down'
                else:
                    direction = 'up'

                # Tente de déplacer le véhicule
                if self.game.move_vehicle(self.selected_vehicle.id, direction):
                    # Réinitialise la position de départ du glisser
                    self.start_drag_pos = (current_x, current_y)
                    # Redessine le plateau
                    self.draw_board()

    def on_canvas_release(self, event):
        """Gère le relâchement du clic."""
        # Si une animation est en cours, ignore
        if self.animation_in_progress:
            return

        # Efface les effets de sélection
        self.canvas.delete("selection")

        if self.selected_vehicle:
            self.selected_vehicle = None

            # Vérifie si le niveau est résolu
            if self.game.is_solved():
                self.show_victory_message()

    def change_level(self, level):
        """Change le niveau du jeu pour un niveau prédéfini."""
        if self.animation_in_progress:
            return

        if self.game.moves_count > 0:
            # Demande confirmation si une partie est en cours
            confirm = messagebox.askyesno(
                "Changer de niveau",
                "Votre progression actuelle sera perdue. Continuer?",
                icon='question'
            )
            if not confirm:
                return

        # Animation de chargement
        self.canvas.delete("all")
        self.canvas.create_text(
            self.cell_size * self.game.board.size / 2,
            self.cell_size * self.game.board.size / 2,
            text=f"Chargement du niveau {level}...",
            font=self.fonts['large'],
            fill=self.colors['accent']
        )
        self.root.update()

        # Charge le niveau
        self.game.load_level(level)
        self.draw_board()

    def generate_random_level(self, difficulty):
        """Génère un niveau aléatoire avec animation de chargement."""
        if self.animation_in_progress:
            return

        if self.game.moves_count > 0:
            # Demande confirmation si une partie est en cours
            confirm = messagebox.askyesno(
                "Générer un niveau aléatoire",
                "Votre progression actuelle sera perdue. Continuer?",
                icon='question'
            )
            if not confirm:
                return

        # Animation de chargement
        self.canvas.delete("all")
        self.canvas.create_text(
            self.cell_size * self.game.board.size / 2,
            self.cell_size * self.game.board.size / 2,
            text=f"Génération niveau {difficulty} aléatoire...",
            font=self.fonts['large'],
            fill=self.colors['accent']
        )
        self.root.update()

        # Génère le niveau
        if self.game.generate_random_level(difficulty):
            self.draw_board()
        else:
            messagebox.showerror("Erreur", "Impossible de générer un niveau aléatoire. Réessayez.")

    def reset_level(self):
        """Réinitialise le niveau actuel avec une animation élégante."""
        if self.animation_in_progress:
            return

        # Animation de réinitialisation
        self.canvas.create_rectangle(
            0, 0,
            self.cell_size * self.game.board.size,
            self.cell_size * self.game.board.size,
            fill=self.colors['background'],
            stipple="gray50",
            tags="reset_overlay"
        )
        self.canvas.create_text(
            self.cell_size * self.game.board.size / 2,
            self.cell_size * self.game.board.size / 2,
            text="Réinitialisation...",
            font=self.fonts['large'],
            fill=self.colors['accent'],
            tags="reset_text"
        )
        self.root.update()
        self.root.after(300)  # Pause pour l'animation

        # Efface l'overlay
        self.canvas.delete("reset_overlay", "reset_text")

        # Réinitialise le niveau
        self.game.reset_level()
        self.draw_board()

    def show_solution(self):
        """Montre la solution du niveau actuel avec animation élégante."""
        if self.animation_in_progress:
            return

        solution = self.game.get_solution()

        if not solution:
            messagebox.showinfo("Solution", "Aucune solution trouvée pour ce niveau.")
            return

        # Demande confirmation
        confirm = messagebox.askyesno(
            "Afficher la solution",
            f"Voulez-vous voir la solution en {len(solution)} mouvements?\n\nCela réinitialisera votre progression actuelle.",
            icon='question'
        )

        if not confirm:
            return

        # Réinitialise d'abord le niveau
        self.game.reset_level()
        self.draw_board()

        # Active le flag d'animation
        self.animation_in_progress = True

        # Animation de la solution
        self.animate_solution(solution)

    def animate_solution(self, solution, index=0):
        """
        Anime la solution pas à pas avec effets visuels.

        Args:
            solution (list): Liste de tuples (vehicle_id, direction)
            index (int): Index du mouvement actuel
        """
        if index >= len(solution):
            # Animation finale
            self.canvas.create_rectangle(
                0, 0,
                self.cell_size * self.game.board.size,
                self.cell_size * self.game.board.size,
                fill=self.colors['success'],
                stipple="gray50",
                tags="success_overlay"
            )
            self.canvas.create_text(
                self.cell_size * self.game.board.size / 2,
                self.cell_size * self.game.board.size / 2,
                text="Solution terminée!",
                font=self.fonts['large'],
                fill="white",
                tags="success_text"
            )
            self.root.update()
            self.root.after(1000)  # Pause
            self.canvas.delete("success_overlay", "success_text")

            # Désactive le flag d'animation
            self.animation_in_progress = False
            return

        # Récupère le mouvement actuel
        vehicle_id, direction = solution[index]

        # Highlight du véhicule sélectionné
        vehicle = self.game.board.vehicles.get(vehicle_id)
        if vehicle:
            x = vehicle.x * self.cell_size
            y = vehicle.y * self.cell_size
            width = vehicle.length * self.cell_size if vehicle.orientation == 'H' else self.cell_size
            height = self.cell_size if vehicle.orientation == 'H' else vehicle.length * self.cell_size

            # Effet de surbrillance
            highlight = self.canvas.create_rectangle(
                x, y, x + width, y + height,
                outline=self.colors['accent'],
                width=3,
                tags="highlight"
            )
            self.root.update()
            self.root.after(200)  # Pause pour l'effet

        # Effectue le mouvement
        self.game.move_vehicle(vehicle_id, direction)

        # Redessine le plateau
        self.draw_board()
        self.canvas.delete("highlight")

        # Continue l'animation après un délai
        self.root.after(self.animation_speed, lambda: self.animate_solution(solution, index + 1))

    def show_victory_message(self):
        """Affiche un message de victoire élégant."""
        # Effet de victoire
        board_size = self.cell_size * self.game.board.size

        # Active le flag d'animation
        self.animation_in_progress = True

        # Overlay semi-transparent
        overlay = self.canvas.create_rectangle(
            0, 0, board_size, board_size,
            fill=self.colors['success'],
            stipple="gray50",
            tags="victory_overlay"
        )

        # Texte de victoire
        victory_text = self.canvas.create_text(
            board_size / 2, board_size / 2 - 20,
            text="Niveau résolu!",
            font=self.fonts['large'],
            fill="white",
            tags="victory_text"
        )

        # Sous-texte
        moves_text = self.canvas.create_text(
            board_size / 2, board_size / 2 + 20,
            text=f"En {self.game.moves_count} mouvements",
            font=self.fonts['medium'],
            fill="white",
            tags="victory_text"
        )

        self.root.update()
        self.root.after(1500)  # Affiche le message pendant 1.5 secondes

        # Efface les éléments de victoire
        self.canvas.delete("victory_overlay", "victory_text")

        # Désactive le flag d'animation
        self.animation_in_progress = False

        # Propose de passer au niveau suivant
        if isinstance(self.game.current_level, int):
            # Si c'est un niveau prédéfini (numérique)
            if 0 < self.game.current_level < 3:
                if messagebox.askyesno("Niveau suivant", "Voulez-vous passer au niveau suivant?"):
                    self.change_level(self.game.current_level + 1)
            else:
                # Si c'est le dernier niveau prédéfini ou un autre cas
                difficulty = random.choice(['medium', 'hard'])
                if messagebox.askyesno("Nouveau niveau", f"Voulez-vous essayer un niveau {difficulty} aléatoire?"):
                    self.generate_random_level(difficulty)
        else:
            # Si c'est un niveau aléatoire (chaîne de caractères)
            # Détermine la difficulté basée sur le texte du niveau actuel
            if "facile" in str(self.game.current_level).lower() or "easy" in str(self.game.current_level).lower():
                next_difficulty = "medium"
                next_text = "moyen"
            elif "moyen" in str(self.game.current_level).lower() or "medium" in str(self.game.current_level).lower():
                next_difficulty = "hard"
                next_text = "difficile"
            else:
                next_difficulty = "hard"
                next_text = "difficile"

            if messagebox.askyesno("Nouveau niveau", f"Voulez-vous essayer un autre niveau {next_text} aléatoire?"):
                self.generate_random_level(next_difficulty)

    def show_rules(self):
        """Affiche les règles du jeu dans un style élégant."""
        rules_text = """
        Rush Hour - Règles du jeu:

        1. Le but du jeu est de faire sortir la voiture rouge par la sortie à droite.

        2. Les voitures (2 cases) et les camions (3 cases) ne peuvent se déplacer que
           dans leur orientation (horizontale ou verticale).

        3. Les véhicules ne peuvent pas traverser les autres véhicules.

        4. Faites glisser les véhicules avec la souris pour les déplacer.

        Amusez-vous bien!
        """
        messagebox.showinfo("Règles du jeu", rules_text)
