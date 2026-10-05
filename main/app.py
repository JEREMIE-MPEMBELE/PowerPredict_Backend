# main/app.py
import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas.equipment import EquipmentInput, PredictionOutput, UIConfig

app = FastAPI(
    title="PowerPredict - Predictive Maintenance API",
    description=(
        "API prédictive pour équipements électriques avec séparation claire"
        " Author : Jérémie MPEMBELE"
    ),
    version="2.0.0",
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl")
)

try:
    pipeline = joblib.load(MODEL_PATH)
    print(f"[OK] Pipeline ML chargé depuis : {MODEL_PATH}")
except Exception as e:
    print(f"[ERREUR] Impossible de charger le modèle : {e}")
    pipeline = None


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "API Maintenance Prédictive PowerPredict",
        "author": "Jérémie MPEMBELE",
    }


@app.post("/predict", response_model=PredictionOutput)
def predict_equipment_status(data: EquipmentInput):
    if pipeline is None:
        raise HTTPException(
            status_code=500, detail="Le modèle ML n'est pas disponible."
        )

    try:
        input_data = pd.DataFrame([data.model_dump()])

        # 1. Analyse Machine Learning (Score brut d'anomalie)
        prediction = int(pipeline.predict(input_data)[0])
        probabilities = pipeline.predict_proba(input_data)[0]
        prob_panne = float(probabilities[1])

        # 2. Calcul physique du taux de charge
        taux_charge = (data.consommation_kw / data.capacite_max_kw) * 100

        # --- 3. RÈGLES PHYSIQUES STRICTES POUR L'UI (SÉCURITÉ RÉSEAU) ---
        # La physique décide de la couleur et du statut de l'interface
        if taux_charge > 100 or data.tension_v < 195:
            niveau = "CRITIQUE"
            prediction = 1
            ui = UIConfig(
                nom_couleur="rouge",
                code_couleur="#EF4444",
                icone="fa-circle-xmark",
                statut_affichage="DANGER CRITIQUE",
            )
        elif (85 < taux_charge <= 100) or (195 <= data.tension_v < 210):
            niveau = "AVERTISSEMENT"
            ui = UIConfig(
                nom_couleur="orange",
                code_couleur="#F59E0B",
                icone="fa-triangle-exclamation",
                statut_affichage="RISQUE MODÉRÉ",
            )
        else:
            niveau = "NORMAL"
            ui = UIConfig(
                nom_couleur="vert",
                code_couleur="#10B981",
                icone="fa-circle-check",
                statut_affichage="ÉQUIPEMENT SAIN",
            )

        # Le modèle ML fournit sa vraie probabilité pure comme indicateur statistique
        prob_affichee = prob_panne

        # Diagnostics physiques
        facteurs = {}
        if taux_charge > 100:
            facteurs["surcharge"] = (
                f"Surcharge sévère : {round(taux_charge, 1)}% de la capacité nominale."
            )
        elif taux_charge > 85:
            facteurs["surcharge"] = (
                f"Charge élevée : {round(taux_charge, 1)}% de la capacité nominale."
            )
        else:
            facteurs["surcharge"] = (
                f"Charge normale : {round(taux_charge, 1)}% de la capacité."
            )

        if data.tension_v < 195:
            facteurs["tension"] = (
                f"Chute de tension critique mesurée : {data.tension_v}V."
            )
        elif data.tension_v < 210:
            facteurs["tension"] = (
                f"Baisse modérée de tension mesurée : {data.tension_v}V."
            )
        else:
            facteurs["tension"] = f"Tension stable : {data.tension_v}V."

        # Recommandations
        recommandations = []
        if taux_charge > 100:
            recommandations.append(
                "Délestage prioritaire requis pour éviter l'avarie matérielle."
            )
        elif taux_charge > 85:
            recommandations.append(
                "Surveiller la charge et planifier une redistribution de départ."
            )

        if data.tension_v < 195:
            recommandations.append(
                "Chute critique : Vérifier le régleur en charge et inspecter la ligne amont."
            )
        elif data.tension_v < 210:
            recommandations.append(
                "Baisse de tension : Inspecter le poste de transformation et vérifier le départ HTA."
            )

        if not recommandations:
            recommandations.append(
                "Aucune intervention requise. Poursuivre le suivi de routine."
            )

        return PredictionOutput(
            panne=prediction,
            probabilite_panne=round(prob_affichee, 4),
            pourcentage_risque=f"{round(prob_affichee * 100, 2)}%",
            niveau_risque=niveau,
            taux_charge_pct=round(taux_charge, 2),
            facteurs_cles=facteurs,
            recommandations=recommandations,
            ui_config=ui,
        )

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Erreur lors de la prédiction : {str(e)}"
        )