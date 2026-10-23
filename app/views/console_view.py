"""Affichage et saisie des informations dans le terminal."""

from typing import Dict, List, Optional, Union

from app.models.produit import Produit


class ConsoleView:
    """Affiche les questions et les résultats dans la console."""

    def demander_mot_cle(self) -> str:
        """Demande le produit ou le mot-clé à chercher sur Amazon."""
        while True:
            reponse = input(
                "Mot-clé à rechercher sur Amazon (ex. iPhone, JBL, Lenovo) : "
            ).strip()
            if reponse:
                return reponse
            print("Écris un produit ou un mot-clé pour lancer la recherche.")

    def afficher_resultats(self, produits: List[Produit]) -> None:
        """Affiche un résumé des produits récupérés."""
        if not produits:
            print("Aucun produit n'a été récupéré.")
            return

        print(f"\n{len(produits)} produit(s) récupéré(s) :")
        for numero, produit in enumerate(produits, start=1):
            prix = (
                f"{produit.prix:.2f} {produit.devise}"
                if produit.prix is not None
                else "prix indisponible"
            )
            print(f"{numero}. {produit.nom} — {prix}")

    def afficher_statistiques(
        self, statistiques: Dict[str, Union[int, Optional[float]]]
    ) -> None:
        """Affiche le résumé des prix calculé depuis SQLite."""
        print("\nStatistiques de la collecte :")
        print(f"- Produits enregistrés : {statistiques['nombre_produits']}")
        print(f"- Produits avec un prix : {statistiques['nombre_avec_prix']}")

        prix_moyen = statistiques["prix_moyen"]
        prix_minimum = statistiques["prix_minimum"]
        prix_maximum = statistiques["prix_maximum"]
        if prix_moyen is None:
            print("- Aucun prix disponible pour calculer les statistiques.")
            return

        print(f"- Prix moyen : {prix_moyen:.2f} EUR")
        print(f"- Prix le plus bas : {prix_minimum:.2f} EUR")
        print(f"- Prix le plus élevé : {prix_maximum:.2f} EUR")

    def afficher_erreur(self, message: str) -> None:
        """Affiche une erreur compréhensible dans le terminal."""
        print(f"Erreur : {message}")
