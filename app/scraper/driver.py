"""Création du navigateur utilisé par Selenium."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import DELAI_CHARGEMENT_PAGE


def creer_driver() -> webdriver.Chrome:
    """Ouvre Chrome et limite le temps d'attente du chargement d'une page."""
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(DELAI_CHARGEMENT_PAGE)
    return driver
