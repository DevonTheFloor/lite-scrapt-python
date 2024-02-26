import requests
from bs4 import BeautifulSoup
import csv


def extraire(url):
    reponse = requests.get(url)
    page = reponse.content

    # transforme (parse) le HTML en objet BeautifulSoup
    soup = BeautifulSoup(page, "html.parser")
    elements = soup.find_all("li", class_="gem-c-document-list__item")
    return elements


def transformer(element):
    titre = element.find("a", class_="govuk-link")
    description = element.find("p", class_="gem-c-document-list__item-description")
    return (titre.string, description.string)


def charger(donnees):
    en_tete = ["titre", "description"]
    # création du fichier data.csv
    with open("data.csv", "w", newline="") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",")
        writer.writerow(en_tete)

        for donnee in donnees:
            writer.writerow(donnee)


def etl(url):
    elements = extraire(url)
    resultats = [transformer(element) for element in elements]
    charger(resultats)


if __name__ == "__main__":
    etl("https://www.gov.uk/search/news-and-communications")
