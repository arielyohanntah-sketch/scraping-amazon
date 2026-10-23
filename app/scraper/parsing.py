"""Lecture des informations d'une carte produit avec des sélecteurs CSS."""

from typing import Optional, Union
from urllib.parse import parse_qs, urljoin, urlparse

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from app.models.produit import Produit


# Sélecteur observé sur les résultats Amazon.fr; à recontrôler si la page change.
SELECTEUR_CARTE_PRODUIT = '[data-component-type="s-search-result"]'


def _texte_optionnel(
    element: Union[WebElement, WebDriver], selecteur: str
) -> Optional[str]:
    """Renvoie le texte trouvé, ou None si cet élément n'existe pas."""
    try:
        texte = element.find_element(By.CSS_SELECTOR, selecteur).text.strip()
        return texte or None
    except NoSuchElementException:
        return None


def _attribut_optionnel(
    element: Union[WebElement, WebDriver], selecteur: str, attribut: str
) -> Optional[str]:
    """Renvoie un attribut HTML (par exemple src ou href), s'il existe."""
    try:
        valeur = element.find_element(By.CSS_SELECTOR, selecteur).get_attribute(attribut)
        return valeur.strip() if valeur else None
    except NoSuchElementException:
        return None


def parser_carte_produit(carte: WebElement) -> Optional[Produit]:
    """Transforme une carte de résultat en Produit, si elle a un nom."""
    nom = _texte_optionnel(carte, "h2")
    if not nom:
        return None

    # Amazon place le prix dans un texte masqué visuellement. Selenium .text
    # peut donc renvoyer une chaîne vide ; textContent lit le contenu HTML.
    try:
        element_prix = carte.find_element(
            By.CSS_SELECTOR, ".a-price .a-offscreen"
        )
        prix_texte = (element_prix.get_attribute("textContent") or "").strip()
    except NoSuchElementException:
        prix_texte = None

    prix = None
    if prix_texte:
        # Exemple : « 29,99 € » devient le nombre 29.99.
        prix_normalise = (
            prix_texte.replace("€", "")
            .replace("\xa0", "")
            .replace(" ", "")
            .replace(",", ".")
        )
        try:
            prix = float(prix_normalise)
        except ValueError:
            prix = None

    lien_produit = None
    try:
        titre = carte.find_element(By.CSS_SELECTOR, "h2")
        lien_produit = titre.find_element(
            By.XPATH, "./ancestor::a[1]"
        ).get_attribute("href")
    except NoSuchElementException:
        pass

    if lien_produit and "/sspa/click" in urlparse(lien_produit).path:
        destination = parse_qs(urlparse(lien_produit).query).get("url", [None])[0]
        if destination:
            lien_produit = destination
    image_url = _attribut_optionnel(carte, "img.s-image", "src")
    if lien_produit:
        lien_produit = urljoin("https://www.amazon.fr", lien_produit)
    if image_url:
        image_url = urljoin("https://www.amazon.fr", image_url)

    return Produit(
        nom=nom,
        prix=prix,
        devise="EUR",
        image_url=image_url,
        url=lien_produit,
    )


def parser_details_produit(driver: WebDriver, produit: Produit) -> None:
    """Complète un produit à partir de sa page détaillée."""
    for selecteur in ("#bylineInfo", "#brand"):
        marque = _texte_optionnel(driver, selecteur)
        if marque:
            marque = marque.replace("Visiter la boutique", "", 1).strip()
        if marque:
            produit.marque = marque
            break

    for selecteur in ("#feature-bullets", "#productDescription", "#aplus"):
        description = _texte_optionnel(driver, selecteur)
        if description:
            produit.description = description
            break

    for selecteur in ("#landingImage", "#imgTagWrapperId img"):
        image_url = _attribut_optionnel(driver, selecteur, "data-old-hires")
        image_url = image_url or _attribut_optionnel(driver, selecteur, "src")
        if image_url:
            produit.image_url = urljoin("https://www.amazon.fr", image_url)
            break
