"""Coordination du scraping et de la sauvegarde des produits."""

from typing import List

from app.models.depot import Depot
from app.models.produit import Produit
from app.scraper.amazon_scraper import AmazonScraper
from app.scraper.image_downloader import ImageDownloader
from app.views.export_view import ExportView


class ScrapingController:
    """Fait le lien entre le scraper, les exports et le dépôt SQLite."""

    def __init__(
        self,
        scraper: AmazonScraper,
        image_downloader: ImageDownloader,
        depot: Depot,
        export_view: ExportView,
    ) -> None:
        self.scraper = scraper
        self.image_downloader = image_downloader
        self.depot = depot
        self.export_view = export_view

    def lancer_scraping(
        self,
        mot_cle: str = "écouteurs",
        nombre_pages: int = 1,
        categorie: str = "tech",
        sous_categorie: str = "ecouteurs",
    ) -> List[Produit]:
        """Collecte les produits, écrit les CSV, puis met à jour SQLite."""
        produits = self.scraper.rechercher(mot_cle, nombre_pages)

        for numero, produit in enumerate(produits, start=1):
            produit.image_path = self.image_downloader.telecharger_image(
                produit.image_url, numero, categorie, sous_categorie
            )

        # Le CSV est créé avant la base, conformément au flux demandé.
        self.export_view.exporter_produits(
            produits, categorie, sous_categorie
        )
        self.export_view.mettre_a_jour_recap(
            categorie, sous_categorie, len(produits)
        )
        self.depot.remplacer_produits(produits)

        return produits
