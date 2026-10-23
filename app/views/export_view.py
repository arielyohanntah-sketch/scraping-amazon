"""Export des produits dans un fichier CSV."""

import csv
from pathlib import Path
from typing import Iterable, Optional

from app.models.produit import Produit


class ExportView:
    """Écrit les produits dans le dossier de données du projet."""

    def __init__(self, dossier_data: Optional[Path] = None) -> None:
        racine_projet = Path(__file__).resolve().parents[2]
        self.dossier_data = dossier_data or racine_projet / "data"

    def exporter_produits(
        self,
        produits: Iterable[Produit],
        categorie: str = "tech",
        sous_categorie: str = "ecouteurs",
    ) -> Path:
        """Crée le CSV de la sous-catégorie et renvoie son chemin."""
        dossier = self.dossier_data / categorie / sous_categorie
        dossier.mkdir(parents=True, exist_ok=True)
        chemin_csv = dossier / "data.csv"

        colonnes = [
            "nom",
            "prix",
            "devise",
            "description",
            "marque",
            "image_url",
            "image_path",
            "url",
        ]

        with chemin_csv.open("w", newline="", encoding="utf-8-sig") as fichier:
            redacteur = csv.DictWriter(fichier, fieldnames=colonnes)
            redacteur.writeheader()
            for produit in produits:
                redacteur.writerow(
                    {
                        "nom": produit.nom,
                        "prix": produit.prix,
                        "devise": produit.devise,
                        "description": produit.description,
                        "marque": produit.marque,
                        "image_url": produit.image_url,
                        "image_path": produit.image_path,
                        "url": produit.url,
                    }
                )

        return chemin_csv

    def mettre_a_jour_recap(
        self, categorie: str, sous_categorie: str, nombre_produits: int
    ) -> Path:
        """Met à jour le récapitulatif des sous-catégories collectées."""
        self.dossier_data.mkdir(parents=True, exist_ok=True)
        chemin_recap = self.dossier_data / "recap.csv"
        donnees = {}

        if chemin_recap.exists():
            with chemin_recap.open(
                "r", newline="", encoding="utf-8-sig"
            ) as fichier:
                for ligne in csv.DictReader(fichier):
                    cle = (ligne["categorie"], ligne["sous_categorie"])
                    donnees[cle] = int(ligne["nombre_produits"])

        donnees[(categorie, sous_categorie)] = nombre_produits
        # Plusieurs sous-catégories peuvent appartenir à la même catégorie.
        nombre_categories = len({categorie for categorie, _ in donnees})

        with chemin_recap.open("w", newline="", encoding="utf-8-sig") as fichier:
            colonnes = [
                "categorie",
                "sous_categorie",
                "nombre_produits",
                "nombre_categories_scrapees",
            ]
            redacteur = csv.DictWriter(fichier, fieldnames=colonnes)
            redacteur.writeheader()
            for (nom_categorie, nom_sous_categorie), total in sorted(
                donnees.items()
            ):
                redacteur.writerow(
                    {
                        "categorie": nom_categorie,
                        "sous_categorie": nom_sous_categorie,
                        "nombre_produits": total,
                        "nombre_categories_scrapees": nombre_categories,
                    }
                )

        return chemin_recap
