import requests

from bs4 import BeautifulSoup

url = "https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=colege&ou=Eure-et-Loir+%2828%29&univers=pagesjaunes&idOu=D028"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
descriptions = soup.find_all("li", class_="bi-header-title")
stockage = []

for desc in descriptions:
    stockage.append(desc.string)

print(soup)
'''print(stockage)'''