import requests
from bs4 import BeautifulSoup

# Einlesen der richtigen URL mit BeautifulSoup je nach Nutzereingabe 
def get_pokemon_url():
    while True:    
        print("Gib den Namen eines Pokémon ein.")
        name = str(input())
        url = f'https://www.pokewiki.de/{name}'

        try:
            response = requests.get(url)
            response.raise_for_status()
            return url, name
        # Hinweis an den Nutzer, wenn die Eingabe nicht zu einer gültigen URL führt
        except requests.RequestException as e:
            print(f"Fehler bei der Anfrage: {e}")
            print("Bitte überprüfen Sie den eingegebenen Namen und versuchen Sie es erneut.")


def main():
    url, name = get_pokemon_url()  # URL und Name von der Funktion erhalten
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Suchen des eingegebenen Pokemon
    pokemon_basis = soup.find('a', class_='mw-selflink selflink')

    # Überprüfen, ob das Ziel-Element gefunden wurde
    if pokemon_basis:
        # Zählervariable für die Anzahl der gefundenen Eltern-Elemente
        count_found_parents = 0

        # Schleife durch die parent-Elemente
        while pokemon_basis.parent is not None:
            pokemon_basis = pokemon_basis.find_parent()
            count_found_parents += 1

            # Stoppen, wenn das sechste Eltern-Element erreicht ist
            if count_found_parents == 6:
                next_tr_sibling = pokemon_basis.find_next_sibling('tr')
                if next_tr_sibling:
                    next_a_content = next_tr_sibling.find('a').text
                    next_a = next_tr_sibling.find('a')
                    # Prüfen, ob ein <a>-Element vorhanden ist und ob dieses über ein 'style'-Attribut verfügt
                    if next_a_content is not None and not next_tr_sibling.has_attr('style'):
                        # Navigieren zur Stelle der Entwicklung des eingegebenen Pokemon
                        next_ul_sibling = next_a.find_next_sibling('ul')
                        next_small_content = next_ul_sibling.find('small').text
                        print(name, "entwickelt sich weiter zu:", next_a_content)
                        print("Hinweis:", next_small_content)
                    else:
                        print(name, "hat keine Entwicklungen.")
                else:
                    print(name, "hat keine Entwicklungen.")
                break
    else:
        print("Der eingegebene Name wurde nicht gefunden.")

if __name__ == "__main__":
    main()
