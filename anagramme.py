import json
import math
import pickle
import sys
import unicodedata
from collections import Counter
import os
import itertools

# --- Constantes ---
DICTIONARY_PATH = "dictionnaire.txt"
CANONICAL_DICT_CACHE_PATH = "dictionnaire_canonique.pkl"


# --- Classes et Fonctions Utilitaires ---

class Colors:
    """Classe pour les codes de couleur ANSI pour le terminal."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    GRAY = '\033[90m'  # Couleur pour les résultats nuls
    BOLD = '\033[1m'
    ENDC = '\033[0m'


class TrieNode:
    """Un nœud dans la structure de données Trie."""

    def __init__(self):
        self.enfants = {}
        self.mots = []


def normaliser_chaine(s):
    """Convertit une chaîne en minuscule et supprime les accents."""
    s_decomposed = unicodedata.normalize('NFD', s.lower())
    return "".join(c for c in s_decomposed if unicodedata.category(c) != 'Mn')


def afficher_barre_progression(iteration, total, prefixe='', suffixe='', longueur=50):
    """Affiche une barre de progression dans le terminal."""
    if total == 0: total = 1
    pourcentage = (iteration / float(total)) * 100
    nb_barres_pleines = int(longueur * iteration // total)
    barre = '█' * nb_barres_pleines + '-' * (longueur - nb_barres_pleines)
    sys.stdout.write(f'\r{prefixe} |{barre}| {pourcentage:.2f}% {suffixe} ')
    sys.stdout.flush()


# --- Fonctions de Prétraitement et de Cache ---

def construire_trie_canonique(chemin_dict_brut):
    """Construit un Trie à partir des mots du dictionnaire."""
    trie_racine = TrieNode()
    try:
        with open(chemin_dict_brut, 'r', encoding='utf-8') as f:
            mots = [ligne.strip() for ligne in f]
    except FileNotFoundError:
        print(
            f"\n{Colors.BOLD}ERREUR CRITIQUE:{Colors.ENDC} Le fichier dictionnaire '{chemin_dict_brut}' est introuvable.")
        print("Veuillez créer ce fichier et y ajouter une liste de mots.")
        sys.exit(1)

    total_mots = len(mots)
    afficher_barre_progression(0, total_mots, prefixe='Construction du Trie:', suffixe='Complet', longueur=40)

    for i, mot in enumerate(mots):
        forme_canonique = "".join(sorted(normaliser_chaine(mot)))
        if not forme_canonique: continue
        node = trie_racine
        for char in forme_canonique:
            if char not in node.enfants:
                node.enfants[char] = TrieNode()
            node = node.enfants[char]
        node.mots.append(mot)
        if (i + 1) % 1000 == 0 or (i + 1) == total_mots:
            afficher_barre_progression(i + 1, total_mots, prefixe='Construction du Trie:', suffixe='Complet',
                                       longueur=40)

    print()  # Saut de ligne après la barre
    return trie_racine


def charger_dictionnaire_trie(chemin_dict_brut, chemin_cache):
    """Charge le Trie depuis le cache ou le construit si nécessaire."""
    if os.path.exists(chemin_cache):
        print("Chargement du dictionnaire canonique depuis le cache...")
        try:
            with open(chemin_cache, 'rb') as f_cache:
                trie_racine = pickle.load(f_cache)
            print(f"{Colors.GREEN}Chargement terminé.{Colors.ENDC}")
            return trie_racine
        except (pickle.UnpicklingError, EOFError) as e:
            print(f"{Colors.YELLOW}Erreur de chargement du cache ({e}). Reconstruction du dictionnaire.{Colors.ENDC}")

    print("Le cache du dictionnaire n'a pas été trouvé ou est invalide.")
    trie_racine = construire_trie_canonique(chemin_dict_brut)
    print("Sauvegarde du dictionnaire canonique dans le cache...")
    with open(chemin_cache, 'wb') as f_cache:
        pickle.dump(trie_racine, f_cache)
    print(f"{Colors.GREEN}Sauvegarde terminée.{Colors.ENDC}")
    return trie_racine


# --- Algorithme de Recherche d'Anagrammes (Tolérance Symétrique) ---

def _chercher_mots_dans_trie(node, compteur):
    """Utilitaire qui parcourt le trie et retourne tous les mots faisables à partir d'un compteur."""
    resultats = []
    if node.mots:
        for mot in node.mots:
            resultats.append((mot, compteur.copy()))
    for char, enfant_node in node.enfants.items():
        if compteur[char] > 0:
            compteur[char] -= 1
            resultats.extend(_chercher_mots_dans_trie(enfant_node, compteur))
            compteur[char] += 1  # Backtrack
    return resultats


def _recherche_anagrammes_interne(compteur_lettres, tolerance_moins, trie_racine):
    """Le cœur de l'algorithme de recherche pour un compteur et une tolérance "en moins" donnés."""
    solutions_locales = set()

    def recherche_recursive(compteur_actuel, chemin_actuel):
        mots_possibles = _chercher_mots_dans_trie(trie_racine, compteur_actuel)
        for mot, compteur_apres_mot in mots_possibles:
            if chemin_actuel and mot < chemin_actuel[-1]:
                continue
            nouveau_chemin = chemin_actuel + [mot]
            solution_triee = tuple(sorted(nouveau_chemin))
            lettres_restantes = sum(compteur_apres_mot.values())
            if lettres_restantes <= tolerance_moins:
                solutions_locales.add(solution_triee)
            if lettres_restantes > 1:
                recherche_recursive(compteur_apres_mot, nouveau_chemin)

    recherche_recursive(compteur_lettres, [])
    return solutions_locales


def trouver_anagrammes_trie(expression, tolerance, trie_racine):
    """Fonction principale qui orchestre la recherche avec tolérance symétrique."""
    expression_normalisee = normaliser_chaine(expression)
    lettres_canoniques = sorted(c for c in expression_normalisee if 'a' <= c <= 'z')
    compteur_lettres_initial = Counter(lettres_canoniques)

    solutions_globales = set()
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    total_taches = sum(math.comb(len(alphabet) + k - 1, k) for k in range(tolerance + 1))
    taches_faites = 0

    print(f"\nLancement de la recherche (Tolérance symétrique de {tolerance})...")
    afficher_barre_progression(0, total_taches, prefixe='Recherche:', suffixe='En cours', longueur=40)

    for k_plus in range(tolerance + 1):
        tolerance_moins = tolerance - k_plus
        for combo in itertools.combinations_with_replacement(alphabet, k_plus):
            compteur_modifie = compteur_lettres_initial.copy()
            compteur_modifie.update(combo)

            solutions_trouvees = _recherche_anagrammes_interne(compteur_modifie, tolerance_moins, trie_racine)
            solutions_globales.update(solutions_trouvees)

            taches_faites += 1
            afficher_barre_progression(taches_faites, total_taches, prefixe='Recherche:', suffixe='En cours',
                                       longueur=40)

    if total_taches > 0: print()

    resultats_formates = []
    for sol in solutions_globales:
        lettres_sol_normalisees = normaliser_chaine("".join(sol))
        compteur_sol = Counter(lettres_sol_normalisees)

        lettres_en_moins = compteur_lettres_initial - compteur_sol
        lettres_en_plus = compteur_sol - compteur_lettres_initial

        resultats_formates.append({
            'solution': list(sol),
            'nb_moins': sum(lettres_en_moins.values()),
            'str_moins': "".join(sorted(lettres_en_moins.elements())),
            'nb_plus': sum(lettres_en_plus.values()),
            'str_plus': "".join(sorted(lettres_en_plus.elements())),
            'longueur': len(lettres_sol_normalisees)
        })

    return resultats_formates


# --- Point d'Entrée Principal ---
if __name__ == "__main__":
    dictionnaire_trie = charger_dictionnaire_trie(DICTIONARY_PATH, CANONICAL_DICT_CACHE_PATH)

    while True:  # Boucle principale pour les nouvelles expressions
        expression_actuelle = input(f"\n{Colors.BOLD}Entrez une expression (ou 'q' pour quitter):{Colors.ENDC} ")

        if expression_actuelle.lower() == 'q':
            break

        lettres_utiles = [c for c in normaliser_chaine(expression_actuelle) if 'a' <= c <= 'z']
        if not lettres_utiles:
            print("Veuillez entrer une expression contenant des lettres.")
            continue

        try:
            tolerance_suggeree = 1 if len(lettres_utiles) > 8 else 0
            tolerance_input = input(
                f"Entrez la tolérance pour \"{expression_actuelle}\" (suggéré: {tolerance_suggeree}): ")
            if tolerance_input == "":
                tolerance = tolerance_suggeree
            else:
                tolerance = int(tolerance_input)
        except ValueError:
            tolerance = tolerance_suggeree
            print(f"Entrée invalide. Utilisation de la tolérance par défaut: {tolerance}")

        resultats_anagrammes = trouver_anagrammes_trie(expression_actuelle, tolerance, dictionnaire_trie)

        # 1. Grouper les résultats
        grouped_results = {}
        for res in resultats_anagrammes:
            total_diff = res['nb_plus'] + res['nb_moins']
            if total_diff not in grouped_results:
                grouped_results[total_diff] = []
            grouped_results[total_diff].append(res)

        # 2. Boucle d'interaction pour l'exploration des résultats
        while True:
            print("\n" + "=" * 17 + " RÉSUMÉ DES RÉSULTATS " + "=" * 17)
            for diff_level in range(tolerance + 1):
                count = len(grouped_results.get(diff_level, []))

                color = Colors.BLUE
                if count == 0:
                    color = Colors.GRAY
                elif diff_level == 0:
                    color = Colors.GREEN
                elif diff_level == 1:
                    color = Colors.YELLOW

                print(f"{color}--- Différence {diff_level}: {Colors.BOLD}{count}{color} résultat(s){Colors.ENDC}")

            try:
                choix = input(f"\nQuelle différence afficher ? ('n' pour nouvelle recherche, 'q' pour quitter): ")
                if choix.lower() == 'q':
                    sys.exit()
                if choix.lower() == 'n':
                    break

                choix_diff = int(choix)
                if choix_diff not in grouped_results:
                    print(f"{Colors.YELLOW}Niveau de différence invalide ou sans résultats.{Colors.ENDC}")
                    continue

            except ValueError:
                print(f"{Colors.YELLOW}Veuillez entrer un nombre, 'n' ou 'q'.{Colors.ENDC}")
                continue

            # 3. Affichage paginé du groupe choisi
            lignes_a_imprimer = []
            results_in_group = sorted(grouped_results[choix_diff], key=lambda x: " ".join(x['solution']))
            total_in_group = len(results_in_group)

            for i, anag_info in enumerate(results_in_group):
                solution_str = " ".join(anag_info['solution'])
                counter_str = f"[{i + 1}/{total_in_group}]"

                # Construction de la ligne de résultat en une seule fois
                line = f'  {counter_str} "{Colors.GREEN}{solution_str}{Colors.ENDC}"'

                # Ajout des informations sur les lettres
                diff_parts = []
                if anag_info['nb_plus'] > 0:
                    diff_parts.append(f"lettres ajoutées: {Colors.GREEN}{anag_info['str_plus']}{Colors.ENDC}")
                if anag_info['nb_moins'] > 0:
                    diff_parts.append(f"lettres retirées: {Colors.YELLOW}{anag_info['str_moins']}{Colors.ENDC}")

                if diff_parts:
                    diff_str = ", ".join(diff_parts)
                    line += f" ({diff_str})"
                
                lignes_a_imprimer.append(line)

            page_size = 25
            start_index = 0
            print("-" * 45)
            while start_index < len(lignes_a_imprimer):
                end_index = min(start_index + page_size, len(lignes_a_imprimer))
                for i in range(start_index, end_index):
                    print(lignes_a_imprimer[i])

                start_index = end_index
                if start_index < len(lignes_a_imprimer):
                    voir_plus = input(
                        f"\n... {len(lignes_a_imprimer) - start_index} ligne(s) restante(s). Appuyez sur Entrée pour continuer, ou 'n' pour revenir au sommaire: ")
                    if voir_plus.lower() == 'n':
                        break
            print("-" * 45)
