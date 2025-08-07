import collections
import unicodedata
import sys
import itertools
import math

from typing import List, Set, Dict, NamedTuple

# --- Fichiers locaux ---
DICTIONARY_PATH = "liste_francais.txt"  # Chemin du dictionnaire local
LAST_EXPRESSION_CACHE = "derniere_expression.txt"  # Chemin du cache pour la dernière expression

class Candidate(NamedTuple):
    """Structure pour stocker un mot candidat et ses données pré-calculées."""
    original: str
    counter: collections.Counter


def charger_dictionnaire_local(chemin_fichier: str) -> Set[str]:
    """Charge le dictionnaire depuis un fichier local (un mot par ligne)."""
    try:
        print(f"Chargement du dictionnaire depuis le fichier local ({chemin_fichier})...")
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            mots = set(f.read().splitlines())
        print(f"Dictionnaire charge avec {len(mots)} mots.")
        return mots
    except FileNotFoundError:
        print(f"ERREUR : Le fichier dictionnaire '{chemin_fichier}' est introuvable.", file=sys.stderr)
        print("Veuillez vous assurer que le fichier se trouve dans le meme repertoire que le programme.", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"ERREUR : Impossible de lire le fichier dictionnaire '{chemin_fichier}'. {e}", file=sys.stderr)
        sys.exit(1)


def normaliser(texte: str) -> str:
    """Nettoie et normalise une chaine de caracteres en supprimant les accents."""
    texte_decompose = unicodedata.normalize('NFD', texte)
    texte_sans_accent = "".join(c for c in texte_decompose if not unicodedata.combining(c))
    return "".join(c for c in texte_sans_accent if c.isalpha()).lower()


def pretraiter_dictionnaire(mots: Set[str]) -> Dict[str, List[str]]:
    """Prétraite le dictionnaire pour regrouper les mots par leur forme canonique."""
    print("Prétraitement du dictionnaire pour la recherche optimisée...")
    canoniques = collections.defaultdict(list)
    for mot in mots:
        mot_normalise = normaliser(mot)
        if len(mot_normalise) >= 2:
            forme_canonique = "".join(sorted(mot_normalise))
            canoniques[forme_canonique].append(mot)
    print(f"{len(canoniques)} formes canoniques uniques trouvées.")
    return canoniques


def charger_derniere_expression() -> str:
    """Charge la derniere expression depuis le cache, ou retourne une valeur par defaut."""
    try:
        with open(LAST_EXPRESSION_CACHE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except (FileNotFoundError, IOError):
        return "L'Origine du monde, Gustave Courbet"


def sauvegarder_derniere_expression(expr: str):
    """Sauvegarde l'expression donnee dans le fichier cache."""
    try:
        with open(LAST_EXPRESSION_CACHE, 'w', encoding='utf-8') as f:
            f.write(expr)
    except IOError as e:
        print(f"Impossible de sauvegarder la derniere expression : {e}", file=sys.stderr)


def calculer_limite_affichage(nombre_lettres: int) -> int:
    """
    Calcule le nombre de résultats à afficher en utilisant une courbe logistique.
    Cela permet une augmentation fluide de la limite en fonction de la complexité.
    """
    L = 200  # Limite maximale de résultats (le plafond de la courbe)
    k = 0.4  # Pente de la courbe (à quel point la transition est rapide)
    n0 = 13  # Point central de la croissance (le nombre de lettres où la limite est L/2)

    # Formule de la fonction logistique
    try:
        limite = L / (1 + math.exp(-k * (nombre_lettres - n0)))
    except OverflowError:
        # Si (nombre_lettres - n0) est très grand et négatif, exp() peut déborder.
        # Dans ce cas, la limite est effectivement 0, mais nous la plafonnons à notre minimum.
        limite = 0

    # On arrondit à l'entier le plus proche et on s'assure de retourner au moins une valeur minimale.
    return max(20, int(round(limite)))


# --- NOUVELLE APPROCHE OPTIMISÉE ---

def generer_combinaisons_depuis_canoniques(
    solution_canonique: List[str],
    dict_canonique: Dict[str, List[str]]
) -> List[str]:
    """Génère toutes les phrases possibles à partir d'une liste de formes canoniques."""
    listes_de_mots = [dict_canonique[cle] for cle in solution_canonique]
    combinaisons_de_mots = list(itertools.product(*listes_de_mots))
    return [" ".join(combo) for combo in combinaisons_de_mots]


def recherche_optimisee_recursive(
    compteur_lettres_restantes: collections.Counter,
    cles_canoniques: List[str],
    solutions: List[List[str]],
    tolerance_restante: int,
    chemin_actuel: List[str] = [],
    start_index: int = 0
):
    """Nouvelle recherche récursive qui gère la tolérance."""
    lettres_non_utilisees = sum(compteur_lettres_restantes.values())
    if lettres_non_utilisees <= tolerance_restante:
        solutions.append(chemin_actuel)

    for i in range(start_index, len(cles_canoniques)):
        cle_canonique = cles_canoniques[i]
        compteur_cle = collections.Counter(cle_canonique)

        lettres_a_emprunter = compteur_cle - compteur_lettres_restantes
        cout = sum(lettres_a_emprunter.values())

        if cout <= tolerance_restante:
            nouveau_compteur_restant = compteur_lettres_restantes - compteur_cle
            nouvelle_tolerance_restante = tolerance_restante - cout
            
            recherche_optimisee_recursive(
                nouveau_compteur_restant,
                cles_canoniques,
                solutions,
                nouvelle_tolerance_restante,
                chemin_actuel + [cle_canonique],
                i
            )


def trouver_anagrammes_optimises(
    expression_cible: str,
    dict_canonique: Dict[str, List[str]],
    tolerance_requise: int
) -> List[Dict]:
    """Fonction principale qui utilise le dictionnaire prétraité et gère la tolérance."""
    print(f"\nLancement de la recherche OPTIMISÉE avec une tolérance de {tolerance_requise}...")
    lettres_normalisees_cible = normaliser(expression_cible)
    compteur_lettres_cible = collections.Counter(lettres_normalisees_cible)
    print(f"Lettres à utiliser ({len(lettres_normalisees_cible)}): {''.join(sorted(lettres_normalisees_cible))}")

    cles_canoniques = sorted(list(dict_canonique.keys()), key=len, reverse=True)
    print(f"{len(cles_canoniques)} formes canoniques candidates pour la recherche.")

    solutions_canoniques = []
    recherche_optimisee_recursive(
        compteur_lettres_cible,
        cles_canoniques,
        solutions_canoniques,
        tolerance_requise,
        chemin_actuel=[],
        start_index=0
    )

    resultats_finaux = []
    solutions_uniques = set()

    for sol_canonique in solutions_canoniques:
        lettres_utilisees = collections.Counter("".join(sol_canonique))
        
        diff_counter = (compteur_lettres_cible - lettres_utilisees) + (lettres_utilisees - compteur_lettres_cible)
        diff = sum(diff_counter.values())

        if diff <= tolerance_requise:
            combinaisons = generer_combinaisons_depuis_canoniques(sol_canonique, dict_canonique)
            for combo_str in combinaisons:
                if combo_str not in solutions_uniques:
                    solutions_uniques.add(combo_str)
                    reste_reel = compteur_lettres_cible - lettres_utilisees
                    lettres_ajoutees = lettres_utilisees - compteur_lettres_cible
                    resultats_finaux.append({
                        'solution_str': combo_str,
                        'reste': "".join(sorted(reste_reel.elements())),
                        'ajoute': "".join(sorted(lettres_ajoutees.elements())),
                        'diff': diff,
                        'mots': combo_str.split()
                    })

    resultats_finaux.sort(key=lambda s: (s['diff'], len(s['mots']), s['solution_str']))
    return resultats_finaux


# --- Point d'entree du programme ---
if __name__ == "__main__":
    dictionnaire = charger_dictionnaire_local(DICTIONARY_PATH)
    dictionnaire_canonique = pretraiter_dictionnaire(dictionnaire)

    try:
        while True:
            # 1. Charger la derniere expression et la proposer
            expression_par_defaut = charger_derniere_expression()
            print("\n----------------------------------------------------")
            expression = input(
                f"Entrez une expression (ou appuyez sur Entrer pour utiliser '{expression_par_defaut}'): ")
            if not expression:
                expression = expression_par_defaut
            else:
                sauvegarder_derniere_expression(expression)

            # 2. Permettre a l'utilisateur de definir la tolerance
            tolerance = 1
            try:
                tolerance_input = input(f"Entrez la tolerance (0 = parfaite, Entrer pour {tolerance}): ")
                if tolerance_input:
                    tolerance = int(tolerance_input)
            except ValueError:
                print(f"Entree invalide. Utilisation de la tolerance par defaut : {tolerance}")

            # 3. Calculer, proposer et définir la limite d'affichage
            lettres_pour_calcul = normaliser(expression)
            limite_suggeree = calculer_limite_affichage(len(lettres_pour_calcul))
            limite_affichage = limite_suggeree
            try:
                limite_input = input(f"Limite de résultats suggérée : {limite_suggeree}. Appuyez sur Entrée pour accepter ou entrez une autre valeur : ")
                if limite_input:
                    limite_affichage = int(limite_input)
            except ValueError:
                print(f"Entrée invalide. Utilisation de la limite suggérée : {limite_affichage}")


            solutions_trouvees = trouver_anagrammes_optimises(expression, dictionnaire_canonique, tolerance)

            print("\n----------------- RESULTATS -----------------")
            if solutions_trouvees:
                total_solutions = len(solutions_trouvees)
                print(f"{total_solutions} solution(s) trouvee(s) (tolerance: {tolerance}).")

                grouped_solutions = collections.defaultdict(list)
                for sol in solutions_trouvees:
                    grouped_solutions[sol['diff']].append(sol)
                
                results_shown = 0
                limit_reached = False

                for diff_val in sorted(grouped_solutions.keys()):
                    if limit_reached:
                        break
                    
                    solutions_in_group = grouped_solutions[diff_val]
                    if results_shown < limite_affichage:
                        print(f"\n--- Solutions avec diff: {diff_val} ---")

                    for sol in solutions_in_group:
                        if results_shown >= limite_affichage:
                            limit_reached = True
                            break
                        
                        details = []
                        if sol['reste']:
                            details.append(f"reste: '{sol['reste']}'")
                        if sol['ajoute']:
                            details.append(f"ajouté: '{sol['ajoute']}'")
                        details.append(f"diff: {sol['diff']}")
                        
                        details_str = " | ".join(details)
                        print(f"  -> {sol['solution_str']} ({details_str})")
                        results_shown += 1
                
                if limit_reached:
                    print(f"\nLimite d'affichage de {limite_affichage} résultats atteinte.")

            else:
                print("Aucune anagramme n'a ete trouvee.")
            print("---------------------------------------------------------")

    except KeyboardInterrupt:
        print("\nRecherche interrompue par l'utilisateur.")
