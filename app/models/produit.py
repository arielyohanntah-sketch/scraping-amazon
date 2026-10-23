"""Modèle représentant un produit récupéré sur le site."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Produit:
    """Informations utiles sur un produit, par exemple un écouteur."""

    nom: str
    prix: Optional[float] = None
    devise: str = "EUR"
    description: Optional[str] = None
    marque: Optional[str] = None
    image_url: Optional[str] = None
    image_path: Optional[str] = None
    url: Optional[str] = None
