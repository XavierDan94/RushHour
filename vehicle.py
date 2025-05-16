class Vehicle:
    def __init__(self, id, x, y, length, orientation, is_main=False):
        """
        Initialise un véhicule.

        Args:
            id (str): Identifiant d'un véhicule (ex: 'A', 'B', etc.)
            x (int): Position x initiale (colonne)
            y (int): Position y initiale (ligne)
            length (int): Longueur du véhicule (2 pour une voiture ou 3 pour un camion)
            orientation (str): 'H' pour horizontal, 'V' pour vertical
            is_main (bool): True si c'est la voiture rouge principale
        """
        self.id = id
        self.x = x
        self.y = y
        self.length = length
        self.orientation = orientation
        self.is_main = is_main

    def get_coordinates(self):
        """Retourne toutes les coordonnées occupées par le véhicule."""
        coords = []
        if self.orientation == 'H':  # Horizontal
            for i in range(self.length):
                coords.append((self.x + i, self.y))
        else:  # Vertical
            for i in range(self.length):
                coords.append((self.x, self.y + i))
        return coords

    def can_move(self, direction, board):
        """
        Vérifie si le véhicule peut se déplacer dans la direction donnée.

        Args:
            direction (str): 'up', 'down', 'left', 'right'
            board (Board): L'état actuel du plateau

        Returns:
            bool: True si le mouvement est possible
        """
        if self.orientation == 'H':  # Horizontal
            if direction in ['up', 'down']:
                return False  # Ne peut pas bouger verticalement

            if direction == 'left':
                new_x = self.x - 1
                if new_x < 0:
                    return False
                return board.is_cell_empty(new_x, self.y)

            if direction == 'right':
                new_x = self.x + self.length
                if new_x >= board.size:
                    return False
                return board.is_cell_empty(new_x, self.y)

        else:  # Vertical
            if direction in ['left', 'right']:
                return False  # Ne peut pas bouger horizontalement

            if direction == 'up':
                new_y = self.y - 1
                if new_y < 0:
                    return False
                return board.is_cell_empty(self.x, new_y)

            if direction == 'down':
                new_y = self.y + self.length
                if new_y >= board.size:
                    return False
                return board.is_cell_empty(self.x, new_y)

        return False

    def move(self, direction):
        """
        Déplace le véhicule dans la direction donnée.

        Args:
            direction (str): 'up', 'down', 'left', 'right'
        """
        if self.orientation == 'H':  # Horizontal
            if direction == 'left':
                self.x -= 1
            elif direction == 'right':
                self.x += 1

        else:  # Vertical
            if direction == 'up':
                self.y -= 1
            elif direction == 'down':
                self.y += 1
