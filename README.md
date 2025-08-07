# Anagrammes

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Un projet Python pour trouver des anagrammes et des anagrammes approximatives avec une tolérance configurable.

## Table des Matières

- [Description](#description)
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
  - [Exemple d'utilisation](#exemple-dutilisation)
  - [Visualisation de la progression](#visualisation-de-la-progression)
- [Structure du Projet](#structure-du-projet)
- [Configuration](#configuration)
- [Contribution](#contribution)
- [Licence](#licence)
- [Remerciements](#remerciements)

## Description

Ce projet implémente un moteur de recherche d'anagrammes en Python. Il permet de trouver des combinaisons de mots à partir d'une expression donnée, en prenant en compte une tolérance pour les anagrammes approximatives. Le programme normalise les entrées (suppression des accents, mise en minuscules, filtrage des caractères non alphabétiques) pour assurer une comparaison précise.

## Fonctionnalités

- **Normalisation de Texte** : Nettoyage et standardisation des chaînes de caractères pour une comparaison efficace.
- **Recherche d'Anagrammes Exactes** : Trouve des anagrammes parfaites (tolérance de 0).
- **Recherche d'Anagrammes Approximatives** : Permet de trouver des anagrammes même si quelques lettres diffèrent, grâce à un paramètre de tolérance.
- **Gestion de Dictionnaire** : Utilise un dictionnaire de mots pour construire les anagrammes.
- **Visualisation de la Progression** : Affiche en temps réel l'état de la recherche récursive pour un meilleur débogage et compréhension.
- **Sauvegarde de la Dernière Expression** : Maintient un historique simple de la dernière expression recherchée.

## Installation

1.  **Cloner le dépôt** :
    ```bash
    git clone https://github.com/votre-utilisateur/Anagrammes.git
    cd Anagrammes
    ```

2.  **Prérequis** :
    Assurez-vous d'avoir Python 3.x installé sur votre système.

3.  **Dictionnaire** :
    Le programme nécessite un fichier dictionnaire. Par défaut, il s'attend à un fichier nommé `dictionnaire.txt` (ou similaire) dans le même répertoire que le script `anagramme.py`. Chaque mot doit être sur une nouvelle ligne.

## Utilisation

Pour exécuter le programme, lancez le script `anagramme.py` depuis votre terminal :

```bash
python anagramme.py
```

Le programme vous invitera à entrer une expression et une tolérance.

### Exemple d'utilisation

```
Entrez l'expression à analyser : chien
Entrez la tolérance (0 pour exact) : 0
```

Le programme affichera ensuite les anagrammes trouvées.

### Visualisation de la progression

La fonction de recherche récursive a été instrumentée pour afficher sa progression. Vous verrez des messages détaillés dans la console, indiquant :

- L'état actuel de la récursion (lettres restantes, chemin actuel, tolérance).
- Les mots candidats qui sont testés.
- Quand une solution est trouvée.

Cela est particulièrement utile pour comprendre comment l'algorithme explore les différentes combinaisons.

## Structure du Projet

- `anagramme.py` : Le script principal contenant toute la logique de recherche d'anagrammes.
- `dictionnaire.txt` (exemple) : Un fichier texte contenant un mot par ligne, utilisé comme base pour la recherche d'anagrammes.
- `README.md` : Ce fichier de documentation.

## Configuration

Actuellement, les principales configurations se font via les entrées utilisateur (expression et tolérance).

Le chemin du dictionnaire est défini en dur dans le script. Si vous souhaitez utiliser un dictionnaire différent ou le placer ailleurs, vous devrez modifier la ligne correspondante dans `anagramme.py` :

```python
CHEMIN_DICTIONNAIRE = "dictionnaire.txt"
```

## Contribution

Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet, n'hésitez pas à :

1.  Forker le dépôt.
2.  Créer une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`).
3.  Commiter vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`).
4.  Pousser vers la branche (`git push origin feature/nouvelle-fonctionnalite`).
5.  Ouvrir une Pull Request.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Remerciements

- À tous ceux qui ont contribué à l'amélioration de ce code.
- Aux ressources et communautés Python pour leur soutien.
