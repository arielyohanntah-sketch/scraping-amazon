"""Téléchargement des fichiers image à partir des liens trouvés par Selenium."""

import mimetypes
from pathlib import Path
from typing import Optional
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen


class ImageDownloader:
    """Enregistre les images dans le dossier de la sous-catégorie."""

    DELAI_ATTENTE = 10
    TAILLE_MAXIMALE = 10 * 1024 * 1024

    def __init__(self) -> None:
        self.racine_projet = Path(__file__).resolve().parents[2]

    def telecharger_image(
        self,
        url: Optional[str],
        numero: int,
        categorie: str,
        sous_categorie: str,
    ) -> Optional[str]:
        """Télécharge une image et renvoie son chemin relatif au projet."""
        if not url or urlparse(url).scheme not in {"http", "https"}:
            return None

        try:
            with urlopen(url, timeout=self.DELAI_ATTENTE) as reponse:
                type_contenu = reponse.headers.get_content_type()
                if not type_contenu.startswith("image/"):
                    return None
                contenu = reponse.read(self.TAILLE_MAXIMALE + 1)
        except (URLError, TimeoutError, OSError):
            return None

        if len(contenu) > self.TAILLE_MAXIMALE:
            return None

        extension = mimetypes.guess_extension(type_contenu) or ".img"
        if extension == ".jpe":
            extension = ".jpg"

        dossier = (
            self.racine_projet
            / "data"
            / categorie
            / sous_categorie
            / "images"
        )
        dossier.mkdir(parents=True, exist_ok=True)
        chemin_image = dossier / f"image_{numero:03d}{extension}"
        chemin_image.write_bytes(contenu)
        return str(chemin_image.relative_to(self.racine_projet))
