# Anagrammes : Un Chercheur d'Anagrammes Intelligent

## 1. Objectif du Projet

Ce projet est un programme en Python capable de trouver des anagrammes pour une expression donnée (un ou plusieurs mots). Il ne se contente pas de trouver des anagrammes parfaits ; il peut également identifier des **solutions approximatives** en ajoutant ou en retirant des lettres, ce qui le rend beaucoup plus flexible et créatif.

Le programme est conçu pour être à la fois performant, grâce à un dictionnaire prétraité, et ergonomique, avec une interface interactive qui guide l'utilisateur.

## 2. Fonctionnalités

- **Anagrammes Multi-mots** : Trouvez des anagrammes composés de plusieurs mots du dictionnaire.
- **Tolérance aux Imperfections (`diff`)** : Spécifiez un niveau de tolérance pour trouver des solutions qui ne sont pas des anagrammes parfaits. Le programme peut "ignorer" des lettres de l'expression d'origine ou "emprunter" des lettres du dictionnaire.
- **Dictionnaire Prétraité** : Pour des recherches quasi-instantanées, le programme utilise un dictionnaire pré-calculé où chaque mot est stocké sous une forme "canonique".
- **Affichage Détaillé** : Les résultats indiquent clairement les lettres non utilisées (`reste`), les lettres ajoutées (`ajouté`) et la différence totale (`diff`) pour comprendre comment la solution a été formée.
- **Limite de Résultats Intelligente** : Le programme suggère une limite de résultats à afficher en utilisant une **courbe de croissance logistique (sigmoïde)**. Cette limite s'adapte intelligemment à la complexité de l'entrée (plus il y a de lettres, plus la suggestion est élevée), tout en laissant l'utilisateur libre de la modifier.

## 3. Installation et Utilisation

### Installation

Le projet n'a **aucune dépendance externe**. Il suffit d'avoir un interprète Python 3 installé sur votre machine.

1.  Clonez ou téléchargez ce dépôt.
2.  Assurez-vous que le fichier `dictionnaire_francais.txt` est présent dans le même répertoire.

### Utilisation

Pour lancer le programme, exécutez le script `anagramme.py` depuis votre terminal :

```bash
python anagramme.py
```

Le programme vous guidera ensuite à travers plusieurs étapes interactives :

1.  **Saisissez une expression** : Entrez le mot ou la phrase pour lequel vous voulez trouver des anagrammes (ex: `Endive braisée`).
2.  **Définissez la tolérance** : Entrez un nombre pour la différence maximale autorisée (`diff`).
    - `0` : Anagrammes parfaits uniquement.
    - `1` : Solutions avec une lettre de différence (ajoutée ou retirée).
    - `2` : Deux lettres de différence, etc.
3.  **Confirmez la limite de résultats** : Le programme vous suggérera une limite de résultats à afficher.
    - Appuyez sur `Entrée` pour accepter la suggestion.
    - Ou entrez un autre nombre pour définir votre propre limite.

### Exemple de Session

```
Entrez une expression (ex: 'Albert Einstein') : Endive braisée
Tolérance (différence max de lettres autorisée, 0 pour anagramme parfaite) : 1

Lettres à utiliser (12): aabdeeiinrsv
Limite de résultats suggérée : 109. Appuyez sur Entrée pour accepter ou entrez une autre valeur : 
Recherche en cours...

Solutions trouvées :

[ Différence = 1 ]
-> envie de baiser (ajouté: 'e' | diff: 1)
-> ... (autres résultats)
```

## 4. L'Algorithme Expliqué

L'efficacité du programme repose sur deux piliers : un prétraitement intelligent et un algorithme de recherche récursif optimisé.

### Étape 1 : Le Prétraitement du Dictionnaire

Avant la première recherche, le programme exécute une étape unique de prétraitement :

1.  Il lit le `dictionnaire_francais.txt`.
2.  Pour chaque mot, il crée une **forme canonique** : les lettres du mot, triées par ordre alphabétique (ex: "chien" -> "cehin").
3.  Il sauvegarde ces données dans un fichier `dictionnaire_calcule.json`. Ce fichier regroupe les mots par leur forme canonique.

Ce prétraitement permet de transformer une recherche d'anagrammes (un problème complexe) en une simple recherche par clé dans un dictionnaire.

### Étape 2 : La Recherche Récursive

Lorsque vous lancez une recherche, l'algorithme suit une approche récursive pour construire les anagrammes mot par mot.

Voici le pseudo-code qui illustre la logique :

```
fonction trouver_anagrammes(expression_actuelle, lettres_disponibles):

  // Condition de base : si l'expression est une solution valide, on l'ajoute
  si expression_actuelle est une anagramme acceptable:
    ajouter expression_actuelle aux résultats

  // Itération : on essaie d'ajouter un nouveau mot
  pour chaque mot dans le dictionnaire pré-calculé:

    // Optimisation 1 : Le mot est-il formable avec les lettres restantes ?
    si les lettres du mot sont contenues dans lettres_disponibles:

      // Appel récursif
      nouvelle_expression = expression_actuelle + " " + mot
      nouvelles_lettres_disponibles = lettres_disponibles - lettres_du_mot
      
      trouver_anagrammes(nouvelle_expression, nouvelles_lettres_disponibles)

    // Optimisation 2 (pour la tolérance) : Le mot est-il formable en "empruntant" des lettres ?
    si la différence de lettres entre le mot et les lettres_disponibles <= tolérance_restante:
      
      // Appel récursif avec la tolérance mise à jour
      ...
```

Cette approche explore l'arbre des possibilités, en "élaguant" les branches qui ne peuvent mener à aucune solution (grâce aux optimisations), ce qui la rend très performante.

### Étape 3 : La Suggestion de Limite via Sigmoïde

Pour éviter de proposer une limite de résultats fixe (ex: toujours 50), le programme utilise une fonction mathématique (une **courbe logistique** ou **sigmoïde**) pour calculer une suggestion adaptée.

- **Pourquoi une sigmoïde ?** Cette courbe modélise parfaitement le besoin : une croissance lente pour les mots courts, une accélération rapide pour les mots de complexité moyenne (là où les résultats deviennent intéressants), et un plateau pour les mots très longs (car afficher 5000 résultats n'est pas plus utile que d'en afficher 200).

Cela rend le programme plus "intelligent" et améliore l'expérience utilisateur sans sacrifier le contrôle, puisque la suggestion peut toujours être modifiée manuellement.
