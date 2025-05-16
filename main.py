# main.py
import tkinter as tk
import random
from game import Game
from gui import GameGUI


def setup_appearance():
    try:
        from tkmacosx import set_appearance_mode
        set_appearance_mode("Light")
    except ImportError:
        pass


def main():
    # Crée la fenêtre principale
    root = tk.Tk()
    setup_appearance()

    # Définit l'icône et les propriétés de la fenêtre
    root.title("Rush Hour")

    try:
        # Essaie de définir l'icône si disponible
        img = tk.PhotoImage(file="assets/icon.png")
        root.iconphoto(True, img)
    except:
        pass

    # Initialise le jeu
    game = Game()

    # Génère un niveau aléatoire au démarrage
    difficulty = random.choice(['medium', 'hard'])  # Préfère les niveaux plus difficiles
    if not game.generate_random_level(difficulty):
        # Si la génération échoue, charge un niveau prédéfini
        game.load_level(random.randint(2, 3))

    # Crée et lance l'interface graphique
    gui = GameGUI(root, game)

    # Centre la fenêtre
    root.update()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"+{x}+{y}")

    # Lance la boucle principale
    root.mainloop()


if __name__ == "__main__":
    main()