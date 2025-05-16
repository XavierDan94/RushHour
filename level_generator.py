# level_generator.py
import random
import time
from board import Board
from vehicle import Vehicle
from solver import Solver


class LevelGenerator:
    def __init__(self, size=6):
        """
        Initialise le générateur de niveaux.

        Args:
            size (int): Taille du plateau
        """
        self.size = size

    def generate_level(self, min_vehicles=5, max_vehicles=10, max_attempts=100):
        """
        Génère un niveau aléatoire avec une solution.

        Args:
            min_vehicles (int): Nombre minimum de véhicules
            max_vehicles (int): Nombre maximum de véhicules
            max_attempts (int): Nombre maximum de tentatives

        Returns:
            tuple: (board, solution) ou (None, None) si aucune solution trouvée
        """
        for attempt in range(max_attempts):
            board = Board(self.size)

            # Ajoute la voiture principale (rouge) en position fixe
            # Varie un peu la position initiale de la voiture rouge pour plus de diversité
            red_car_x = random.randint(0, 3)  # Position entre 0 et 3 (pour une grille 6x6)
            main_car = Vehicle('X', red_car_x, 2, 2, 'H', True)

            if not board.add_vehicle(main_car):
                continue

            # Variables pour contrôler la complexité du niveau
            block_exit_directly = random.random() < 0.3  # 30% de chance d'avoir un bloqueur direct
            exit_column = self.size - 1  # Colonne de sortie (5 pour une grille 6x6)

            # IDs disponibles pour les véhicules
            available_ids = [chr(i) for i in range(65, 91) if chr(i) != 'X']  # A-Z sauf X
            random.shuffle(available_ids)  # Mélange les IDs pour plus de variété

            # Nombre aléatoire de véhicules à ajouter
            num_vehicles = random.randint(min_vehicles, max_vehicles)

            # Si on veut un bloqueur direct, ajoute-le d'abord
            if block_exit_directly:
                # Place un véhicule vertical qui bloque directement la sortie
                blocker_id = available_ids.pop(0)
                blocker_y = random.randint(0, 3)  # Position qui peut couvrir la ligne 2
                blocker_length = 3 if blocker_y == 0 else random.choice([2, 3])

                blocker = Vehicle(blocker_id, exit_column, blocker_y, blocker_length, 'V')

                # Vérifie que le bloqueur couvre bien la ligne de sortie
                blocker_coords = blocker.get_coordinates()
                blocks_exit = (exit_column, 2) in blocker_coords

                if blocks_exit and board.add_vehicle(blocker):
                    num_vehicles -= 1  # On a déjà ajouté un véhicule

            # Ajoute des véhicules qui créeront un puzzle intéressant
            vehicles_added = 0
            placement_attempts = 0

            while vehicles_added < num_vehicles and placement_attempts < 200 and available_ids:
                placement_attempts += 1

                vehicle_id = available_ids[0]

                # Détermine aléatoirement s'il s'agit d'une voiture ou d'un camion
                length = random.choice([2, 3])  # 2 pour voiture, 3 pour camion

                # Orientation aléatoire
                orientation = random.choice(['H', 'V'])

                # Position aléatoire en fonction de l'orientation et de la longueur
                if orientation == 'H':
                    x = random.randint(0, self.size - length)
                    y = random.randint(0, self.size - 1)

                    # Évite de bloquer la ligne de la voiture rouge
                    if y == 2 and (x <= main_car.x + 1 and x + length > main_car.x):
                        continue

                    # Pour les véhicules horizontaux, évite de les placer trop souvent à côté de X
                    if y == 2 and x == main_car.x + 2 and random.random() < 0.7:
                        continue  # 70% de chance de rejeter cette position

                else:  # Vertical
                    x = random.randint(0, self.size - 1)
                    y = random.randint(0, self.size - length)

                    # Évite de trop souvent bloquer le chemin de sortie directement
                    if x == exit_column and y <= 2 and y + length > 2:
                        # Si on a déjà un bloqueur direct ou si on a 70% de chance de rejeter
                        if block_exit_directly or random.random() < 0.7:
                            continue
                        else:
                            block_exit_directly = True  # On a maintenant un bloqueur direct

                    # Favorise les véhicules qui créent des dépendances intéressantes
                    # (ex: véhicules qui bloquent d'autres véhicules qui bloquent la voiture rouge)
                    if 2 < x < exit_column and random.random() < 0.6:
                        # 60% de chance de placer un véhicule vertical dans la zone de jeu
                        pass
                    elif x <= main_car.x and random.random() < 0.4:
                        # 40% de chance de placer un véhicule vertical qui bloque la voiture rouge
                        pass
                    elif random.random() < 0.3:
                        # Sinon, 30% de chance de rejeter pour favoriser d'autres positions
                        continue

                # Crée le véhicule
                new_vehicle = Vehicle(vehicle_id, x, y, length, orientation)

                # Tente d'ajouter le véhicule
                if board.add_vehicle(new_vehicle):
                    available_ids.pop(0)  # Retire l'ID utilisé
                    vehicles_added += 1
                    placement_attempts = 0  # Réinitialise le compteur de tentatives

            # Si on n'a pas pu ajouter assez de véhicules, on continue
            if vehicles_added < min_vehicles:
                continue

            # Trouve une solution
            solver = Solver(board)
            solution = solver.solve()

            # Vérifie que la solution est suffisamment complexe
            if solution:
                solution_length = len(solution)

                # Pour les niveaux faciles, on veut au moins 5 mouvements
                # Pour les niveaux moyens, on veut au moins 10 mouvements
                # Pour les niveaux difficiles, on veut au moins 15 mouvements
                min_solution_length = 5
                if min_vehicles >= 6:  # Niveau moyen
                    min_solution_length = 10
                if min_vehicles >= 8:  # Niveau difficile
                    min_solution_length = 15

                # Rejette les solutions trop courtes
                if solution_length < min_solution_length:
                    continue

                # Vérifie également que la solution n'est pas trop longue (évite les puzzles frustrants)
                if solution_length > 50:
                    continue

                print(f"Niveau généré avec {len(board.vehicles)} véhicules et {solution_length} mouvements")
                return board, solution

        # Aucune solution trouvée après max_attempts
        return None, None

    def generate_guaranteed_solvable_level(self, min_vehicles=5, max_vehicles=10, min_moves=5, max_moves=30):
        """
        Génère un niveau garantie soluble en partant d'un état de base et en faisant des mouvements aléatoires
        pour créer un puzzle difficile mais soluble.

        Args:
            min_vehicles (int): Nombre minimum de véhicules
            max_vehicles (int): Nombre maximum de véhicules
            min_moves (int): Nombre minimum de mouvements pour la solution
            max_moves (int): Nombre maximum de mouvements pour la solution

        Returns:
            tuple: (board, solution) ou (None, None) si échec
        """
        max_tries = 5  # Nombre maximal de tentatives

        for attempt in range(max_tries):
            try:
                print(f"Tentative de génération {attempt + 1}/{max_tries}")

                # Crée un plateau avec la voiture rouge à une position initiale difficile
                board = Board(self.size)
                # Position à gauche (0 ou 1) pour garantir un challenge
                red_car_x = random.randint(0, 1)  # Position 0 ou 1 pour plus de difficulté
                main_car = Vehicle('X', red_car_x, 2, 2, 'H', True)
                board.add_vehicle(main_car)

                # Ajoute plusieurs bloqueurs stratégiques sur le chemin vers la sortie
                exit_x = self.size - 1
                blocker_count = random.randint(2, 3)  # 2 ou 3 bloqueurs principaux

                # Positions des bloqueurs, réparties le long du chemin
                blocker_positions = []
                available_positions = list(range(red_car_x + 2, exit_x))

                if len(available_positions) >= blocker_count:
                    blocker_positions = sorted(random.sample(available_positions, blocker_count))
                else:
                    blocker_positions = available_positions

                # Ajoute les bloqueurs principaux
                for i, bx in enumerate(blocker_positions):
                    blocker_id = chr(ord('A') + i)
                    # Varie les positions verticales pour plus de complexité
                    if i % 2 == 0:
                        # Bloqueur qui couvre la ligne 2 (chemin de la voiture rouge)
                        by = random.choice([1, 0])
                        bl = 3 if by == 0 else 2
                    else:
                        # Bloqueur qui couvre aussi la ligne 2
                        by = random.choice([2, 1])
                        bl = 2

                    blocker = Vehicle(blocker_id, bx, by, bl, 'V')
                    if board.add_vehicle(blocker):
                        print(f"Bloqueur {blocker_id} ajouté à x={bx}, y={by}, longueur={bl}")

                # Ajoute des véhicules horizontaux qui bloquent les bloqueurs
                horizontal_blockers = []

                # Pour chaque bloqueur principal, essaie d'ajouter un ou deux véhicules qui le bloquent
                for i, bx in enumerate(blocker_positions):
                    blocker_id = chr(ord('A') + i)

                    # Ajoute un véhicule au-dessus ou en-dessous du bloqueur
                    if random.random() < 0.7:  # 70% de chance d'ajouter un bloqueur secondaire
                        h_id = chr(ord('D') + i * 2)
                        h_y = random.choice([0, 4])  # En haut ou en bas du plateau
                        h_x = max(0, bx - random.randint(0, 1))
                        h_length = random.choice([2, 3])

                        if h_x + h_length > self.size:
                            h_x = max(0, self.size - h_length)

                        horizontal_blockers.append((h_id, h_x, h_y, h_length, 'H'))

                    # Potentiellement un deuxième bloqueur secondaire
                    if random.random() < 0.5:  # 50% de chance d'en ajouter un deuxième
                        h_id = chr(ord('D') + i * 2 + 1)
                        h_y = 5 - h_y if 'h_y' in locals() else random.choice([0, 4])
                        h_x = max(0, bx - random.randint(0, 1))
                        h_length = random.choice([2, 3])

                        if h_x + h_length > self.size:
                            h_x = max(0, self.size - h_length)

                        horizontal_blockers.append((h_id, h_x, h_y, h_length, 'H'))

                # Ajoute les bloqueurs horizontaux
                for h_id, h_x, h_y, h_length, h_orientation in horizontal_blockers:
                    h_vehicle = Vehicle(h_id, h_x, h_y, h_length, h_orientation)
                    if board.add_vehicle(h_vehicle):
                        print(f"Bloqueur horizontal {h_id} ajouté à x={h_x}, y={h_y}")

                # Vérifie combien de véhicules ont été ajoutés jusqu'à présent
                vehicles_count = len(board.vehicles)

                # Ajoute des véhicules supplémentaires pour atteindre le nombre minimum
                if vehicles_count < min_vehicles:
                    additional_needed = min_vehicles - vehicles_count
                    additional_ids = [chr(ord('J') + i) for i in range(additional_needed)]

                    # Positions potentielles pour des véhicules additionnels
                    for i, vehicle_id in enumerate(additional_ids):
                        # Essaie plusieurs positions
                        for _ in range(10):  # Max 10 tentatives par véhicule
                            v_orientation = random.choice(['H', 'V'])
                            v_length = random.choice([2, 3])

                            if v_orientation == 'H':
                                v_x = random.randint(0, self.size - v_length)
                                v_y = random.randint(0, self.size - 1)

                                # Évite de chevaucher la voiture rouge
                                if v_y == 2 and (v_x <= main_car.x + 1 and v_x + v_length > main_car.x):
                                    continue
                            else:  # Vertical
                                v_x = random.randint(0, self.size - 1)
                                v_y = random.randint(0, self.size - v_length)

                                # Évite de chevaucher la voiture rouge
                                if v_x >= main_car.x and v_x <= main_car.x + 1 and v_y <= 2 and v_y + v_length > 2:
                                    continue

                            # Essaie d'ajouter le véhicule
                            additional_vehicle = Vehicle(vehicle_id, v_x, v_y, v_length, v_orientation)
                            if board.add_vehicle(additional_vehicle):
                                print(f"Véhicule additionnel {vehicle_id} ajouté")
                                break

                # Vérifie à nouveau le nombre de véhicules
                if len(board.vehicles) < min_vehicles:
                    print(f"Échec: seulement {len(board.vehicles)} véhicules sur {min_vehicles} requis")
                    continue

                # À ce stade, nous avons un niveau avec tous les véhicules placés
                # Maintenant, vérifions qu'il est soluble et obtenons la solution
                solver = Solver(board)
                start_time = time.time()
                solution = solver.solve(max_time=10.0)  # Maximum 10 secondes pour trouver une solution
                solve_time = time.time() - start_time

                if solution is None:
                    print("Échec: niveau insoluble")
                    continue

                solution_length = len(solution)
                print(f"Solution trouvée en {solve_time:.3f}s, {solution_length} mouvements")

                # Vérifie si la solution est dans la plage de mouvements souhaitée
                if solution_length < min_moves:
                    print(f"Solution trop courte: {solution_length} mouvements < {min_moves}")
                    continue

                if solution_length > max_moves:
                    print(f"Solution trop longue: {solution_length} mouvements > {max_moves}")
                    continue

                print(f"Niveau soluble généré: {len(board.vehicles)} véhicules, {solution_length} mouvements")
                return board, solution

            except Exception as e:
                print(f"Erreur pendant la génération: {e}")

        print("Échec de toutes les tentatives de génération")
        return None, None

    def _get_coordinates(self, vehicle):
        """Helper method to get coordinates of a vehicle."""
        coords = []
        if vehicle.orientation == 'H':
            for i in range(vehicle.length):
                coords.append((vehicle.x + i, vehicle.y))
        else:  # Vertical
            for i in range(vehicle.length):
                coords.append((vehicle.x, vehicle.y + i))
        return coords