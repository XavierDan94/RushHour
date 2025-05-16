# levels.py
from vehicle import Vehicle


def get_level(level_number):
    """
    Retourne une liste de véhicules pour un niveau prédéfini.

    Args:
        level_number (int): Numéro du niveau (1, 2 ou 3)

    Returns:
        list: Liste de véhicules
    """
    if level_number == 1:
        # Niveau 1 - Facile (peu de véhicules, solution simple)
        return [
            # Voiture principale (rouge)
            Vehicle('X', 1, 2, 2, 'H', True),

            # Quelques voitures stratégiquement placées
            Vehicle('A', 0, 0, 2, 'H'),  # Voiture horizontale en haut à gauche
            Vehicle('B', 3, 0, 2, 'V'),  # Voiture verticale à droite
            Vehicle('C', 3, 3, 2, 'H'),  # Voiture horizontale en bas à droite
            Vehicle('D', 0, 3, 2, 'V'),  # Voiture verticale en bas à gauche

            # Un seul camion
            Vehicle('E', 4, 1, 3, 'V'),  # Camion vertical qui bloque la sortie
        ]

    elif level_number == 2:
        # Niveau 2 - Moyen (configuration différente avec défi progressif)
        return [
            # Voiture principale (rouge) plus près du centre
            Vehicle('X', 2, 2, 2, 'H', True),

            # Structure de blocage plus élaborée
            Vehicle('A', 0, 1, 2, 'H'),  # Voiture horizontale en haut à gauche
            Vehicle('B', 4, 0, 2, 'V'),  # Voiture verticale en haut à droite
            Vehicle('C', 0, 3, 2, 'H'),  # Voiture horizontale en bas à gauche
            Vehicle('D', 2, 3, 2, 'H'),  # Voiture horizontale juste sous X
            Vehicle('E', 2, 4, 2, 'V'),  # Voiture verticale en bas (partiellement sous D)

            # Véhicules stratégiques pour le puzzle
            Vehicle('F', 3, 0, 2, 'H'),  # Voiture horizontale en haut à droite
            Vehicle('G', 1, 0, 2, 'V'),  # Voiture verticale à gauche, bloquant le passage
            Vehicle('H', 1, 4, 2, 'H'),  # Voiture horizontale en bas

            # Camion bloquant la sortie
            Vehicle('I', 4, 1, 3, 'V'),  # Camion vertical bloquant la sortie
        ]

    elif level_number == 3:
        # Niveau 3 - Difficile (nouveau niveau optimisé pour être résolvable mais difficile)
        return [
            # Voiture principale (rouge) au milieu
            Vehicle('X', 2, 2, 2, 'H', True),

            # Véhicules bloquant la sortie et créant un défi
            Vehicle('A', 0, 0, 2, 'H'),  # Voiture en haut à gauche
            Vehicle('B', 3, 0, 2, 'H'),  # Voiture en haut à droite
            Vehicle('C', 2, 1, 2, 'V'),  # Voiture verticale bloquant la voiture rouge
            Vehicle('D', 1, 3, 2, 'H'),  # Voiture horizontale sous la voiture rouge
            Vehicle('E', 4, 2, 2, 'V'),  # Voiture verticale bloquant la sortie
            Vehicle('F', 3, 4, 2, 'H'),  # Voiture en bas à droite
            Vehicle('G', 0, 4, 2, 'H'),  # Voiture en bas à gauche

            # Véhicules verticaux stratégiques
            Vehicle('H', 0, 1, 3, 'V'),  # Camion à gauche
            Vehicle('I', 1, 0, 2, 'V'),  # Voiture au-dessus de la voiture rouge
            Vehicle('J', 5, 1, 3, 'V'),  # Camion à droite tout au bord
            Vehicle('K', 3, 3, 2, 'V'),  # Voiture verticale à droite

            # Camions supplémentaires pour compliquer la résolution
            Vehicle('L', 0, 5, 3, 'H'),  # Camion horizontal en bas
        ]
    else:
        # Si le niveau demandé n'existe pas, retourne un niveau simple
        return [
            Vehicle('X', 1, 2, 2, 'H', True),  # Voiture principale
            Vehicle('A', 0, 0, 2, 'H'),  # Une voiture en haut à gauche
            Vehicle('B', 3, 2, 2, 'V'),  # Une voiture qui bloque la sortie
        ]


def check_level_validity(vehicles):
    """
    Vérifie qu'un niveau est valide (pas de chevauchement de véhicules).

    Args:
        vehicles (list): Liste de véhicules

    Returns:
        bool: True si le niveau est valide
    """
    occupied_cells = set()

    for vehicle in vehicles:
        for x, y in get_coordinates(vehicle):
            if (x, y) in occupied_cells:
                print(f"Erreur: Cellule ({x}, {y}) occupée par plusieurs véhicules!")
                return False
            occupied_cells.add((x, y))

    return True


def get_coordinates(vehicle):
    """
    Retourne toutes les coordonnées occupées par un véhicule.

    Args:
        vehicle (Vehicle): Véhicule

    Returns:
        list: Liste de tuples (x, y)
    """
    coords = []

    if vehicle.orientation == 'H':
        for i in range(vehicle.length):
            coords.append((vehicle.x + i, vehicle.y))
    else:  # Vertical
        for i in range(vehicle.length):
            coords.append((vehicle.x, vehicle.y + i))

    return coords


# Vérifie que tous les niveaux prédéfinis sont valides
for level in range(1, 4):
    vehicles = get_level(level)
    if check_level_validity(vehicles):
        print(f"Niveau {level}: Valide avec {len(vehicles)} véhicules")
    else:
        print(f"Niveau {level}: INVALIDE - Vérifiez les positions des véhicules!")