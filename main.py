"""Point de départ de l'application console."""

import re
import unicodedata

from selenium.common.exceptions import TimeoutException, WebDriverException

from app.controllers.scrapping_controller import ScrapingController
from app.models.depot import Depot
from app.scraper.amazon_scraper import AmazonScraper
from app.scraper.driver import creer_driver
from app.scraper.image_downloader import ImageDownloader
from app.views.console_view import ConsoleView
from app.views.export_view import ExportView
from config import CATEGORIE, NOMBRE_PAGES_PAR_DEFAUT


def creer_nom_sous_categorie(mot_cle: str) -> str:
    """Prépare un nom de dossier simple à partir du mot-clé recherché."""
    sans_accents = unicodedata.normalize("NFKD", mot_cle)
    sans_accents = "".join(
        caractere
        for caractere in sans_accents
        if not unicodedata.combining(caractere)
    )
    nom = re.sub(r"[^a-zA-Z0-9]+", "_", sans_accents).strip("_").lower()
    return nom or "recherche"


def main() -> None:
    vue = ConsoleView()
    mot_cle = vue.demander_mot_cle()
    sous_categorie = creer_nom_sous_categorie(mot_cle)

    try:
        driver = creer_driver()
    except WebDriverException as erreur:
        vue.afficher_erreur(
            f"Impossible d'ouvrir Chrome. Vérifie que Chrome est installé. Détail : {erreur}"
        )
        return

    try:
        scraper = AmazonScraper(driver)
        depot = Depot()
        controleur = ScrapingController(
            scraper=scraper,
            image_downloader=ImageDownloader(),
            depot=depot,
            export_view=ExportView(),
        )
        produits = controleur.lancer_scraping(
            mot_cle=mot_cle,
            nombre_pages=NOMBRE_PAGES_PAR_DEFAUT,
            categorie=CATEGORIE,
            sous_categorie=sous_categorie,
        )
        vue.afficher_resultats(produits)
        vue.afficher_statistiques(depot.obtenir_statistiques())
        print("Les résultats ont été enregistrés dans le dossier data.")
    except TimeoutException:
        vue.afficher_erreur(
            "Les cartes de produits n'ont pas été trouvées dans le délai prévu."
        )
    except WebDriverException as erreur:
        vue.afficher_erreur(f"Le navigateur a rencontré un problème : {erreur}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
