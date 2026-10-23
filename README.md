# Projet de web scraping Amazon

Ce projet a été réalisé dans le cadre d'un cours de programmation Python. Il me permet de pratiquer le web scraping avec Selenium en recherchant des produits sur Amazon.fr.

Le programme demande un mot-clé, par exemple `iPhone`, `JBL` ou `montres`. Il récupère quelques informations sur les produits trouvés, puis les enregistre dans des fichiers CSV et dans une base SQLite. Il affiche aussi des statistiques simples sur les prix.

## Informations récupérées

Selon les informations présentes sur Amazon, le programme essaie de récupérer :

- le nom et le prix du produit ;
- la marque et la description, quand elles sont disponibles ;
- le lien de l'image et une copie de l'image dans le dossier du projet ;
- le lien de la page du produit.

Pour limiter la taille d'une collecte, le programme traite au maximum cinq produits par page. Le nombre de pages à parcourir et les délais d'attente se règlent dans `config.py`.

## Organisation des fichiers

```text
app/
├── controllers/       Lance et coordonne les différentes étapes
├── models/            Produit et accès à la base SQLite
├── scraper/           Navigation Amazon et lecture des pages
└── views/             Affichage dans la console et export CSV
config.py              Catégorie, limites et délais
main.py                Démarrage du programme
requirements.txt       Bibliothèques nécessaires
data/                  Fichiers créés pendant les recherches
```

Le code est organisé en MVC : le modèle représente et enregistre les produits, la vue s'occupe de l'affichage et des fichiers CSV, et le contrôleur relie ces étapes. Le dossier `scraper` contient le code Selenium qui ouvre les pages et récupère les informations.

## Installation

Ouvre un terminal dans le dossier du projet, puis crée et active l'environnement virtuel. Installe ensuite les dépendances :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Le projet utilise Chrome. Selenium Manager cherche le pilote nécessaire au lancement du programme.

## Lancer une recherche

Dans le même terminal, lance :

```powershell
python main.py
```

Entre le mot-clé que tu veux rechercher quand le programme le demande. Les résultats sont rangés dans un dossier sous `data/tech/`, nommé à partir du mot-clé.

## Résultats d'une recherche

```text
data/
├── recap.csv
├── produits.db
└── tech/
    └── mot_cle_recherche/
        ├── data.csv
        └── images/
```

`data.csv` contient les produits de cette recherche et `images/` contient les images téléchargées. `recap.csv` résume les recherches enregistrées. La base `produits.db` sert à conserver les produits et à calculer les statistiques de la collecte.

## À savoir

Amazon peut modifier la présentation de ses pages. Si le programme ne trouve plus les produits ou certaines informations, les sélecteurs CSS utilisés dans `app/scraper/parsing.py` devront peut-être être vérifiés. Les champs absents sur une page restent vides dans les résultats.
