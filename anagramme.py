import collections
import unicodedata
import sys

from typing import List, Set, Dict, NamedTuple

# --- Fichiers locaux ---
DICTIONARY_PATH = "liste_francais.txt"  # Chemin du dictionnaire local
LAST_EXPRESSION_CACHE = "derniere_expression.txt"  # Chemin du cache pour la dernière expression

# --- Constantes de configuration ---
MAX_SOLUTIONS = 10000  # Limite le nombre total de solutions à trouver pour éviter l'explosion combinatoire
MAX_RESULTS_TO_DISPLAY = 50  # Limite le nombre de solutions affichées à l'utilisateur

class Candidate(NamedTuple):
    """Structure pour stocker un mot candidat et ses données pré-calculées."""
    original: str
    counter: collections.Counter


def charger_dictionnaire_local(chemin_fichier: str) -> Set[str]:
    """Charge le dictionnaire depuis un fichier local (un mot par ligne)."""
    try:
        print(f"Chargement du dictionnaire depuis le fichier local ({chemin_fichier})...")
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            # On utilise un set pour des recherches rapides et pour éliminer les doublons
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
    # Utilise unicodedata pour une decomposition correcte des caracteres accentues
    # NFD = Normalization Form Decomposed (separe la lettre de son accent)
    texte_decompose = unicodedata.normalize('NFD', texte)
    # On ne garde que les caracteres qui ne sont pas des marques diacritiques (les accents)
    texte_sans_accent = "".join(c for c in texte_decompose if not unicodedata.combining(c))
    return "".join(c for c in texte_sans_accent if c.isalpha()).lower()


def charger_derniere_expression() -> str:
    """Charge la derniere expression depuis le cache, ou retourne une valeur par defaut."""
    try:
        with open(LAST_EXPRESSION_CACHE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except (FileNotFoundError, IOError):
        return "Mines antipersonnel"


def sauvegarder_derniere_expression(expr: str):
    """Sauvegarde l'expression donnee dans le fichier cache."""
    try:
        with open(LAST_EXPRESSION_CACHE, 'w', encoding='utf-8') as f:
            f.write(expr)
    except IOError as e:
        print(f"Impossible de sauvegarder la derniere expression : {e}", file=sys.stderr)


def trouver_anagrammes_approximatifs(expression_cible: str, dictionnaire_a_utiliser: Set[str], tolerance_requise: int) -> List[Dict]:
    """Fonction principale pour orchestrer la recherche d'anagrammes approximatifs."""
    print(f"\nAnalyse de l'expression avec une tolerance de {tolerance_requise} lettre(s)...")

    lettres_normalisees_cible = normaliser(expression_cible)
    if not lettres_normalisees_cible:
        print("L'expression fournie ne contient aucune lettre.")
        return []

    compteur_lettres_cible = collections.Counter(lettres_normalisees_cible)
    print(f"Lettres a utiliser : {''.join(sorted(lettres_normalisees_cible))}")

    candidats = []
    for mot in dictionnaire_a_utiliser:
        # FILTRE DE QUALITE : On ignore les mots trop courts qui polluent les resultats.
        if len(mot) < 3:
            continue

        mot_normalise = normaliser(mot)
        if not mot_normalise:
            continue

        compteur_mot = collections.Counter(mot_normalise)

        # FILTRE DE VALIDITE : On ne garde que les mots qui peuvent etre formes
        # avec les lettres de la cible. C'est la verification la plus importante.
        if any(compteur_mot[char] > compteur_lettres_cible[char] for char in compteur_mot):
            continue

        # Le mot est un candidat valide, on l'ajoute.
        candidats.append(Candidate(original=mot, counter=compteur_mot))

    # Le tri par longueur est une heuristique qui peut aider a trouver
    # des solutions plus rapidement dans certains cas.
    candidats.sort(key=lambda c: len(c.original), reverse=True)

    print(f"{len(candidats)} mots candidats trouves.")
    print("Lancement de la recherche approximative...")

    solutions = []  # On s'assure que la liste est bien vide avant de commencer.
    recherche_recursive_approximative(compteur_lettres_cible, candidats, [], solutions, tolerance_requise)

    # Trier les solutions pour un affichage plus propre
    # On trie par difference, puis par nombre de mots, puis alphabetiquement
    solutions.sort(key=lambda s: (s['diff'], len(s['mots']), s['solution_str']))

    return solutions


def recherche_recursive_approximative(
        compteur_lettres: collections.Counter,
        candidats: List[Candidate],
        chemin_actuel: List[str],
        solutions: List[Dict],
        tolerance_actuelle: int,
        start_index: int = 0
) -> None:
    """
    Fonction recursive qui cherche des combinaisons de mots de maniere exhaustive.
    """
    indentation = "  " * len(chemin_actuel)
    print(f"{indentation}RECURSION: Lettres restantes: {''.join(sorted(compteur_lettres.elements()))}, Chemin: {chemin_actuel}, Tolerance: {tolerance_actuelle}")
    sys.stdout.flush()

    # On a une solution potentielle. On l'enregistre si elle respecte la tolerance.
    lettres_restantes_compteur = sum(compteur_lettres.values())

    # Condition de sauvegarde de la solution.
    # Si la tolerance est 0, on cherche une correspondance exacte (reste = 0).
    # Sinon, on accepte un reste inferieur ou egal a la tolerance.
    is_solution_valid = (
        tolerance_actuelle == 0 and lettres_restantes_compteur == 0
    ) or (
        tolerance_actuelle > 0 and lettres_restantes_compteur <= tolerance_actuelle
    )

    # On ne sauvegarde la solution que si elle contient au moins un mot et est valide.
    if chemin_actuel and is_solution_valid:
        reste = ''.join(sorted(compteur_lettres.elements()))
        solution_str = ' '.join(chemin_actuel)
        print(f"{indentation}  SOLUTION TROUVEE: {solution_str} (reste: '{reste}' | diff: {lettres_restantes_compteur})")
        sys.stdout.flush()
        solutions.append({
            'solution_str': solution_str,
            'reste': reste,
            'diff': lettres_restantes_compteur,
            'mots': chemin_actuel
        })

    # Conditions d'arret pour eviter une recherche infinie ou trop profonde
    if len(solutions) >= MAX_SOLUTIONS or len(chemin_actuel) >= 8:
        return

    # Boucle de recherche
    for i in range(start_index, len(candidats)):
        candidat = candidats[i]
        print(f"{indentation}  TESTING CANDIDAT: {candidat.original}")
        sys.stdout.flush()

        # VERIFICATION : Le candidat peut-il etre forme avec les lettres restantes ?
        if all(compteur_lettres[char] >= candidat.counter[char] for char in candidat.counter):
            compteur_restant = compteur_lettres - candidat.counter

            # Le candidat est valide, on continue la recherche avec les lettres restantes.
            recherche_recursive_approximative(
                compteur_restant,
                candidats,
                chemin_actuel + [candidat.original],
                solutions,
                tolerance_actuelle,
                i + 1  # On continue avec les mots suivants pour eviter les doublons
            )


# --- Point d'entree du programme ---
if __name__ == "__main__":
    dictionnaire = charger_dictionnaire_local(DICTIONARY_PATH)

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

            # Permettre a l'utilisateur de definir la tolerance
            tolerance = 0
            try:
                tolerance_input = input(f"Entrez la tolerance (0 = parfaite, Entrer pour {tolerance}): ")
                if tolerance_input:
                    tolerance = int(tolerance_input)
            except ValueError:
                print(f"Entree invalide. Utilisation de la tolerance par defaut : {tolerance}")

            solutions_trouvees = trouver_anagrammes_approximatifs(expression, dictionnaire, tolerance)

            print("\n----------------- RESULTATS APPROXIMATIFS -----------------")
            if solutions_trouvees:
                total_solutions = len(solutions_trouvees)
                solutions_a_afficher = solutions_trouvees[:MAX_RESULTS_TO_DISPLAY]
                print(
                    f"{total_solutions} solution(s) trouvee(s). Affichage des {len(solutions_a_afficher)} meilleures (max: {MAX_SOLUTIONS}, tolerance: {tolerance}) :\n")
                for sol in solutions_a_afficher:
                    print(f"  -> {sol['solution_str']} (reste: '{sol['reste']}' | diff: {sol['diff']})")
            else:
                print("Aucune anagramme approximative n'a ete trouvee.")
            print("---------------------------------------------------------")

    except KeyboardInterrupt:
        print("\nRecherche interrompue par l'utilisateur.")
