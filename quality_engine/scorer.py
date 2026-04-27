# quality_engine/scorer.py
# Module 2 - Calcul du score de qualité des données

import pandas as pd

def calculer_score_qualite(df):
    """
    Calcule 4 indicateurs de qualité et un score global.
    Retourne un dictionnaire avec les résultats.
    """

    resultats = {}
    total_lignes = len(df)
    total_cellules = df.size  # lignes x colonnes

    # --- 1. COMPLETUDE ---
    # % de cellules qui ne sont PAS vides
    cellules_vides = df.isnull().sum().sum()
    completude = ((total_cellules - cellules_vides) / total_cellules) * 100
    resultats["completude"] = round(completude, 2)

    # --- 2. UNICITE ---
    # % de lignes qui ne sont PAS des doublons
    nb_doublons = df.duplicated().sum()
    unicite = ((total_lignes - nb_doublons) / total_lignes) * 100
    resultats["unicite"] = round(unicite, 2)

    # --- 3. VALIDITE ---
    # % de colonnes numériques qui n'ont pas de valeurs négatives anormales
    # (pour des données financières, on vérifie les colonnes de population)
    cols_population = [col for col in df.columns if 'pop' in col.lower()]
    if cols_population:
        valeurs_neg = (df[cols_population] < 0).sum().sum()
        total_pop_cellules = df[cols_population].size
        validite = ((total_pop_cellules - valeurs_neg) / total_pop_cellules) * 100
    else:
        validite = 100.0
    resultats["validite"] = round(validite, 2)

    # --- 4. SCORE GLOBAL ---
    # Moyenne des 3 indicateurs
    score_global = (completude + unicite + validite) / 3
    resultats["score_global"] = round(score_global, 2)

    return resultats


# --- EXECUTION ---
if __name__ == "__main__":
    print("Chargement du dataset...")
    df = pd.read_csv("data/communes.csv", sep=";", encoding="utf-8", low_memory=False)

    print("Calcul du score qualité...\n")
    scores = calculer_score_qualite(df)

    print("=" * 40)
    print("   RAPPORT QUALITE - openDQ")
    print("=" * 40)
    print(f"  Complétude  : {scores['completude']} %")
    print(f"  Unicité     : {scores['unicite']} %")
    print(f"  Validité    : {scores['validite']} %")
    print("-" * 40)
    print(f"  SCORE GLOBAL : {scores['score_global']} / 100")
    print("=" * 40)