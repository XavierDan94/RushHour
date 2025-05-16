from copy import deepcopy


class Board:
    def __init__(self, size=6):
        """
        Initialise un la grille de jeu

        Args:
            size (int): Taille de la grille de jeu (6x6)
        """
        self.size = size
        self.vehicles = {}  # Dictionnaire permettant de stocker les véhicules
        self.exit_pos = (size - 1, 2)  # Position de la sortie

    def add_vehicle(self, vehicle):
        """
        Ajoute un véhicule à la grille en vérifiant qu'il n'y ait aucun chevauchement.

        Args:
            vehicle (Vehicle): Véhicule à ajouter

        Returns:
            bool: True si le véhicule a été ajouté avec succès
        """
        # On vérifie que toutes les coordonnées du véhicule à placer sont vides
        for x, y in vehicle.get_coordinates():
            if not self.is_cell_empty(x, y):
                print(f"Impossible d'ajouter le véhicule {vehicle.id} aux coordonnées {x},{y} - cellule occupée")
                return False

        # Si toutes les cellules sont vides, ajoute le véhicule
        self.vehicles[vehicle.id] = vehicle
        return True

    def is_cell_empty(self, x, y):
        """
        Vérifie si une cellule est vide.

        Args:
            x (int): Coordonnée x
            y (int): Coordonnée y

        Returns:
            bool: True si la cellule est vide
        """
        # On vérifie si la position est en dehors de la grille
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return False

        # On vérifie si un véhicule occupe une cellule
        for vehicle in self.vehicles.values():
            coords = vehicle.get_coordinates()
            if (x, y) in coords:
                return False

        return True

    def get_vehicle_at(self, x, y):
        """Retourne le véhicule à la position donnée ou None si je ne trouve rien."""
        for vehicle in self.vehicles.values():
            if (x, y) in vehicle.get_coordinates():
                return vehicle
        return None

    def move_vehicle(self, vehicle_id, direction):
        """
        Déplace un véhicule dans la direction donnée.

        Args:
            vehicle_id (str): ID du véhicule à déplacer
            direction (str): 'up', 'down', 'left', 'right'

        Returns:
            bool: True si le mouvement a été effectué
        """
        if vehicle_id not in self.vehicles:
            return False

        vehicle = self.vehicles[vehicle_id]
        if vehicle.can_move(direction, self):
            vehicle.move(direction)
            return True

        return False

    def is_solved(self):
        """
        Vérifie si le niveau est résolu (voiture rouge à la sortie).

        Returns:
            bool: True si le nivéau est résolu
        """
        for vehicle in self.vehicles.values():
            if vehicle.is_main:
                if vehicle.orientation == 'H' and vehicle.x + vehicle.length - 1 == self.exit_pos[0]:
                    return True
        return False

    def get_state_hash(self):
        """
        Retourne un hash unique de l'état actuel du plateau.
        Utile pour l'algorithme A*.
        """
        state = []
        for vid, vehicle in sorted(self.vehicles.items()):
            state.append((vid, vehicle.x, vehicle.y))
        return hash(tuple(state))

    def clone(self):
        """
        Crée une copie de la grille et de tous ses véhicules.
        Utile pour l'algorithme de recherche A*.
        """
        new_board = Board(self.size)
        new_board.exit_pos = self.exit_pos

        for vehicle in self.vehicles.values():
            from vehicle import Vehicle  # Import ici pour éviter l'import circulaire
            new_vehicle = Vehicle(
                vehicle.id,
                vehicle.x,
                vehicle.y,
                vehicle.length,
                vehicle.orientation,
                vehicle.is_main
            )
            new_board.add_vehicle(new_vehicle)

        return new_board
