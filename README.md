```markdown
# ⚡ PowerPredict

> Système intelligent de prédiction des pannes et de diagnostic de charge pour les équipements électriques, propulsé par FastAPI et Scikit-Learn.

---

## 🚀 À propos du projet
**PowerPredict** est une application web full-stack de Machine Learning conçue pour analyser l'état des équipements électriques (comme les transformateurs). Elle permet d'évaluer le taux de charge, de prédire les risques de pannes et de fournir des recommandations automatisées pour optimiser la maintenance préventive.

---

## 🛠️ Technologies & Stack Technique

- **Backend :** FastAPI, Uvicorn, Pydantic
- **Machine Learning :** Scikit-Learn, Pandas, NumPy, Joblib
- **Frontend :** HTML5, CSS3, JavaScript (Vanilla)
- **Hébergement & Déploiement :** Render

---

## 📂 Structure du Projet

```text
PowerPredict_Backend/
│
├── models/
│   └── model.pkl         # Modèle de Machine Learning entraîné (Pipeline)
│
├── main.app              # Point d'entrée de l'API FastAPI
├── requirements.txt      # Dépendances du projet
├── .python-version       # Version de Python configurée (3.11.9)
├── index.html            # Interface utilisateur (Frontend)
└── script.js             # Logique JavaScript & appels API

```

---

## 🔌 API Endpoints

* **`GET /`** : Vérification de l'état de l'API (Health Check).
* **`POST /predict`** : Reçoit les caractéristiques d'un équipement et retourne le diagnostic complet (taux de charge, niveau de risque, facteurs clés et recommandations).

### Exemple de Payload (JSON) pour `/predict` :

```json
{
  "type_materiel": "Transformateur 630 kVA",
  "capacite_max_kw": 500,
  "consommation_kw": 350,
  "tension_v": 220
}

```

---

## 💻 Installation et Lancement en Local

Si tu souhaites cloner et tester le projet sur ta machine :

1. **Cloner le dépôt :**
```bash
git clone [https://github.com/JEREMIE-MPEMBELE/PowerPredict_Backend.git](https://github.com/JEREMIE-MPEMBELE/PowerPredict_Backend.git)
cd PowerPredict_Backend

```


2. **Créer et activer un environnement virtuel :**
```bash
python -m venv .venv
# Sur Windows :
.venv\Scripts\activate
# Sur Mac/Linux :
source .venv/bin/activate

```


3. **Installer les dépendances :**
```bash
pip install -r requirements.txt

```


4. **Lancer le serveur de développement :**
```bash
uvicorn main:app --reload

```



---

## 🌐 Déploiement

L'API est actuellement déployée et accessible en ligne sur Render :

* **URL de l'API :** `https://powerpredict-sfwt.onrender.com`

---

## 👨‍💻 Auteur

Développé par **Jérémie MPEMBELE** — PowerPredict © 2026

```

```
