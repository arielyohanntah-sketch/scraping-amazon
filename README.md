# Projet de web scraping Amazon

Application console Python organisée selon le modèle MVC. Le projet recherche des écouteurs sur Amazon.fr avec Selenium, enregistre les informations dans un fichier CSV et dans SQLite, et calcule quelques statistiques de prix.

## Informations récupérées

- Nom et prix du produit
- Marque et description, si elles sont présentes sur la page produit
- Lien de l'image et chemin de l'image enregistrée localement
- Lien de la page du produit

Le programme traite au maximum cinq produits par page de résultats. Les informations qui ne sont pas trouvées restent vides.

## Structure du projet

```text
app/
├── controllers/       Coordination des étapes du programme
├── models/            Produit et accès à la base SQLite
├── scraper/           Selenium, analyse des pages et images
└── views/             Console et export CSV
config.py              Valeurs par défaut et délais d'attente
main.py                Point de départ du programme
requirements.txt       Dépendances Python
data/                  Fichiers CSV, images et base SQLite créés à l'exécution
```

## Installation

Dans un terminal ouvert à la racine du projet, crée et active l'environnement virtuel, puis installe Selenium :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Chrome doit être installé. Selenium Manager s'occupe normalement de trouver le pilote correspondant lors du lancement.

## Lancement

```powershell
python main.py
```

La console demande le mot-clé à chercher sur Amazon (par exemple `iPhone`, `JBL` ou `montres`). Le projet classe les recherches dans la catégorie générale `tech`, puis dans un sous-dossier nommé d'après le mot-clé. La pagination est conservée dans le scraper et son nombre de pages se règle dans `config.py`.

## Fichiers générés

```text
data/
├── recap.csv
├── produits.db
└── tech/
    └── mot_cle_recherche/
        ├── data.csv
        └── images/
```

data.csv contient les produits de la dernière collecte. recap.csv récapitule les sous-catégories collectées et leur nombre de produits. produits.db contient les produits de la dernière collecte et sert au calcul des statistiques. Le dossier images contient les fichiers image téléchargés quand leur lien est disponible.

## Organisation MVC

- **Modèle** : Produit décrit un produit et Depot lit ou écrit les données SQLite.
- **Vue** : ConsoleView gère les échanges dans le terminal et ExportView écrit les CSV.
- **Contrôleur** : ScrapingController coordonne la collecte, le filtrage et les sauvegardes.
- **Scraper** : AmazonScraper utilise Selenium pour naviguer et les fonctions de parsing.py pour lire les éléments de page.

## Réglages

Modifie config.py pour régler le nombre de pages, les délais d'attente ou le nombre maximum de produits traités sur chaque page. Les fichiers de chaque collecte sont rangés dans un dossier nommé d'après le mot-clé recherché.

Les sélecteurs CSS de app/scraper/parsing.py ont été comparés à une page de résultats et à une fiche produit Amazon.fr. La structure du site peut changer : vérifie-les de nouveau si le programme ne trouve plus certaines informations.
