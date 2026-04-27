# quality_engine/anomaly_detector.py
# Module 3 - Détection d'anomalies par IA (Isolation Forest)

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# --- 1. Chargement ---
print("Chargement du dataset...")
df = pd.read_csv("data/communes.csv", sep=";", encoding="utf-8", low_memory=False)

# --- 2. Sélection des colonnes financières clés ---
# On choisit des indicateurs financiers importants pour une commune
colonnes_analyse = [
    "prod",    # Produits de fonctionnement
    "charge",  # Charges de fonctionnement
    "dette",   # Dette
    "emp",     # Emprunts
    "caf",     # Capacité d'autofinancement
    "pop1",    # Population
    "equip",   # Dépenses d'équipement
    "subv",    # Subventions
]

print(f"Colonnes analysées : {colonnes_analyse}\n")

# --- 3. Nettoyage ---
# On garde uniquement les colonnes choisies et on supprime les lignes vides
df_analyse = df[["inom"] + colonnes_analyse].dropna()
print(f"Communes analysées : {len(df_analyse)}")

# --- 4. Normalisation ---
# L'IA a besoin que toutes les colonnes soient à la même échelle
# Sinon "dette" (millions) écrase "population" (milliers)
scaler = StandardScaler()
X = scaler.fit_transform(df_analyse[colonnes_analyse])

# --- 5. Modèle Isolation Forest ---
print("Entraînement du modèle IA...")
modele = IsolationForest(
    contamination=0.02,  # On suppose que 2% des communes sont anormales
    random_state=42
)
modele.fit(X)

# --- 6. Prédiction ---
# -1 = anomalie détectée, 1 = normale
df_analyse = df_analyse.copy()
df_analyse["anomalie"] = modele.predict(X)
df_analyse["score_anomalie"] = modele.score_samples(X)

# --- 7. Résultats ---
anomalies = df_analyse[df_analyse["anomalie"] == -1].copy()
anomalies = anomalies.sort_values("score_anomalie")  # Les plus suspectes en premier

print(f"\n{'='*50}")
print(f"  RAPPORT ANOMALIES - openDQ")
print(f"{'='*50}")
print(f"  Communes analysées  : {len(df_analyse)}")
print(f"  Anomalies détectées : {len(anomalies)}")
print(f"  Taux d'anomalie     : {round(len(anomalies)/len(df_analyse)*100, 2)} %")
print(f"{'='*50}")
print(f"\nTop 10 communes les plus suspectes :\n")
print(anomalies[["inom"] + colonnes_analyse].head(10).to_string(index=False))

# --- 8. Sauvegarde ---
anomalies.to_csv("data/anomalies_detectees.csv", index=False)
print(f"\n Résultats sauvegardés dans data/anomalies_detectees.csv")