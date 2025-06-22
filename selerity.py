from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import logging
import time

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extraire(url):
    """
    Extrait les éléments HTML depuis une URL avec Selenium.
    Retourne une liste d'éléments ou None en cas d'erreur.
    """
    try:
        # Configuration de Selenium avec Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Exécuter sans interface graphique
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # Charger la page
        driver.get(url)
        time.sleep(3)  # Attendre que la page soit complètement chargée
        html_content = driver.page_source
        driver.quit()
        
        logging.info(f"Page web chargée avec succès : {url}")
        
        # Transforme le HTML en objet BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        elements = soup.find_all("div", class_="bi-content")
        
        if not elements:
            logging.warning("Aucun élément trouvé avec la classe 'bi-content'. Vérifiez la structure HTML.")
        else:
            logging.info(f"{len(elements)} éléments trouvés avec la classe 'bi-content'.")
        
        return elements
    
    except Exception as e:
        logging.error(f"Erreur inattendue lors de l'extraction : {e}")
        return None

def transformer(element):
    """
    Transforme un élément HTML en un tuple (titre, adresse, description).
    Gère les cas où les éléments sont absents ou mal formatés.
    """
    try:
        titre = element.find("h3")
        adresse = element.find("a", class_="pj-lb pj-link")
        description = element.find("p", class_="bi-description")
        
        titre_text = titre.get_text(strip=True) if titre else "Titre non trouvé"
        adresse_text = adresse.get_text(strip=True) if adresse else "Adresse non trouvée"
        description_text = description.get_text(strip=True) if description else "Description non trouvée"
        
        logging.info(f"Données extraites : Titre={titre_text}, Adresse={adresse_text}, Description={description_text}")
        return (titre_text, adresse_text, description_text)
    
    except AttributeError as attr_err:
        logging.error(f"Erreur dans la transformation, élément HTML mal formé : {attr_err}")
        return ("Erreur", "Erreur", "Erreur")

def charger(donnees, output_file):
    """
    Charge les données dans un fichier CSV spécifié par l'utilisateur.
    Vérifie si les données sont valides avant écriture.
    """
    if not donnees:
        logging.error("Aucune donnée à écrire dans le CSV.")
        return
    
    en_tete = ["nom", "adresse", "description"]
    try:
        with open(output_file, "w", newline="", encoding="utf-8") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=",")
            writer.writerow(en_tete)
            valid_rows = 0
            
            for donnee in donnees:
                if donnee and len(donnee) == 3:
                    writer.writerow(donnee)
                    valid_rows += 1
                else:
                    logging.warning(f"Donnée invalide ignorée : {donnee}")
            
            logging.info(f"{valid_rows} lignes écrites dans le fichier CSV : {output_file}")
    
    except IOError as io_err:
        logging.error(f"Erreur lors de l'écriture du fichier CSV : {io_err}")

def etl(url, output_file):
    """
    Exécute le processus ETL (Extraction, Transformation, Chargement) sur une URL.
    """
    logging.info("Début du processus ETL.")
    
    elements = extraire(url)
    if elements is None:
        logging.error("Échec de l'extraction, abandon du processus.")
        return
    
    resultats = [transformer(element) for element in elements]
    charger(resultats, output_file)
    
    logging.info("Processus ETL terminé.")

if __name__ == "__main__":
    # Demander à l'utilisateur de saisir l'URL
    url = input("Entrez l'URL de la page à scraper (ex. https://www.super-site/with-great-pages) : ").strip()
    if not url:
        logging.error("Aucune URL fournie. Arrêt du programme.")
        exit(1)
    
    # Demander à l'utilisateur de saisir le nom du fichier CSV de sortie
    output_file = input("Entrez le nom du fichier CSV de sortie (ex. djgeneralist.csv) : ").strip()
    if not output_file:
        logging.error("Aucun nom de fichier fourni. Arrêt du programme.")
        exit(1)
    
    # Ajouter l'extension .csv si absente
    if not output_file.endswith('.csv'):
        output_file += '.csv'
    
    etl(url, output_file)