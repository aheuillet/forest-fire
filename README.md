# Simulateur de feux de forêt

## Prérequis

- Python >=3.5
- Numpy 
- PyGame
- MatPlotlib
- PySimpleGui (installable via `pip install pysimplegui`)

## Structure de l'application

Le simulateur propose deux modes différents:

- Le mode *PyGame* exploitant PyGame pour proposer une animation graphique de la progression de la simulation mais ne lancant qu'une unique simulation.
- Le mode *fast* permettant d'itérer rapidement mais ne proposant qu'une simple barre de progression pour le suivi, sans animations graphiques. Il permet d'estimer le seuil critique de percolation en réalisant un Monte-Carlo sur des valeurs de percolation comprises entre 0 et 1, avec un pas et un nombre d'*epochs* défini par l'utilisateur.

Pour lancer l'application, il suffit d'exécuter la commande suivante:

```bash
python3 gui.py
```

On se retrouve alors devant une fenêtre offrant plusieurs paramètres à choisir:

- La taille de la grille utilisée dans la simulation (par défaut 25)
- Le nombre de départs de feu répartis sur la carte (par défaut 1)
- La probabilité qu'un arbre prenne feu (uniquement pour le mode *PyGame*, par défaut 0.5)
- Le nombre d'*epochs* (uniquement pour le mode *fast*, par défaut 1)
- Le pas utilisé pour incrémenter le coefficient de percolation (uniquement pour le mode *fast*, par défaut 0.1)

![Image menu 1](./images/menu1.png "Premier menu")

Une fois la simulation terminée, une courbe représentant la densité d'arbres restants en fonction du coefficient de percolation s'affiche.
Une fenêtre présentant diverses statistiques s'affiche également:

- La densité moyenne d'arbres restants sur l'ensemble des simulation
- Le nombre moyen d'itérations nécessaires pour terminer une simulation
- Le seuil critique de percolation estimé (uniquement pour le mode *fast*)


## Résultats
