# Anagrammes : Un Chercheur d'Anagrammes Intelligent

## 1. Objectif du Projet

Ce projet est un programme en Python capable de trouver des anagrammes pour une expression donnée (un ou plusieurs mots). Il ne se contente pas de trouver des anagrammes parfaits ; il peut également identifier des **solutions approximatives** en ajoutant ou en retirant des lettres, ce qui le rend beaucoup plus flexible et créatif.

Le programme est conçu pour être à la fois performant, grâce à un dictionnaire prétraité et mis en cache, et ergonomique, avec une interface interactive qui guide l'utilisateur.

## 2. Fonctionnalités

- **Anagrammes Multi-mots** : Trouvez des anagrammes composés de plusieurs mots du dictionnaire.
- **Tolérance aux Imperfections (`diff`)** : Spécifiez un niveau de tolérance pour trouver des solutions qui ne sont pas des anagrammes parfaits.
- **Dictionnaire Canonique Persistant** : Pour des recherches et des démarrages quasi-instantanés, le programme prétraite le dictionnaire une seule fois et le sauvegarde dans un fichier cache.
- **Affichage Détaillé** : Les résultats indiquent clairement les lettres non utilisées (`reste`), les lettres ajoutées (`ajouté`) et la différence totale (`diff`).
- **Limite de Résultats Intelligente** : Le programme suggère une limite de résultats à afficher en utilisant une **courbe de croissance logistique (sigmoïde)**. Cette limite s'adapte intelligemment à la complexité de l'entrée, tout en laissant l'utilisateur libre de la modifier.

## 3. Installation et Utilisation

### Installation

Le projet n'a **aucune dépendance externe**. Il suffit d'avoir un interprète Python 3 installé sur votre machine.

1.  Clonez ou téléchargez ce dépôt.
2.  Assurez-vous que le fichier `liste_francais.txt` est présent dans le même répertoire.

### Utilisation

Pour lancer le programme, exécutez le script `anagramme.py` depuis votre terminal :

```bash
python anagramme.py
```

Le programme vous guidera ensuite à travers plusieurs étapes interactives :

1.  **Saisissez une expression** : Entrez le mot ou la phrase pour lequel vous voulez trouver des anagrammes (ex: `Endive braisée`).
2.  **Définissez la tolérance** : Entrez un nombre pour la différence maximale autorisée (`diff`).
3.  **Confirmez la limite de résultats** : Le programme vous suggérera une limite de résultats à afficher. Acceptez-la ou définissez la vôtre.

**Note sur le premier lancement :** Lors de la toute première exécution, le programme va créer un fichier nommé `dictionnaire_canonique.json`. Ce fichier est un **cache** contenant le dictionnaire pré-traité. Sa création peut prendre quelques secondes, mais il accélérera considérablement tous les lancements futurs du programme.

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

L'efficacité du programme repose sur deux piliers : un prétraitement intelligent mis en cache et un algorithme de recherche récursif optimisé.

### Étape 1 : Le Prétraitement et la Mise en Cache du Dictionnaire

L'efficacité du programme repose sur une optimisation cruciale : le prétraitement du dictionnaire est effectué **une seule fois**.

1.  Lors du tout premier lancement, le programme lit le `liste_francais.txt`.
2.  Pour chaque mot, il crée une **forme canonique** : les lettres du mot, triées par ordre alphabétique (ex: "chien" -> "cehin").
3.  Ce dictionnaire de formes canoniques est ensuite sauvegardé dans un fichier cache : `dictionnaire_canonique.json`.

Lors de toutes les exécutions suivantes, le programme charge directement ce cache, ce qui rend le démarrage quasi-instantané. Cette approche transforme une recherche d'anagrammes (un problème complexe) en une simple recherche par clé dans un dictionnaire déjà prêt.

### Étape 2 : La Recherche Récursive

Lorsque vous lancez une recherche, l'algorithme suit une approche récursive pour construire les anagrammes mot par mot. Le pseudo-code illustre cette logique :

```
fonction trouver_anagrammes(expression_actuelle, lettres_disponibles):

  // On essaie d'ajouter un nouveau mot
  pour chaque mot dans le dictionnaire canonique:

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

Cette approche explore l'arbre des possibilités, en "élaguant" les branches qui ne peuvent mener à aucune solution, ce qui la rend très performante.

### Étape 3 : La Suggestion de Limite via Sigmoïde

Pour éviter de proposer une limite de résultats fixe, le programme utilise une fonction mathématique (une **courbe logistique** ou **sigmoïde**) pour calculer une suggestion adaptée. Cette courbe modélise parfaitement le besoin : une croissance lente pour les mots courts, une accélération rapide pour les mots de complexité moyenne, et un plateau pour les mots très longs. Cela rend le programme plus "intelligent" et améliore l'expérience utilisateur.
