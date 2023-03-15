import requests
from lxml import html

# URL de la page à accéder
url = "https://extensions.gnome.org/extension/5805/disk-usage/"

# Récupération du contenu de la page
response = requests.get(url)
content = response.content

# Extraction de l'élément à partir de son xpath
tree = html.fromstring(content)
element = tree.xpath('/html/body/div[2]/div/div[2]/div[1]/span[3]')[0]
texte = element.text

# Affichage du texte extrait
print(texte)
