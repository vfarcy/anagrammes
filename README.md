# Anagrammes : Un Chercheur d'Anagrammes Puissant

Ce script est un programme en ligne de commande (CLI) écrit en Python pour trouver toutes les anagrammes possibles d'une expression donnée. Il est conçu pour être à la fois rapide et flexible, en utilisant des structures de données avancées et en offrant plusieurs options à l'utilisateur.

## Fonctionnalités

- **Recherche Rapide** : Utilise une structure de données en **Trie (Arbre préfixe)** pour des recherches ultra-rapides, même avec de grands dictionnaires.
- **Cache Intelligent** : Le dictionnaire est traité et mis en cache dans un fichier `.pkl` lors du premier lancement. Les démarrages suivants sont quasi-instantanés.
- **Gestion des Accents** : Le programme normalise automatiquement les entrées et le dictionnaire pour gérer les caractères accentués (`é`, `à`, `ç`, etc.) de manière transparente.
- **Tolérance Ajustable** : Vous pouvez spécifier un nombre de "lettres non utilisées" autorisées, vous permettant de trouver des anagrammes qui n'utilisent pas toutes les lettres de l'expression d'origine.
- **Résultats Pertinents** : Les résultats sont triés par pertinence (du plus petit nombre de lettres non utilisées au plus grand).
- **Affichage Détaillé** : Chaque anagramme trouvée est affichée avec :
    - Le nombre total de lettres utilisées.
    - Les lettres exactes non utilisées (la "différence").
    - Le nombre de lettres non utilisées.
- **Interface Conviviale** : Le programme guide l'utilisateur avec des suggestions pour la tolérance et le nombre de résultats à afficher.
- **Barres de Progression** : Des barres de progression indiquent le chargement du dictionnaire et l'avancement de la recherche pour un meilleur confort d'utilisation.

## Prérequis

- Python 3.x

## Installation

L'installation est simple mais nécessite une étape manuelle **cruciale**.

1.  **Clonez ou téléchargez le projet.**

2.  **Créez le dictionnaire** :
    - Dans le répertoire racine du projet, créez un fichier nommé `dictionnaire.txt`.
    - **Remplissez ce fichier avec une liste de mots français**, un mot par ligne. Vous pouvez trouver de telles listes facilement en ligne (cherchez "liste de mots français txt"). Plus votre dictionnaire sera complet, meilleurs seront les résultats.

3.  **Lancez le programme une première fois** :
    ```bash
    python anagramme.py
    ```
    Lors de ce premier lancement, le script va :
    - Lire votre `dictionnaire.txt`.
    - Construire la structure de données Trie.
    - La sauvegarder dans un fichier cache `dictionnaire_canonique.pkl`.
    Cette étape peut prendre un peu de temps, mais les lancements suivants seront très rapides.

## Utilisation

Une fois l'installation terminée, lancez le script :
```bash
python anagramme.py
```

Le programme vous demandera ensuite d'entrer une expression. Suivez simplement les instructions à l'écran pour définir la tolérance et le nombre de résultats souhaités.

Pour quitter le programme, entrez `q` lorsque vous êtes invité à saisir une expression.

### Exemple de Session

```
==================================================
Entrez une expression (ou 'q' pour quitter): endive braisée
Entrez la tolérance (suggéré: 1): 1
Nombre max de résultats (suggéré: 23): 20

Lancement de la recherche (Trie) avec une tolérance de 1...
Lettres à utiliser (13): abdeeeiinrsv
Recherche: |████████████████████████████████████████| 100.00% En cours

----------------- RÉSULTATS -----------------
bien vide (10 lettres, différence: aers, 4 lettre(s) en moins)
braise endive (12 lettres, différence: v, 1 lettre(s) en moins)
... et 5 autre(s) résultat(s).
---------------------------------------------
```
