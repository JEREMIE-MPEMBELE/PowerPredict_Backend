# schemas/equipment.py
from typing import Dict, List, Literal
from pydantic import BaseModel, Field


class EquipmentInput(BaseModel):
  type_materiel: str = Field(
      ...,
      example="Transformateur 630 kVA",
      description="Type d'équipement électrique",
  )
  capacite_max_kw: float = Field(
      ..., gt=0, example=500.0, description="Capacité maximale en kW"
  )
  consommation_kw: float = Field(
      ..., ge=0, example=350.0, description="Consommation actuelle en kW"
  )
  tension_v: float = Field(
      ..., gt=0, example=220.0, description="Tension mesurée en Volts"
  )


class UIConfig(BaseModel):
  nom_couleur: Literal["rouge", "orange", "vert"] = Field(
      ..., example="rouge", description="Nom sémantique de la couleur"
  )
  code_couleur: str = Field(
      ..., example="#EF4444", description="Code HEX optionnel de secours"
  )
  icone: str = Field(
      ...,
      example="fa-circle-xmark",
      description="Nom de classe d icone (FontAwesome/Bootstrap)",
  )
  statut_affichage: str = Field(
      ..., example="DANGER CRITIQUE", description="Texte de badge UI"
  )


class PredictionOutput(BaseModel):
  panne: int = Field(
      ..., description="0: Normal, 1: Risque de panne détecté"
  )
  probabilite_panne: float = Field(
      ..., description="Probabilité de panne entre 0 et 1"
  )
  pourcentage_risque: str = Field(
      ..., description="Probabilité sous forme de pourcentage"
  )
  niveau_risque: Literal["NORMAL", "AVERTISSEMENT", "CRITIQUE"] = Field(
      ..., description="Niveau de gravité"
  )
  taux_charge_pct: float = Field(
      ..., description="Taux d utilisation de l equipement"
  )
  facteurs_cles: Dict[str, str] = Field(
      ..., description="Diagnostic détaillé des facteurs physiques"
  )
  recommandations: List[str] = Field(
      ..., description="Actions prioritaires pour le technicien"
  )
  ui_config: UIConfig = Field(
      ..., description="Configuration graphique prête à l emploi"
  )