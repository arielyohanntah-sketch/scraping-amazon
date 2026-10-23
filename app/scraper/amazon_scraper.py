"""Recherche des produits sur les pages de résultats Amazon."""

from typing import List
from urllib.parse import urlencode

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

from config import DELAI_ATTENTE_RESULTATS, NOMBRE_MAX_PRODUITS_PAR_PAGE
from app.models.produit import Produit
from app.scraper.parsing import (
    SELECTEUR_CARTE_PRODUIT,
    parser_carte_produit,
    parser_details_produit,
)


class AmazonScraper:
    """Ouvre des pages de recherche et transforme les cartes en produits."""

    URL_RECHERCHE = "https://www.amazon.fr/s"

    def __init__(
        self, driver: WebDriver, delai_attente: int = DELAI_ATTENTE_RESULTATS
    ) -> None:
        self.driver = driver
        self.delai_attente = delai_attente

    def rechercher(self, mot_cle: str, nombre_pages: int = 1) -> List[Produit]:
        """Récupère les produits des premières pages de résultats."""
        if nombre_pages < 1:
            raise ValueError("nombre_pages doit être supérieur ou égal à 1")

        produits = []
        for numero_page in range(1, nombre_pages + 1):
            parametres = urlencode({"k": mot_cle, "page": numero_page})
            self.driver.get(f"{self.URL_RECHERCHE}?{parametres}")

            cartes = WebDriverWait(self.driver, self.delai_attente).until(
                conditions.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, SELECTEUR_CARTE_PRODUIT)
                )
            )

            # On limite le nombre de pages produit ouvertes pour cette page de résultats.
            for carte in cartes[:NOMBRE_MAX_PRODUITS_PAR_PAGE]:
                produit = parser_carte_produit(carte)
                if produit is not None:
                    produits.append(produit)

        for produit in produits:
            if not produit.url:
                continue
            self.driver.get(produit.url)
            try:
                WebDriverWait(self.driver, self.delai_attente).until(
                    conditions.presence_of_element_located(
                        (By.CSS_SELECTOR, "#productTitle")
                    )
                )
            except TimeoutException:
                # Si la page attendue n'apparaît pas, on garde les données de la carte.
                continue
            parser_details_produit(self.driver, produit)

        return produits
