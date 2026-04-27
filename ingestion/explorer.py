# ingestion/explorer.py
# Module 1 - Chargement et exploration du dataset

import pandas as pd

# --- 1. Chargement du fichier ---
print("Chargement du dataset...")
df = pd.read_csv("data/communes.csv", sep=";", encoding="utf-8", low_memory=False)

# --- 2. Premières infos ---
print("\n== DIMENSIONS DU DATASET ==")
print(f"Nombre de lignes    : {df.shape[0]}")
print(f"Nombre de colonnes  : {df.shape[1]}")

print("\n== APERCU DES 5 PREMIERES LIGNES ==")
print(df.head())

print("\n== NOM DES COLONNES ==")
print(df.columns.tolist())

print("\n== TYPES DE DONNEES ==")
print(df.dtypes)

print("\n== VALEURS MANQUANTES PAR COLONNE ==")
print(df.isnull().sum())