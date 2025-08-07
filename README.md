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

## 4. L'Algorithme Expliqué - principes généraux

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


## 5. Explication détaillée de l'algo

### Chercheur d'Anagrammes

Ce projet peut trouver des anagrammes parfaites et approximatives pour une expression donnée en français.

#### Fonctionnalités

*   **Anagrammes Parfaites et Approximatives :** Trouve des solutions qui utilisent toutes les lettres, ou des solutions qui ont un certain nombre de lettres en trop ou en moins (tolérance).
*   **Recherche Optimisée :** Utilise un dictionnaire "canonique" prétraité pour accélérer considérablement la recherche.
*   **Mise en Cache :** Met en cache le dictionnaire prétraité dans un fichier JSON pour un démarrage instantané lors des exécutions ultérieures.
*   **Limitation Dynamique des Résultats :** Suggère un nombre raisonnable de résultats à afficher en fonction de la complexité de l'expression d'entrée.
*   **Interface en Ligne de Commande Interactive :** Une interface conviviale pour entrer des expressions et définir les paramètres.

#### Comment Fonctionne l'Algorithme de Recherche Optimisée (L'Analogie LEGO)

Le cœur du programme est la fonction `recherche_optimisee_recursive`. Pour comprendre son fonctionnement, imaginez qu'il s'agit d'un ingénieur chargé d'un projet de construction LEGO complexe.

##### 1. Le Cahier des Charges (Les Paramètres Initiaux)

Imaginons un ingénieur recevant un cahier des charges précis pour démarrer sa mission : trouver les anagrammes. Il fait un appel initial à la fonction :

*   **La Boîte de LEGO (`compteur_lettres_cible`) :** C'est un `Counter` (un inventaire précis) de toutes les briques (lettres) disponibles pour le projet. C'est l'état initial de nos ressources.
*   **Le Catalogue de Pièces (`cles_canoniques`) :** C'est la liste de toutes les "pièces assemblées" autorisées (mots sous leur forme canonique, ex: `deimno` pour "monde"). Pour optimiser, ce catalogue est trié des pièces les plus grandes aux plus petites.
*   **La Marge d'Erreur (`tolerance_requise`) :** Le client final accepte que la construction finale n'utilise pas toutes les briques, ou même qu'elle en emprunte quelques-unes qui n'étaient pas dans la boîte de départ. C'est notre budget d'imperfection.
*   **Le Plan de Montage (`solutions_canoniques`) :** C'est une feuille blanche au début, sur laquelle l'ingénieur notera chaque plan de montage final qui respecte le cahier des charges.

##### 2. Le Processus de l'Ingénieur (Une Itération de la Fonction Récursive)

L'ingénieur (la fonction) a un processus de travail systématique. À chaque étape, il se pose les questions suivantes :

**Étape A : Le Cas de Base (Validation de la solution actuelle)**

> "Est-ce que l'assemblage que j'ai sur ma table (`chemin_actuel`) est déjà une solution valide ?"

Le code vérifie : `if sum(compteur_lettres_restantes.values()) <= tolerance_restante:`.
*   **Traduction :** "Le nombre de briques non utilisées dans ma boîte est-il inférieur ou égal à ma marge d'erreur restante ?" Si oui, c'est une solution acceptable ! L'ingénieur prend une photo du plan (`chemin_actuel`) et l'ajoute à son carnet de solutions (`solutions.append(chemin_actuel)`).
*   **Note :** Il ne s'arrête pas là. Une solution peut être un sous-ensemble d'une solution encore meilleure.

**Étape B : L'Exploration (La Boucle `for` et le Backtracking)**

> "Maintenant, quelle nouvelle pièce du catalogue puis-je ajouter à mon assemblage actuel ?"

C'est la boucle `for i in range(start_index, len(cles_canoniques)):`.

1.  **Il prend une pièce du catalogue** (`cle_canonique`).
2.  **Il évalue le coût :**
    *   Il compare les briques nécessaires pour cette pièce (`compteur_cle`) avec les briques qu'il lui reste (`compteur_lettres_restantes`).
    *   Le calcul `lettres_a_emprunter = compteur_cle - compteur_lettres_restantes` identifie les briques manquantes.
    *   Le `cout = sum(lettres_a_emprunter.values())` est le nombre de briques qu'il devrait "emprunter" (qui ne sont pas dans sa boîte actuelle).
3.  **Il prend une décision :**
    *   `if cout <= tolerance_restante:`
    *   **Traduction :** "Est-ce que le coût pour ajouter cette pièce est dans mon budget de tolérance restant ?"

**Étape C : La Délégation (L'Appel Récursif)**

> "Oui, je peux me permettre d'ajouter cette pièce. Je vais demander à un assistant de finir le travail à partir de là."

Si la décision est positive, l'ingénieur ne fait pas le travail lui-même. Il photocopie l'état actuel du projet et le confie à un assistant (un "clone", l'appel récursif) avec des instructions mises à jour :

*   `recherche_optimisee_recursive(...)` est appelé avec un **nouvel état du problème** :
    *   **Une boîte de LEGO plus petite (`nouveau_compteur_restant`) :** L'inventaire des briques après avoir construit la pièce actuelle.
    *   **Un budget de tolérance réduit (`nouvelle_tolerance_restante`) :** Le budget initial moins le coût de la pièce qu'il vient d'ajouter.
    *   **Un plan de montage mis à jour (`chemin_actuel + [cle_canonique]`) :** Le plan de l'assemblage en cours, avec la nouvelle pièce ajoutée.
    *   **Un catalogue restreint (`start_index = i`) :** C'est une optimisation cruciale. Il dit à son assistant : "Ne perds pas de temps à essayer les pièces que j'ai déjà évaluées ou écartées. Commence ton travail à partir de cette pièce dans le catalogue." Cela évite de tester les combinaisons `(A, B)` puis `(B, A)` et prévient les boucles infinies.

##### 3. La Fin de la Mission (Le Retour de la Récursion)

Quand un assistant (un appel récursif) a fini d'explorer toutes les possibilités qui lui ont été confiées (sa boucle `for` est terminée), il rend son rapport à son supérieur (la fonction retourne).

Le supérieur continue alors sa propre boucle `for`, en essayant la **pièce suivante** dans le catalogue. C'est le **backtracking** en action : en ne passant pas l'état modifié mais en reprenant simplement la boucle, on "annule" implicitement le choix précédent pour en explorer un autre.

Ce processus se poursuit jusqu'à ce que l'ingénieur initial ait exploré toutes les branches de possibilités qu'il pouvait initier. Le résultat final est la liste complète de tous les plans de montage valides qu'il a pu trouver.