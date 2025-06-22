import csv
import re
import os
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def lire_csv(input_file):
    """
    Lit le fichier CSV et retourne les en-têtes et les données.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as fichier_csv:
            reader = csv.reader(fichier_csv, delimiter=',')
            headers = next(reader)  # Lire la première ligne (en-têtes)
            data = [row for row in reader]
        
        if 'adresse' not in headers:
            logging.error("La colonne 'adresse' n'existe pas dans le fichier CSV.")
            return None, None
        
        logging.info(f"Fichier CSV '{input_file}' lu avec succès. En-têtes : {headers}")
        return headers, data
    
    except FileNotFoundError:
        logging.error(f"Le fichier '{input_file}' n'existe pas.")
        return None, None
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier CSV : {e}")
        return None, None

def separer_adresse(adresse):
    """
    Sépare une adresse en (adresse, code_postal, ville) en utilisant une regex pour le code postal.
    Retourne (adresse_sans_cp_ville, code_postal, ville) ou des valeurs par défaut en cas d'erreur.
    """
    try:
        # Regex pour trouver un code postal de 5 chiffres
        match = re.search(r'(\d{5})\s+(.+)$', adresse)
        if match:
            code_postal = match.group(1)
            ville = match.group(2).strip()
            # Tout ce qui précède le code postal est considéré comme l'adresse
            adresse_sans_cp_ville = adresse[:match.start()].strip()
            return adresse_sans_cp_ville, code_postal, ville
        else:
            logging.warning(f"Format d'adresse invalide : {adresse}")
            return adresse, "Non trouvé", "Non trouvé"
    
    except Exception as e:
        logging.error(f"Erreur lors de la séparation de l'adresse '{adresse}' : {e}")
        return adresse, "Erreur", "Erreur"

def transformer_donnees(headers, data):
    """
    Transforme les données en ajoutant les colonnes 'code_postal' et 'ville'.
    """
    adresse_index = headers.index('adresse')
    new_data = []
    
    for row in data:
        adresse = row[adresse_index]
        adresse_sans_cp_ville, code_postal, ville = separer_adresse(adresse)
        # Créer une nouvelle ligne avec les colonnes supplémentaires
        new_row = row.copy()
        new_row[adresse_index] = adresse_sans_cp_ville  # Remplacer l'adresse complète
        new_row.append(code_postal)
        new_row.append(ville)
        new_data.append(new_row)
    
    logging.info(f"{len(new_data)} lignes transformées avec succès.")
    return new_data

def ecrire_csv(headers, data, output_file):
    """
    Écrit les données dans un nouveau fichier CSV avec les colonnes supplémentaires.
    """
    try:
        new_headers = headers + ['code_postal', 'ville']
        with open(output_file, 'w', newline='', encoding='utf-8') as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=',')
            writer.writerow(new_headers)
            for row in data:
                writer.writerow(row)
        
        logging.info(f"Nouveau fichier CSV créé : {output_file}")
    
    except Exception as e:
        logging.error(f"Erreur lors de l'écriture du fichier CSV '{output_file}' : {e}")

def traiter_csv():
    """
    Fonction principale pour lire, transformer et écrire le fichier CSV.
    """
    # Demander le fichier CSV d'entrée
    input_file = input("Entrez le nom du fichier CSV à traiter (ex. djgeneralist.csv) : ").strip()
    if not input_file:
        logging.error("Aucun nom de fichier fourni. Arrêt du programme.")
        return
    
    # Ajouter l'extension .csv si absente
    if not input_file.endswith('.csv'):
        input_file += '.csv'
    
    # Vérifier si le fichier existe
    if not os.path.exists(input_file):
        logging.error(f"Le fichier '{input_file}' n'existe pas. Arrêt du programme.")
        return
    
    # Créer le nom du fichier de sortie
    output_file = input_file.replace('.csv', '_cp.csv')
    
    # Lire le fichier CSV
    headers, data = lire_csv(input_file)
    if headers is None or data is None:
        return
    
    # Transformer les données
    new_data = transformer_donnees(headers, data)
    
    # Écrire dans le nouveau fichier CSV
    ecrire_csv(headers, new_data, output_file)

if __name__ == "__main__":
    traiter_csv()