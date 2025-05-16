import heapq
import time


class Solver:
    def __init__(self, board):
        """
        Initialise le solveur avec la grille initial.

        Args:
            board (Board): État initial de la grille
        """
        self.initial_board = board

    def heuristic(self, board):
        """
        Fonction heuristique améliorée pour A*.
        Combine plusieurs facteurs pour une estimation plus précise.

        Args:
            board (Board): État actuel de la grille

        Returns:
            float: Valeur heuristique
        """
        # Trouve la voiture principale
        main_car = None
        for vehicle in board.vehicles.values():
            if vehicle.is_main:
                main_car = vehicle
                break

        if not main_car:
            return float('inf')  # Pas de voiture principale trouvée

        # 1. Distance directe à la sortie
        exit_x = board.exit_pos[0]
        distance_to_exit = exit_x - (main_car.x + main_car.length - 1)

        # 2. Nombre de véhicules bloquant directement le chemin
        direct_blockers = 0
        blockers_ids = []

        for x in range(main_car.x + main_car.length, exit_x + 1):
            vehicle = board.get_vehicle_at(x, main_car.y)
            if vehicle and vehicle.id not in blockers_ids:
                direct_blockers += 1
                blockers_ids.append(vehicle.id)

        # 3. Pénalité pour les véhicules "bloquant les bloqueurs"
        secondary_blockers = 0

        for blocker_id in blockers_ids:
            blocker = board.vehicles[blocker_id]
            if blocker.orientation == 'V':  # Véhicule vertical
                # Vérifie les blocages vers le haut
                for y in range(blocker.y - 1, -1, -1):
                    if not board.is_cell_empty(blocker.x, y):
                        secondary_blockers += 1

                # Vérifie les blocages vers le bas
                for y in range(blocker.y + blocker.length, board.size):
                    if not board.is_cell_empty(blocker.x, y):
                        secondary_blockers += 1

        total_vehicles = len(board.vehicles)
        density_factor = total_vehicles / (board.size * board.size)

        # Combinaison des facteurs avec des poids optimisés
        h_value = (
                distance_to_exit * 1.0 +  # Poids standard pour la distance
                direct_blockers * 2.0 +  # Les bloqueurs directs sont importants
                secondary_blockers * 0.5 +  # Les bloqueurs secondaires sont moins importants
                density_factor * 3.0  # La densité influence la difficulté de mouvement
        )

        return h_value

    def solve(self, max_time=10.0):
        """
        Résout le puzzle en utilisant l'algorithme A* avec des optimisations.

        Args:
            max_time (float): Temps maximum de recherche en secondes

        Returns:
            list: Liste de tuples (vehicle_id, direction) représentant la solution,
                 ou None si aucune solution n'existe ou si le temps est dépassé
        """
        start_time = time.time()
        start_board = self.initial_board

        # File de priorité pour A*
        open_set = []

        # Ensemble des états déjà visités (utilise un set pour des recherches O(1))
        closed_set = set()

        # Dictionnaire pour retracer le chemin
        came_from = {}

        # Coût réel du départ à l'état actuel
        g_score = {}
        g_score[start_board.get_state_hash()] = 0

        # Estimation du coût total
        f_score = {}
        f_score[start_board.get_state_hash()] = self.heuristic(start_board)

        # Représente les mouvements qui ont mené à cet état
        moves = {}
        moves[start_board.get_state_hash()] = []

        # Ajoute l'état initial à la file de priorité
        heapq.heappush(open_set, (f_score[start_board.get_state_hash()], id(start_board), start_board))

        # Pour éviter les cycles, garde une trace des états déjà vus
        seen = {start_board.get_state_hash()}

        # Compteur de nœuds explorés pour le débogage
        nodes_explored = 0

        while open_set and time.time() - start_time < max_time:
            nodes_explored += 1

            # Récupère l'état avec le score f le plus bas
            _, _, current_board = heapq.heappop(open_set)
            current_hash = current_board.get_state_hash()

            # Vérifie si l'état actuel est une solution
            if current_board.is_solved():
                solve_time = time.time() - start_time
                print(f"Solution trouvée en {solve_time:.3f}s après exploration de {nodes_explored} nœuds")
                return moves[current_hash]

            # Ajoute l'état actuel à l'ensemble des états visités
            closed_set.add(current_hash)

            # Génère tous les mouvements possibles dans un ordre optimisé
            # Priorité aux véhicules bloquant directement la voiture principale
            sorted_vehicles = self._prioritize_vehicles(current_board)

            for vehicle_id in sorted_vehicles:
                vehicle = current_board.vehicles[vehicle_id]

                # Détermine les directions possibles selon l'orientation
                if vehicle.orientation == 'H':
                    directions = ['left', 'right']
                else:
                    directions = ['up', 'down']

                for direction in directions:
                    # Crée une copie du plateau pour tester le mouvement
                    new_board = current_board.clone()

                    # Tente de déplacer le véhicule
                    if new_board.move_vehicle(vehicle_id, direction):
                        neighbor_hash = new_board.get_state_hash()

                        # Ignore les états déjà visités ou vus
                        if neighbor_hash in closed_set or neighbor_hash in seen:
                            continue

                        # Marque cet état comme vu
                        seen.add(neighbor_hash)

                        # Coût pour atteindre ce nouvel état
                        tentative_g_score = g_score[current_hash] + 1

                        # Si cet état n'a pas encore été découvert ou le nouveau chemin est meilleur
                        if neighbor_hash not in g_score or tentative_g_score < g_score[neighbor_hash]:
                            # Met à jour les scores
                            g_score[neighbor_hash] = tentative_g_score
                            f_score[neighbor_hash] = tentative_g_score + self.heuristic(new_board)

                            # Enregistre le mouvement qui a mené à cet état
                            new_moves = moves[current_hash].copy()
                            new_moves.append((vehicle_id, direction))
                            moves[neighbor_hash] = new_moves

                            # Ajoute l'état à la file de priorité
                            heapq.heappush(open_set, (f_score[neighbor_hash], id(new_board), new_board))

        # Temps écoulé ou aucune solution trouvée
        if time.time() - start_time >= max_time:
            print(f"Temps dépassé après exploration de {nodes_explored} nœuds")
        else:
            print(f"Aucune solution trouvée après exploration de {nodes_explored} nœuds")

        return None

    def _prioritize_vehicles(self, board):
        """
        Trie les véhicules pour prioriser ceux qui sont les plus pertinents à déplacer.

        Args:
            board (Board): État actuel de la grille

        Returns:
            list: Liste triée des IDs de véhicules
        """
        vehicles_scores = {}
        main_car = None

        # Trouve la voiture principale
        for vehicle in board.vehicles.values():
            if vehicle.is_main:
                main_car = vehicle
                break

        if not main_car:
            return list(board.vehicles.keys())

        # Évalue chaque véhicule
        for vehicle_id, vehicle in board.vehicles.items():
            # Par défaut, score moyen
            score = 50

            # La voiture principale est prioritaire
            if vehicle.is_main:
                score = 100

            # Les véhicules qui bloquent directement la voiture principale sont prioritaires
            elif (vehicle.orientation == 'V' and
                  vehicle.x > main_car.x + main_car.length - 1 and
                  vehicle.x <= board.exit_pos[0] and
                  vehicle.y <= main_car.y and vehicle.y + vehicle.length > main_car.y):
                score = 90

            # Les véhicules qui bloquent les bloqueurs sont aussi importants
            elif vehicle.orientation == 'H':
                # Vérifie si ce véhicule bloque un véhicule vertical important
                for other_id, other in board.vehicles.items():
                    if other.orientation == 'V' and other.x > main_car.x:
                        if (vehicle.y == other.y - 1 or vehicle.y == other.y + other.length) and \
                                (other.x >= vehicle.x and other.x < vehicle.x + vehicle.length):
                            score = 80
                            break

            vehicles_scores[vehicle_id] = score

        # Trie les véhicules par score décroissant
        return sorted(board.vehicles.keys(), key=lambda vid: vehicles_scores[vid], reverse=True)
