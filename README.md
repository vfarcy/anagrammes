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

## Structure du Projet

Voici les fichiers et dossiers clés du projet :

- `anagramme.py` : Le script Python principal qui contient toute la logique du programme, y compris la construction du Trie, l'algorithme de recherche et l'interface utilisateur.
- `dictionnaire.txt` : Ce fichier doit être créé par l'utilisateur et contenir une liste de mots (un mot par ligne) qui serviront de base pour la recherche d'anagrammes.
- `dictionnaire_canonique.pkl` : Un fichier cache généré automatiquement par le programme lors du premier lancement. Il contient la structure de données Trie optimisée du dictionnaire, permettant des chargements quasi-instantanés lors des exécutions ultérieures.
- `LICENSE` : Contient les informations de licence du projet.
- `README.md` : Ce fichier de documentation que vous êtes en train de lire.

## Prérequis

- Python 3.x

Ce projet ne nécessite aucune bibliothèque Python externe. Toutes les dépendances sont incluses dans la distribution standard de Python.

## Comment ça marche (Aperçu Technique)

Le programme utilise plusieurs concepts pour offrir une recherche d'anagrammes efficace :

1.  **Normalisation des Données** : Toutes les entrées (expressions et mots du dictionnaire) sont normalisées. Cela implique de les convertir en minuscules et de supprimer les caractères accentués (par exemple, 'é' devient 'e') pour assurer une comparaison cohérente et insensible à la casse ou aux accents.

2.  **Trie Canonique** : Le cœur de l'optimisation réside dans la construction d'un Trie (arbre préfixe) spécial. Chaque nœud de ce Trie représente une séquence de lettres triées alphabétiquement (une forme "canonique"). Par exemple, les mots "chien" et "niche" auront la même forme canonique "cehin" et seront stockés sous le même chemin dans le Trie. Cela permet de regrouper efficacement tous les mots qui sont des anagrammes les uns des autres.

3.  **Algorithme de Recherche Récursive** : Pour trouver les anagrammes d'une expression donnée, le programme utilise un algorithme de recherche récursive. Il parcourt le Trie en utilisant un "compteur" des lettres disponibles dans l'expression d'origine. À chaque étape, il tente de former des mots à partir des lettres restantes et explore les branches du Trie.

4.  **Gestion de la Tolérance Symétrique** : La fonctionnalité de tolérance permet de trouver des anagrammes même si elles ne consomment pas toutes les lettres de l'expression d'origine (lettres "en moins") ou si elles nécessitent l'ajout de quelques lettres (lettres "en plus"). Le programme explore intelligemment les combinaisons de lettres pour satisfaire cette tolérance, offrant une grande flexibilité dans les résultats.

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
- **Interface Conviviale** : Le programme guide l'utilisateur avec des suggestions pour la tolérance et offre une exploration interactive des résultats par niveau de pertinence.
- **Barres de Progression** : Des barres de progression indiquent le chargement du dictionnaire et l'avancement de la recherche pour un meilleur confort d'utilisation.

## Structure du Projet

Voici les fichiers et dossiers clés du projet :

- `anagramme.py` : Le script Python principal qui contient toute la logique du programme, y compris la construction du Trie, l'algorithme de recherche et l'interface utilisateur.
- `dictionnaire.txt` : Ce fichier doit être créé par l'utilisateur et contenir une liste de mots (un mot par ligne) qui serviront de base pour la recherche d'anagrammes.
- `dictionnaire_canonique.pkl` : Un fichier cache généré automatiquement par le programme lors du premier lancement. Il contient la structure de données Trie optimisée du dictionnaire, permettant des chargements quasi-instantanés lors des exécutions ultérieures.
- `LICENSE` : Contient les informations de licence du projet.

- `README.md` : Ce fichier de documentation que vous êtes en train de lire.

## Prérequis

- Python 3.x

Ce projet ne nécessite aucune bibliothèque Python externe. Toutes les dépendances sont incluses dans la distribution standard de Python.

## Comment ça marche (Aperçu Technique)

Le programme utilise plusieurs concepts pour offrir une recherche d'anagrammes efficace :

1.  **Normalisation des Données** : Toutes les entrées (expressions et mots du dictionnaire) sont normalisées. Cela implique de les convertir en minuscules et de supprimer les caractères accentués (par exemple, 'é' devient 'e') pour assurer une comparaison cohérente et insensible à la casse ou aux accents.

2.  **Trie Canonique** : Le cœur de l'optimisation réside dans la construction d'un Trie (arbre préfixe) spécial. Chaque nœud de ce Trie représente une séquence de lettres triées alphabétiquement (une forme "canonique"). Par exemple, les mots "chien" et "niche" auront la même forme canonique "cehin" et seront stockés sous le même chemin dans le Trie. Cela permet de regrouper efficacement tous les mots qui sont des anagrammes les uns des autres.

3.  **Algorithme de Recherche Récursive** : Pour trouver les anagrammes d'une expression donnée, le programme utilise un algorithme de recherche récursive. Il parcourt le Trie en utilisant un "compteur" des lettres disponibles dans l'expression d'origine. À chaque étape, il tente de former des mots à partir des lettres restantes et explore les branches du Trie.

4.  **Gestion de la Tolérance Symétrique** : La fonctionnalité de tolérance permet de trouver des anagrammes même si elles ne consomment pas toutes les lettres de l'expression d'origine (lettres "en moins") ou si elles nécessitent l'ajout de quelques lettres (lettres "en plus"). Le programme explore intelligemment les combinaisons de lettres pour satisfaire cette tolérance, offrant une grande flexibilité dans les résultats.

## Algorithme de Recherche d'Anagrammes : Plongée Détaillée

La recherche d'anagrammes dans ce programme repose sur un algorithme de **recherche récursive avec backtracking**, optimisé par l'utilisation de la structure de données **Trie canonique**.

### Fonctionnement Pas à Pas (Exemple Conceptuel)

Imaginons que nous cherchions des anagrammes pour l'expression "rat" avec une tolérance de 0 (toutes les lettres doivent être utilisées).

1.  **Initialisation** :
    *   Lettres disponibles : `r, a, t` (compteur: `{'r':1, 'a':1, 't':1}`)
    *   Solution partielle actuelle : `[]` (vide)

2.  **Première étape de la récursion** :
    *   Le programme tente de former un premier mot à partir des lettres `r, a, t`.
    *   Il parcourt le Trie canonique. Supposons qu'il trouve le mot "art".
    *   Si "art" est trouvé :
        *   Lettres restantes : `r, a, t` - `a, r, t` = `{} ` (compteur vide)
        *   Solution partielle : `["art"]`
        *   Comme il ne reste plus de lettres et que la tolérance est respectée (0 lettres non utilisées), "art" est une solution valide.

    *   Supposons qu'il trouve le mot "rat".
    *   Si "rat" est trouvé :
        *   Lettres restantes : `r, a, t` - `r, a, t` = `{} ` (compteur vide)
        *   Solution partielle : `["rat"]`
        *   "rat" est une solution valide.

    *   Supposons qu'il trouve le mot "tar".
    *   Si "tar" est trouvé :
        *   Lettres restantes : `r, a, t` - `t, a, r` = `{} ` (compteur vide)
        *   Solution partielle : `["tar"]`
        *   "tar" est une solution valide.

    *   *Backtracking* : Après avoir exploré une branche (par exemple, après avoir trouvé "art"), le programme "revient en arrière" (backtracking) pour restaurer les lettres disponibles et explorer d'autres chemins.

Cet exemple est simplifié pour un seul mot. Pour des expressions plus longues et des anagrammes multi-mots, le processus se complexifie :

*   Le programme essaie de trouver un premier mot.
*   Pour chaque mot trouvé, il retire les lettres utilisées de l'expression d'origine.
*   Il appelle récursivement la fonction de recherche avec les lettres restantes et la solution partielle mise à jour.
*   Ce processus continue jusqu'à ce qu'il n'y ait plus de lettres ou que la tolérance soit atteinte.

### Complexité de l'Algorithme

La complexité de cet algorithme est intrinsèquement élevée en raison de la nature combinatoire du problème des anagrammes, surtout avec la gestion de la tolérance.

*   **Facteurs influençant la complexité :**
    *   **Longueur de l'expression d'entrée (N)** : Plus l'expression est longue, plus le nombre de combinaisons de lettres possibles est grand.
    *   **Taille du dictionnaire (M)** : Un dictionnaire plus grand signifie plus de mots à considérer à chaque étape de la récursion.
    *   **Profondeur de la récursion (K)** : Le nombre de mots composant l'anagramme finale.
    *   **Niveau de tolérance (T)** : C'est le facteur le plus impactant. Pour chaque niveau de tolérance, le programme doit explorer des combinaisons de lettres à ajouter ou à retirer, ce qui multiplie exponentiellement le nombre de chemins à explorer.

*   **Impact du Trie :** Le Trie canonique réduit considérablement le temps de recherche de mots valides à partir d'un ensemble de lettres donné, transformant une recherche potentiellement linéaire dans le dictionnaire en une recherche basée sur la longueur du mot.

*   **Nature de la complexité :** Bien que des optimisations comme le Trie et le pruning (élagage des branches non prometteuses) soient utilisées, la complexité reste de nature **exponentielle** dans le pire des cas, notamment à cause de la gestion de la tolérance qui implique de tester de nombreuses combinaisons de lettres.

### Améliorations Possibles

1.  **Parallélisation de la Recherche** : La partie de la recherche qui gère la tolérance symétrique (exploration des combinaisons de lettres à ajouter/retirer) peut être naturellement parallélisée. Chaque combinaison de lettres à tester peut être traitée indépendamment sur un cœur de processeur différent, accélérant significativement le processus pour des tolérances élevées.

2.  **Optimisation du Trie pour la Mémoire** : Pour des dictionnaires extrêmement volumineux, des techniques de compression du Trie (par exemple, Trie compressé ou Trie de suffixe) pourraient réduire l'empreinte mémoire, bien que cela puisse légèrement augmenter le temps d'accès.

3.  **Heuristiques de Pruning Avancées** : Développer des heuristiques plus intelligentes pour élaguer les branches de recherche. Par exemple, si un chemin partiel ne peut manifestement pas mener à une solution valide dans la tolérance donnée, il peut être abandonné plus tôt.

4.  **Pré-calculs pour les Expressions Courantes** : Pour les expressions très fréquemment recherchées, il serait possible de pré-calculer et de stocker leurs anagrammes dans une base de données, offrant des réponses instantanées pour ces cas.

5.  **Passage en Langage Bas Niveau (C/C++)** : Pour les parties les plus critiques en termes de performance (comme la construction du Trie ou les boucles internes de l'algorithme de recherche), une réécriture en langage compilé comme le C ou le C++ via des extensions Python (par exemple, Cython ou l'API C de Python) pourrait offrir des gains de vitesse substantiels, en particulier pour des dictionnaires très grands ou des expressions complexes.

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

Le programme vous demandera d'entrer une expression. Après la recherche, il affichera un résumé des résultats regroupés par "niveau de différence" (nombre de lettres non utilisées ou ajoutées).

```
==================================================
Entrez une expression (ou 'q' pour quitter): endive braisée
Entrez la tolérance (suggéré: 1): 1

Lancement de la recherche (Tolérance symétrique de 1)...
Recherche: |████████████████████████████████████████| 100.00% En cours

================= RÉSUMÉ DES RÉSULTATS =================
--- Différence 0: 2 résultat(s) (vert = parfait)
--- Différence 1: 7 résultat(s) (jaune = légère différence)
--- Différence 2: 0 résultat(s) (gris = aucune solution)

Quelle différence afficher ? ('n' pour nouvelle recherche, 'q' pour quitter): 1
```

Vous pouvez alors choisir un niveau de différence pour voir les anagrammes correspondantes. Les résultats sont affichés par pages de 25.

```
---------------------------------------------
  [1/7] "braise endive" (lettres retirées: v)
  [2/7] "bien vide" (lettres ajoutées: aers)
  ...
  [25/7] "..."

... 2 ligne(s) restante(s). Appuyez sur Entrée pour continuer, ou 'n' pour revenir au sommaire: [Entrée]

  [26/7] "..."
  [27/7] "..."
---------------------------------------------
```

Après avoir parcouru les résultats d'un niveau, vous pouvez appuyer sur `Entrée` pour voir la page suivante, ou `n` pour revenir au sommaire des résultats.

Pour lancer une nouvelle recherche, entrez `n` lorsque vous êtes invité à choisir une différence à afficher. Pour quitter le programme à tout moment, entrez `q`.

## Mode Test

Le programme inclut un mode test non-interactif, utile pour la validation ou l'intégration dans des scripts automatisés. Utilisez les arguments de ligne de commande suivants :

```bash
python anagramme.py --test --expression "votre expression" --expected "mot1 mot2" --tolerance N
```

- `--test` : Active le mode test.
- `--expression` : L'expression pour laquelle chercher les anagrammes (entre guillemets).
- `--expected` : L'anagramme attendue, sous forme de mots séparés par des espaces (entre guillemets).
- `--tolerance` : La tolérance numérique à appliquer pour la recherche.

Le mode test vérifiera si l'anagramme `--expected` est trouvée parmi les résultats pour l'expression et la tolérance données.

## Licence

Ce projet est distribué sous la [Licence MIT](LICENSE).
