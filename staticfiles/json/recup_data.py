import json
import pycountry
import ram
# Liste des fichiers JSON contenant les noms de pays
json_files = ['Afrique_name.json', 'Amerique_noms.json','Pacific_name.json', 'Arabic_name.json', 'Asian_name.json', 'Europe_name.json']

# Charger la liste complète des pays à partir de pycountry
all_countries = [country.name for country in pycountry.countries]

# Nom du fichier texte de sortie
output_file = "liste_pays.txt"

# Écrire la liste de tous les pays dans le fichier texte
with open(output_file, "w", encoding="utf-8") as file:
    for country in all_countries:
        file.write(country + "\n")

print(f"La liste des pays a été écrite dans le fichier {output_file}.")

# Initialiser un ensemble pour stocker les pays uniques de vos fichiers JSON
unique_json_countries = set()

# Parcourir tous les fichiers JSON
for file_name in json_files:
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        # Supposons que chaque fichier JSON contient une liste de pays
        for item in data:
            pays = item.get('pays')
            if pays:
                unique_json_countries.add(pays)

# Convertir l'ensemble en liste
unique_json_countries = list(unique_json_countries)

# Trouver les pays manquants
missing_countries = set(all_countries) - set(unique_json_countries)

# Imprimer les pays manquants
print("Pays manquants par rapport à la liste ISO 3166-1 :")
for country in missing_countries:
    print(country)

# Ouvrir le fichier JSON en lecture
with open('Asian_name.json', 'r') as json_file:
    data = json.load(json_file)

# Accéder aux joueurs

randomdata[i]['pays']
    