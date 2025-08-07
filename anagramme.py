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


# --- Structure de données Trie ---
class TrieNode:
    """Un nœud dans la structure de données Trie."""

    def __init__(self):
        self.enfants = {}
        self.mots = []


# --- Fonctions de Normalisation et Prétraitement ---

def normaliser_chaine(s):
    """Convertit une chaîne en minuscule et supprime les accents."""
    s_decomposed = unicodedata.normalize('NFD', s.lower())
    return "".join(c for c in s_decomposed if unicodedata.category(c) != 'Mn')


def construire_trie_canonique(chemin_dict_brut):
    """Construit un Trie à partir des mots du dictionnaire."""
    trie_racine = TrieNode()
    try:
        with open(chemin_dict_brut, 'r', encoding='utf-8') as f:
            mots = [ligne.strip() for ligne in f]
    except FileNotFoundError:
        print(f"\nERREUR CRITIQUE: Le fichier dictionnaire '{chemin_dict_brut}' est introuvable.")
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

    return trie_racine


def charger_dictionnaire_trie(chemin_dict_brut, chemin_cache):
    """Charge le Trie depuis le cache ou le construit si nécessaire."""
    if os.path.exists(chemin_cache):
        print("Chargement du dictionnaire canonique depuis le cache...")
        try:
            with open(chemin_cache, 'rb') as f_cache:
                trie_racine = pickle.load(f_cache)
            print("Chargement terminé.")
            return trie_racine
        except (pickle.UnpicklingError, EOFError) as e:
            print(f"Erreur de chargement du cache ({e}). Reconstruction du dictionnaire.")

    print("Le cache du dictionnaire n'a pas été trouvé ou est invalide.")
    trie_racine = construire_trie_canonique(chemin_dict_brut)
    print("Sauvegarde du dictionnaire canonique dans le cache pour les futurs lancements...")
    with open(chemin_cache, 'wb') as f_cache:
        pickle.dump(trie_racine, f_cache)
    print("Sauvegarde terminée.")
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
    """
    Le cœur de l'algorithme de recherche pour un compteur et une tolérance "en moins" donnés.
    """
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
    """
    Fonction principale qui orchestre la recherche avec tolérance symétrique.
    """
    expression_normalisee = normaliser_chaine(expression)
    lettres_canoniques = sorted(c for c in expression_normalisee if 'a' <= c <= 'z')
    compteur_lettres_initial = Counter(lettres_canoniques)

    solutions_globales = set()
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    # --- Calcul du nombre total de tâches pour la barre de progression ---
    total_taches = 0
    for k_plus in range(tolerance + 1):
        total_taches += math.comb(len(alphabet) + k_plus - 1, k_plus)

    taches_faites = 0
    print(f"\nLancement de la recherche (Tolérance symétrique de {tolerance})...")
    afficher_barre_progression(0, total_taches, prefixe='Recherche:', suffixe='En cours', longueur=40)

    # --- Boucle principale pour la tolérance symétrique ---
    for k_plus in range(tolerance + 1):
        tolerance_moins = tolerance - k_plus

        # Itère sur toutes les combinaisons de 'k_plus' lettres à ajouter
        for combo in itertools.combinations_with_replacement(alphabet, k_plus):
            compteur_modifie = compteur_lettres_initial.copy()
            for char_to_add in combo:
                compteur_modifie[char_to_add] += 1

            # Lance la recherche pour cette configuration
            solutions_trouvees = _recherche_anagrammes_interne(compteur_modifie, tolerance_moins, trie_racine)
            solutions_globales.update(solutions_trouvees)

            taches_faites += 1
            afficher_barre_progression(taches_faites, total_taches, prefixe='Recherche:', suffixe='En cours',
                                       longueur=40)

    if total_taches > 0: print()

    # --- Formatage final des résultats ---
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


# --- Fonctions Utilitaires ---
def calculer_limite_affichage(nombre_lettres):
    """Calcule le nombre de résultats à afficher."""
    L = 200;
    k = 0.4;
    n0 = 13
    limite = L / (1 + math.exp(-k * (nombre_lettres - n0)))
    return max(20, int(round(limite)))


def afficher_barre_progression(iteration, total, prefixe='', suffixe='', longueur=50):
    """Affiche une barre de progression dans le terminal."""
    if total == 0: total = 1
    pourcentage = (iteration / float(total)) * 100
    nb_barres_pleines = int(longueur * iteration // total)
    barre = '█' * nb_barres_pleines + '-' * (longueur - nb_barres_pleines)
    sys.stdout.write(f'\r{prefixe} |{barre}| {pourcentage:.2f}% {suffixe} ')
    sys.stdout.flush()


# --- Point d'Entrée Principal ---
if __name__ == "__main__":
    dictionnaire_trie = charger_dictionnaire_trie(DICTIONARY_PATH, CANONICAL_DICT_CACHE_PATH)

    while True:
        print("\n" + "=" * 50)
        expression_entree = input("Entrez une expression (ou 'q' pour quitter): ")
        if expression_entree.lower() == 'q': break

        lettres_utiles = [c for c in normaliser_chaine(expression_entree) if 'a' <= c <= 'z']
        if not lettres_utiles:
            print("Veuillez entrer une expression contenant des lettres.")
            continue

        try:
            tolerance_suggeree = 1 if len(lettres_utiles) > 8 else 0
            tolerance = int(
                input(f"Entrez la tolérance (symétrique, suggéré: {tolerance_suggeree}): ") or tolerance_suggeree)
        except ValueError:
            tolerance = tolerance_suggeree
            print(f"Entrée invalide. Utilisation de la tolérance par défaut: {tolerance}")

        limite_suggeree = calculer_limite_affichage(len(lettres_utiles))
        try:
            limite_affichage = int(input(f"Nombre max de résultats (suggéré: {limite_suggeree}): ") or limite_suggeree)
        except ValueError:
            limite_affichage = limite_suggeree
            print(f"Entrée invalide. Utilisation de la limite par défaut: {limite_affichage}")

        resultats_anagrammes = trouver_anagrammes_trie(expression_entree, tolerance, dictionnaire_trie)

        # Trier les résultats par différence totale croissante
        resultats_anagrammes.sort(key=lambda x: x['nb_moins'] + x['nb_plus'])

        print("\n" + "-" * 17 + " RÉSULTATS " + "-" * 17)
        if resultats_anagrammes:
            for i, anag_info in enumerate(resultats_anagrammes):
                if i >= limite_affichage:
                    print(f"\n... et {len(resultats_anagrammes) - limite_affichage} autre(s) résultat(s).")
                    break

                solution_str = " ".join(anag_info['solution'])
                longueur_str = f"{anag_info['longueur']} lettres"

                # Construction de la chaîne de différence
                diff_parts = []
                if anag_info['nb_plus'] > 0:
                    diff_parts.append(f"+{anag_info['nb_plus']} ({anag_info['str_plus']})")
                if anag_info['nb_moins'] > 0:
                    diff_parts.append(f"-{anag_info['nb_moins']} ({anag_info['str_moins']})")

                if not diff_parts:
                    print(f"{solution_str} ({longueur_str}, anagramme parfaite)")
                else:
                    diff_str = ", ".join(diff_parts)
                    print(f"{solution_str} ({longueur_str}, diff: {diff_str})")
        else:
            print("Aucune anagramme n'a été trouvée.")
        print("-" * (45))