# game.py
import time
import random
from board import Board
from vehicle import Vehicle
from solver import Solver
from level_generator import LevelGenerator
import levels


class Game:
    def __init__(self):
        """Initialise le jeu."""
        # Initialisation des attributs principaux
        self.board = None
        self.initial_board = None
        self.current_level = 1  # Niveau par défaut (entier pour les niveaux prédéfinis)
        self.moves_count = 0
        self.solutions = {}  # Cache des solutions: {niveau: solution}

        # Taille standard du plateau
        self.board_size = 6

        # Crée un plateau vide initial
        from board import Board
        self.board = Board(self.board_size)

        # Charge le premier niveau prédéfini
        self.load_level(self.current_level)

        # Sauvegarde l'état initial
        self.initial_board = self.board.clone()

        print(f"Jeu initialisé avec le niveau {self.current_level}")

    def load_level(self, level_number):
        """
        Charge un niveau prédéfini.

        Args:
            level_number (int): Numéro du niveau
        """
        self.current_level = level_number
        self.moves_count = 0

        # Crée un nouveau plateau
        self.board = Board()

        # Ajoute les véhicules du niveau
        vehicles = levels.get_level(level_number)
        for vehicle in vehicles:
            success = self.board.add_vehicle(vehicle)
            if not success:
                print(f"Erreur: Impossible d'ajouter le véhicule {vehicle.id} - position occupée")

        # Sauvegarde l'état initial du plateau
        self.initial_board = self.board.clone()

        # Réinitialise la solution en cache pour ce niveau
        if level_number in self.solutions:
            del self.solutions[level_number]

        # Vérifie que le niveau est soluble
        solver = Solver(self.board.clone())
        solution = solver.solve(max_time=5.0)

        if solution is None:
            print(f"ALERTE: Le niveau {level_number} pourrait être insoluble!")
            # Tente de charger un niveau aléatoire à la place
            if not self.generate_random_level('medium'):
                # Si la génération échoue, crée un niveau très simple soluble
                self.board = Board()
                self.board.add_vehicle(Vehicle('X', 1, 2, 2, 'H', True))
                self.board.add_vehicle(Vehicle('A', 3, 2, 2, 'V'))
                self.initial_board = self.board.clone()

    def generate_random_level(self, difficulty='medium'):
        """
        Génère un niveau aléatoire fiable.

        Args:
            difficulty (str): 'easy', 'medium' ou 'hard'

        Returns:
            bool: True si un niveau a été généré avec succès
        """
        # Paramètres selon la difficulté
        if difficulty == 'easy':
            min_vehicles = 5
            max_vehicles = 8
            min_moves = 5
            max_moves = 15
        elif difficulty == 'medium':
            min_vehicles = 7
            max_vehicles = 10
            min_moves = 10
            max_moves = 25
        else:  # 'hard'
            min_vehicles = 9
            max_vehicles = 13
            min_moves = 15
            max_moves = 40

        # Crée un générateur de niveaux
        generator = LevelGenerator()

        # Indicateur spécial pour marquer qu'il s'agit d'un niveau aléatoire
        self.current_level = f"Aléatoire ({difficulty})"

        # Nombre maximum de tentatives
        max_attempts = 5

        # Tentatives multiples pour générer un niveau
        for attempt in range(max_attempts):
            try:
                print(f"Tentative {attempt + 1}/{max_attempts} de génération de niveau aléatoire {difficulty}")

                # Tente de générer un niveau aléatoire
                board, solution = generator.generate_level(min_vehicles, max_vehicles)

                if board and solution:
                    # Vérifie si la solution est dans la plage de mouvements souhaitée
                    if len(solution) < min_moves:
                        print(f"Solution trop courte: {len(solution)} mouvements")
                        continue  # Trop facile, essaie encore

                    if len(solution) > max_moves:
                        print(f"Solution trop longue: {len(solution)} mouvements")
                        continue  # Trop difficile, essaie encore

                    # Stocke la solution
                    self.solutions[self.current_level] = solution

                    # Charge le plateau généré
                    self.board = board
                    self.initial_board = board.clone()
                    self.moves_count = 0

                    print(
                        f"Niveau aléatoire généré avec succès: {len(board.vehicles)} véhicules, {len(solution)} mouvements")
                    return True
            except Exception as e:
                print(f"Erreur lors de la génération: {e}")

        # Si toutes les tentatives échouent, on génère un niveau de secours basé sur un niveau prédéfini
        # avec quelques modifications pour le rendre légèrement différent
        print("Utilisation d'un niveau de secours basé sur un niveau prédéfini")

        # Charge un niveau prédéfini comme base
        base_level = 1 if difficulty == 'easy' else (2 if difficulty == 'medium' else 3)
        vehicles = levels.get_level(base_level)

        # Apporte quelques modifications aléatoires mineures
        for vehicle in vehicles:
            if not vehicle.is_main:  # Ne pas toucher à la voiture rouge
                # 50% de chance de déplacer le véhicule d'une case si possible
                if random.random() < 0.5:
                    if vehicle.orientation == 'H':
                        offset = random.choice([-1, 1])
                        if 0 <= vehicle.x + offset <= 6 - vehicle.length:
                            vehicle.x += offset
                    else:  # Vertical
                        offset = random.choice([-1, 1])
                        if 0 <= vehicle.y + offset <= 6 - vehicle.length:
                            vehicle.y += offset

        # Crée un nouveau plateau avec ces véhicules
        self.board = Board(6)

        # Ajoute les véhicules en vérifiant qu'il n'y a pas de chevauchement
        valid_vehicles = []
        occupied_cells = set()

        # Ajoute d'abord la voiture principale
        for vehicle in vehicles:
            if vehicle.is_main:
                valid_vehicles.append(vehicle)
                for x, y in self._get_coordinates(vehicle):
                    occupied_cells.add((x, y))
                break

        # Puis les autres véhicules
        for vehicle in vehicles:
            if not vehicle.is_main:
                # Vérifie qu'il n'y a pas de chevauchement
                valid = True
                for x, y in self._get_coordinates(vehicle):
                    if (x, y) in occupied_cells:
                        valid = False
                        break

                if valid:
                    valid_vehicles.append(vehicle)
                    for x, y in self._get_coordinates(vehicle):
                        occupied_cells.add((x, y))

        # Ajoute les véhicules valides au plateau
        for vehicle in valid_vehicles:
            self.board.add_vehicle(vehicle)

        # Trouve une solution pour ce niveau de secours
        solver = Solver(self.board)
        solution = solver.solve()

        if solution:
            self.solutions[self.current_level] = solution
            self.initial_board = self.board.clone()
            self.moves_count = 0
            print(f"Niveau de secours généré avec {len(valid_vehicles)} véhicules")
            return True

        # Si même le niveau de secours échoue, on revient au niveau 1
        print("Échec du niveau de secours, chargement du niveau 1")
        self.load_level(1)
        return False

    def _get_coordinates(self, vehicle):
        """Aide pour obtenir les coordonnées d'un véhicule."""
        coords = []
        if vehicle.orientation == 'H':
            for i in range(vehicle.length):
                coords.append((vehicle.x + i, vehicle.y))
        else:  # Vertical
            for i in range(vehicle.length):
                coords.append((vehicle.x, vehicle.y + i))
        return coords

    def load_level(self, level_number):
        """
        Charge un niveau prédéfini.

        Args:
            level_number (int): Numéro du niveau
        """
        self.current_level = level_number
        self.moves_count = 0

        # Crée un nouveau plateau
        self.board = Board(6)

        # Ajoute les véhicules du niveau
        vehicles = levels.get_level(level_number)
        for vehicle in vehicles:
            self.board.add_vehicle(vehicle)

        # Sauvegarde l'état initial du plateau
        self.initial_board = self.board.clone()

        # Réinitialise la solution en cache pour ce niveau
        if level_number in self.solutions:
            del self.solutions[level_number]

        print(f"Niveau {level_number} chargé avec {len(vehicles)} véhicules")

    def reset_level(self):
        """Réinitialise le niveau actuel."""
        if self.initial_board:
            self.board = self.initial_board.clone()
            self.moves_count = 0

    def move_vehicle(self, vehicle_id, direction):
        """
        Déplace un véhicule dans la direction donnée.

        Args:
            vehicle_id (str): ID du véhicule à déplacer
            direction (str): 'up', 'down', 'left', 'right'

        Returns:
            bool: True si le mouvement a été effectué
        """
        if self.board.move_vehicle(vehicle_id, direction):
            self.moves_count += 1
            return True
        return False

    def is_solved(self):
        """
        Vérifie si la grille est résolu.

        Returns:
            bool: True si résolu
        """
        return self.board.is_solved()

    def get_solution(self):
        """
        Retourne la solution de la grille actuelle.

        Returns:
            list: Liste de tuples (vehicle_id, direction), ou None si pas de solution
        """
        # Vérifie si la solution est en cache
        if self.current_level in self.solutions:
            return self.solutions[self.current_level]

        # Sinon, calcule la solution
        solver = Solver(self.initial_board.clone())
        solution = solver.solve()

        # Stocke la solution en cache
        self.solutions[self.current_level] = solution

        return solution

    def get_current_state(self):
        """
        Retourne l'état actuel du jeu pour sauvegarder.

        Returns:
            dict: État actuel du jeu
        """
        return {
            'current_level': self.current_level,
            'moves_count': self.moves_count,
            'board': self.serialize_board(self.board),
            'initial_board': self.serialize_board(self.initial_board)
        }

    def load_state(self, state):
        """
        Charge un état sauvegardé.

        Args:
            state (dict): État à charger

        Returns:
            bool: True si le chargement a réussi
        """
        try:
            self.current_level = state['current_level']
            self.moves_count = state['moves_count']
            self.board = self.deserialize_board(state['board'])
            self.initial_board = self.deserialize_board(state['initial_board'])
            return True
        except Exception as e:
            print(f"Erreur lors du chargement de l'état: {e}")
            return False

    @staticmethod
    def serialize_board(board):
        """
        Sérialise un Board en dictionnaire.

        Args:
            board (Board): Plateau à sérialiser

        Returns:
            dict: Plateau sérialisé
        """
        vehicles_data = []
        for vehicle in board.vehicles.values():
            vehicles_data.append({
                'id': vehicle.id,
                'x': vehicle.x,
                'y': vehicle.y,
                'length': vehicle.length,
                'orientation': vehicle.orientation,
                'is_main': vehicle.is_main
            })

        return {
            'size': board.size,
            'exit_pos': board.exit_pos,
            'vehicles': vehicles_data
        }

    @staticmethod
    def deserialize_board(data):
        """
        Désérialise un dictionnaire en Board.

        Args:
            data (dict): Dictionnaire à désérialiser

        Returns:
            Board: Plateau désérialisé
        """
        board = Board(data['size'])
        board.exit_pos = data['exit_pos']

        for vehicle_data in data['vehicles']:
            vehicle = Vehicle(
                vehicle_data['id'],
                vehicle_data['x'],
                vehicle_data['y'],
                vehicle_data['length'],
                vehicle_data['orientation'],
                vehicle_data['is_main']
            )
            board.add_vehicle(vehicle)

        return board

    def get_level_difficulty(self):
        """
        Retourne la difficulté estimée du niveau actuel.

        Returns:
            tuple: (difficulté en texte, nombre de mouvements)
        """
        solution = self.get_solution()

        if not solution:
            return "Inconnue", 0

        moves = len(solution)

        # Détermine la difficulté en fonction du nombre de mouvements
        if moves < 15:
            difficulty = "Facile"
        elif moves < 30:
            difficulty = "Moyenne"
        else:
            difficulty = "Difficile"

        return difficulty, moves

    def get_hint(self):
        """
        Retourne un indice pour le mouvement suivant.

        Returns:
            tuple: (vehicle_id, direction) ou None
        """
        solution = self.get_solution()

        if not solution or self.moves_count >= len(solution):
            return None

        return solution[self.moves_count]