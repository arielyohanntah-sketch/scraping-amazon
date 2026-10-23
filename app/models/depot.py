"""Accès aux produits enregistrés dans la base SQLite."""

import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Union

from app.models.produit import Produit


class Depot:
    """Enregistre et récupère les produits dans ``data/produits.db``."""

    def __init__(self, chemin_db: Optional[Path] = None) -> None:
        racine_projet = Path(__file__).resolve().parents[2]
        self.chemin_db = chemin_db or racine_projet / "data" / "produits.db"
        self.chemin_db.parent.mkdir(parents=True, exist_ok=True)
        self._creer_table()

    def _creer_table(self) -> None:
        """Crée la table des produits si elle n'existe pas encore."""
        with sqlite3.connect(self.chemin_db) as connexion:
            connexion.execute(
                """
                CREATE TABLE IF NOT EXISTS produits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prix REAL,
                    devise TEXT NOT NULL,
                    description TEXT,
                    marque TEXT,
                    image_url TEXT,
                    image_path TEXT,
                    url TEXT
                )
                """
            )

    def ajouter_produit(self, produit: Produit) -> None:
        """Ajoute un produit à la base de données."""
        with sqlite3.connect(self.chemin_db) as connexion:
            connexion.execute(
                """
                INSERT INTO produits
                    (nom, prix, devise, description, marque, image_url, image_path, url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    produit.nom,
                    produit.prix,
                    produit.devise,
                    produit.description,
                    produit.marque,
                    produit.image_url,
                    produit.image_path,
                    produit.url,
                ),
            )

    def remplacer_produits(self, produits: List[Produit]) -> None:
        """Remplace le contenu de la table par les produits de la collecte."""
        with sqlite3.connect(self.chemin_db) as connexion:
            connexion.execute("DELETE FROM produits")
            connexion.executemany(
                """
                INSERT INTO produits
                    (nom, prix, devise, description, marque, image_url, image_path, url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        produit.nom,
                        produit.prix,
                        produit.devise,
                        produit.description,
                        produit.marque,
                        produit.image_url,
                        produit.image_path,
                        produit.url,
                    )
                    for produit in produits
                ],
            )

    def lister_produits(self) -> List[Produit]:
        """Renvoie les produits enregistrés sous forme d'objets Produit."""
        with sqlite3.connect(self.chemin_db) as connexion:
            lignes = connexion.execute(
                """
                SELECT nom, prix, devise, description, marque, image_url, image_path, url
                FROM produits
                ORDER BY id
                """
            ).fetchall()

        return [
            Produit(
                nom=ligne[0],
                prix=ligne[1],
                devise=ligne[2],
                description=ligne[3],
                marque=ligne[4],
                image_url=ligne[5],
                image_path=ligne[6],
                url=ligne[7],
            )
            for ligne in lignes
        ]

    def obtenir_statistiques(self) -> Dict[str, Union[int, Optional[float]]]:
        """Calcule des statistiques simples sur les prix enregistrés."""
        with sqlite3.connect(self.chemin_db) as connexion:
            ligne = connexion.execute(
                """
                SELECT
                    COUNT(*),
                    COUNT(prix),
                    AVG(prix),
                    MIN(prix),
                    MAX(prix)
                FROM produits
                """
            ).fetchone()

        return {
            "nombre_produits": ligne[0],
            "nombre_avec_prix": ligne[1],
            "prix_moyen": ligne[2],
            "prix_minimum": ligne[3],
            "prix_maximum": ligne[4],
        }
