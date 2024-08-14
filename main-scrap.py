import requests
from bs4 import BeautifulSoup
import csv


def extraire(url):
    """
    Extrait tous les éléments de liste (`<li>`) ayant la classe `gem-c-document-list__item` à partir d'une page HTML située à l'URL spécifiée.
    Cette fonction envoie une requête HTTP GET à l'URL donnée, récupère le contenu de la page, et utilise BeautifulSoup pour parser le HTML. Elle retourne tous les éléments `<li>` de la page qui possèdent la classe CSS `gem-c-document-list__item`.
    :param url: str
        L'URL de la page web à partir de laquelle les éléments doivent être extraits.
    :return: list of bs4.element.Tag
        Une liste d'objets BeautifulSoup représentant les éléments `<li>` trouvés avec la classe `gem-c-document-list__item`. Si aucun élément n'est trouvé, la liste retournée sera vide.
    :raises requests.exceptions.RequestException:
        Si une erreur se produit lors de la requête HTTP (par exemple, problème de réseau ou URL incorrecte).
    :raises bs4.FeatureNotFound:
        Si le parser `html.parser` n'est pas disponible sur le système.
    """
    reponse = requests.get(url)
    page = reponse.content

    # transforme (parse) le HTML en objet BeautifulSoup
    soup = BeautifulSoup(page, "html.parser")
    elements = soup.find_all("li", class_="gem-c-document-list__item")
    return elements


def transformer(element):
    """
    Transforme un élément BeautifulSoup en un tuple contenant le titre et la description.
    Cette fonction prend un élément `<li>` analysé par BeautifulSoup, extrait le titre et la description, et les retourne sous forme de tuple. Le titre est extrait de la balise `<a>` avec la classe `govuk-link`, tandis que la description est extraite de la balise `<p>` avec la classe `gem-c-document-list__item-description`.
    :param element: bs4.element.Tag
        Un objet BeautifulSoup représentant un élément `<li>` d'une liste de documents. Cet élément doit contenir un lien (`<a>`) avec la classe `govuk-link` et un paragraphe (`<p>`) avec la classe `gem-c-document-list__item-description`.
    :return: tuple
        Un tuple contenant deux chaînes de caractères : le titre et la description de l'élément. Si l'une des balises n'est pas trouvée, les valeurs correspondantes dans le tuple seront `None`.
    :raises AttributeError:
        Si l'attribut `string` n'est pas disponible sur les balises trouvées (par exemple, si elles sont absentes ou mal formatées).
    """
    titre = element.find("a", class_="govuk-link")
    description = element.find("p", class_="gem-c-document-list__item-description")
    return (titre.string, description.string)


def charger(donnees):
    """
    Charge les données fournies dans un fichier CSV nommé `data.csv`.
    Cette fonction prend une liste de données, où chaque élément est une liste ou un tuple contenant les informations pour une entrée. Elle crée un fichier `data.csv` et y écrit les données sous forme de lignes, avec des en-têtes "nom" et "adresse".
    :param donnees: list of list or list of tuple
        Une liste où chaque élément est une liste ou un tuple représentant une ligne de données à écrire dans le fichier CSV. Chaque sous-liste ou tuple doit contenir deux éléments : le nom et l'adresse.
    :return: None
        Cette fonction ne retourne rien. Elle crée ou écrase simplement le fichier `data.csv` avec les données fournies.
    :raises IOError:
        Si une erreur se produit lors de l'ouverture ou de l'écriture dans le fichier `data.csv`.
    """
    en_tete = ["nom", "adresse"]
    # création du fichier data.csv
    with open("data.csv", "w", newline="") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",")
        writer.writerow(en_tete)

        for donnee in donnees:
            writer.writerow(donnee)


def etl(url):
    """
    Extrait des éléments d'une page web, les transforme en tuples de données, puis les enregistre dans un fichier CSV.
    Cette fonction exécute un flux de travail complet qui consiste à :
    1. Extraire les éléments de liste (`<li>`) à partir d'une page web spécifiée par l'URL.
    2. Transformer chaque élément extrait en un tuple contenant un titre et une description.
    3. Charger les résultats transformés dans un fichier CSV nommé `data.csv`.
    :param url: str
        L'URL de la page web à partir de laquelle les éléments doivent être extraits.
    :return: None
        Cette fonction ne retourne rien. Elle crée un fichier CSV avec les données extraites et transformées.
    :raises requests.exceptions.RequestException:
        Si une erreur se produit lors de la requête HTTP à l'URL spécifiée.
    :raises bs4.FeatureNotFound:
        Si le parser `html.parser` n'est pas disponible sur le système.
    :raises AttributeError:
        Si les éléments extraits n'ont pas les attributs attendus pour l'extraction du titre ou de la description.
    :raises IOError:
        Si une erreur se produit lors de l'ouverture ou de l'écriture dans le fichier `data.csv`.
    """
    elements = extraire(url)
    resultats = [transformer(element) for element in elements]
    charger(resultats)


if __name__ == "__main__":
    etl("https://www.gov.uk/search/news-and-communications")
