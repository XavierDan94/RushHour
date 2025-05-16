# Rush Hour - Jeu de puzzle

Rush Hour, le célèbre casse tête est arrivé sur Python ! Votre mission : permettre à la voiture rouge de s'extirper sans s'arracher les cheveux. Bon courage !
## Installation

### Prérequis

Pour exécuter ce jeu, il est nécessaire d'avoir :
- Python 3.6 ou une version plus récente
- Bibliothèque PIL (Python Imaging Library, sous forme du package Pillow)

### Étapes d'installation

1. **Télécharger le dépot git** :
   ```
   git clone https://github.com/XavierDan94/RushHour.git
   cd rush-hour
   ```

2. **Installation de la dépendance** :
   ```
   pip install pillow
   ```

   Note : Si vous utilisez Python 3, vous devrez peut-être utiliser `pip3` au lieu de `pip`.

3. **Exécution le jeu** :
   ```
   python main.py
   ```

   Note : Si Python 3 utilisé, utiliser `python3` au lieu de `python`.

## Structure du dépôt

Le projet comprend :

- `main.py` : Point d'entrée du programme
- `game.py` : Gère la logique du jeu
- `gui.py` : Code l'interface graphique de l'utilisateur
- `board.py` : Réprésente la grille de jeu
- `vehicle.py` : Gestion des véhicules (camion ou voiture)
- `solver.py` : Comprend l'algorithme de résolution (ici, on utilisera A*)
- `level_generator.py` : Permet de générer des niveaux aléatoires
- `levels.py` : Comprend les niveaux pré-définis à l'avance

## Comment jouer

1. **Objectif du jeu** : Faire sortir la voiture à droite de la grille de jeu matérialisée par un carré jaune.

2. **Déplacer les véhicules** : Cliquez et faites glisser un véhicule pour le déplacer. Les voitures (2 cases) et les camions (3 cases) ne peuvent se déplacer que dans leur orientation (horizontale ou verticale).

3. **Niveaux disponibles** :
   - 3 niveaux prédéfinis
   - Niveaux aléatoires générés dans trois niveaux de difficulté (facile, moyen, difficile)

4. **Fonctionnalités supplémentaires** :
   - Bouton "Afficher la solution" pour voir la résolution automatique d'un niveau
   - Bouton "Réinitialiser" pour recommencer le niveau actuel

## Personnalisation

### Ajouter vos propres niveaux

Vous pouvez ajouter vos propres niveaux en modifiant le fichier `levels.py`. Le format pour définir un niveau est le suivant :

```python
[
    Vehicle('X', x, y, longueur, orientation, True),  # La voiture principale (toujours avec 'X' et is_main=True)
    Vehicle('A', x, y, longueur, orientation),  # Autres véhicules avec des identifiants uniques
    # ...
]
```

Où :
- `x`, `y` sont les coordonnées (0,0 est en haut à gauche)
- `longueur` est 2 pour les voitures et 3 pour les camions
- `orientation` est 'H' pour horizontal ou 'V' pour vertical

### Personnaliser l'apparence

Il est possible de personnaliser l'apparence des véhicule. Pour cela il suffit dans le dossier asset 
de placer des images PNG nommées comme suit :
   - `car_h_X.png` : Voiture principale horizontale
   - `car_h.png` : Voiture horizontale
   - `car_v.png` : Voiture verticale
   - `truck_h.png` : Camion horizontal
   - `truck_v.png` : Camion vertical

## Dépannage

**Erreur "ModuleNotFoundError: No module named 'PIL'"** :
   Exécutez `pip install pillow` pour installer la bibliothèque requise.
