# dashboard/app.py
# Module 4 - Dashboard de pilotage qualité

import pandas as pd
import streamlit as st
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# --- CONFIG PAGE ---
st.set_page_config(
    page_title="openDQ - Data Quality",
    page_icon="🔍",
    layout="wide"
)

# --- TITRE ---
st.title("🔍 openDQ — Tableau de bord Qualité des Données")
st.markdown("**Plateforme de pilotage de la qualité des données financières des communes françaises**")
st.divider()

# --- CHARGEMENT ---
@st.cache_data
def charger_donnees():
    df = pd.read_csv("data/communes.csv", sep=";", encoding="utf-8", low_memory=False)
    return df

df = charger_donnees()

# --- SECTION 1 : VUE GENERALE ---
st.header("📊 Vue générale du dataset")

col1, col2, col3 = st.columns(3)
col1.metric("Nombre de communes", f"{len(df):,}")
col2.metric("Nombre de colonnes", f"{df.shape[1]}")
col3.metric("Année des données", f"{df['an'].max()}")

st.dataframe(df[["inom", "dep", "pop1", "prod", "charge", "dette"]].head(20))

st.divider()

# --- SECTION 2 : SCORE QUALITE ---
st.header("✅ Score de qualité des données")

total_cellules = df.size
cellules_vides = df.isnull().sum().sum()
completude = round(((total_cellules - cellules_vides) / total_cellules) * 100, 2)
unicite = round(((len(df) - df.duplicated().sum()) / len(df)) * 100, 2)
score_global = round((completude + unicite) / 2, 2)

col1, col2, col3 = st.columns(3)
col1.metric("Complétude", f"{completude} %")
col2.metric("Unicité", f"{unicite} %")
col3.metric("Score global", f"{score_global} / 100")

st.divider()

# --- SECTION 3 : ANOMALIES ---
st.header("🚨 Détection d'anomalies par IA")

colonnes_analyse = ["prod", "charge", "dette", "emp", "caf", "pop1", "equip", "subv"]
df_analyse = df[["inom", "dep"] + colonnes_analyse].dropna()

scaler = StandardScaler()
X = scaler.fit_transform(df_analyse[colonnes_analyse])

modele = IsolationForest(contamination=0.02, random_state=42)
modele.fit(X)

df_analyse = df_analyse.copy()
df_analyse["anomalie"] = modele.predict(X)
df_analyse["score_anomalie"] = modele.score_samples(X)

anomalies = df_analyse[df_analyse["anomalie"] == -1].sort_values("score_anomalie")

st.metric("Anomalies détectées", f"{len(anomalies)} communes")

st.subheader("Top 20 communes les plus suspectes")
st.dataframe(anomalies[["inom", "dep"] + colonnes_analyse].head(20))

st.divider()

# --- SECTION 4 : EXPLORATION ---
st.header("🔎 Exploration par département")

deps = sorted(df["dep"].unique().tolist())
dep_choisi = st.selectbox("Choisis un département", deps)

df_dep = df[df["dep"] == dep_choisi][["inom", "pop1", "prod", "charge", "dette", "caf"]]
st.dataframe(df_dep)

st.bar_chart(df_dep.set_index("inom")["dette"].head(20))

st.caption("openDQ — Projet Data Steward | Données : data.gouv.fr / DGFiP")