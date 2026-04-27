# catalog/catalogue.py
# Catalogue de données - openDQ

import pandas as pd
import json

# --- DEFINITION DU CATALOGUE ---
catalogue = [
    {
        "colonne": "an",
        "nom_complet": "Année",
        "description": "Année d'exercice budgétaire",
        "type": "Entier",
        "exemple": "2022",
        "obligatoire": True,
        "regle_qualite": "Doit être entre 2000 et 2024"
    },
    {
        "colonne": "dep",
        "nom_complet": "Département",
        "description": "Code du département de la commune",
        "type": "Texte",
        "exemple": "75",
        "obligatoire": True,
        "regle_qualite": "Ne doit pas être vide"
    },
    {
        "colonne": "inom",
        "nom_complet": "Nom de la commune",
        "description": "Nom officiel de la commune",
        "type": "Texte",
        "exemple": "PARIS",
        "obligatoire": True,
        "regle_qualite": "Ne doit pas être vide"
    },
    {
        "colonne": "pop1",
        "nom_complet": "Population",
        "description": "Population municipale de la commune",
        "type": "Entier",
        "exemple": "2182174",
        "obligatoire": True,
        "regle_qualite": "Doit être supérieure à 0"
    },
    {
        "colonne": "prod",
        "nom_complet": "Produits de fonctionnement",
        "description": "Total des recettes de la section de fonctionnement (en milliers d'euros)",
        "type": "Décimal",
        "exemple": "7596960.58",
        "obligatoire": False,
        "regle_qualite": "Doit être positif"
    },
    {
        "colonne": "charge",
        "nom_complet": "Charges de fonctionnement",
        "description": "Total des dépenses de la section de fonctionnement (en milliers d'euros)",
        "type": "Décimal",
        "exemple": "7447929.54",
        "obligatoire": False,
        "regle_qualite": "Doit être positif"
    },
    {
        "colonne": "dette",
        "nom_complet": "Dette",
        "description": "Encours total de la dette de la commune (en milliers d'euros)",
        "type": "Décimal",
        "exemple": "9226931.46",
        "obligatoire": False,
        "regle_qualite": "Doit être positif ou nul"
    },
    {
        "colonne": "caf",
        "nom_complet": "Capacité d'autofinancement",
        "description": "Capacité de la commune à financer ses investissements sur ses propres ressources",
        "type": "Décimal",
        "exemple": "435289.19",
        "obligatoire": False,
        "regle_qualite": "Peut être négatif (commune en difficulté financière)"
    },
    {
        "colonne": "equip",
        "nom_complet": "Dépenses d'équipement",
        "description": "Dépenses d'investissement pour les équipements de la commune",
        "type": "Décimal",
        "exemple": "1627417.23",
        "obligatoire": False,
        "regle_qualite": "Doit être positif ou nul"
    },
    {
        "colonne": "subv",
        "nom_complet": "Subventions versées",
        "description": "Montant des subventions versées par la commune aux associations et organismes",
        "type": "Décimal",
        "exemple": "874221.67",
        "obligatoire": False,
        "regle_qualite": "Doit être positif ou nul"
    },
]

# --- AFFICHAGE ---
df_catalogue = pd.DataFrame(catalogue)

print("=" * 60)
print("   CATALOGUE DE DONNEES - openDQ")
print("=" * 60)
print(df_catalogue[["colonne", "nom_complet", "type", "obligatoire"]].to_string(index=False))

# --- SAUVEGARDE ---
# En CSV
df_catalogue.to_csv("catalog/catalogue.csv", index=False)

# En JSON
with open("catalog/catalogue.json", "w", encoding="utf-8") as f:
    json.dump(catalogue, f, ensure_ascii=False, indent=2)

print("\n✅ Catalogue sauvegardé en CSV et JSON dans catalog/")
print(f"   Nombre de colonnes documentées : {len(catalogue)}")