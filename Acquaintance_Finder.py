import json
import requests
from bs4 import BeautifulSoup

def get_all_links(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <a> (anchor) tags in the HTML
        links = soup.find_all('a')

        # Extract the href attribute from each <a> tag
        
        hrefs = [link.get('href') for link in links]
        cleanHrefs = []
        for href in hrefs:
            if href:
                if href[:4] != "http":
                    href = "https://en.uesp.net" + href
                cleanHrefs.append(href)
        return cleanHrefs

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def search_words_in_url(url, links_datas):
    try:
        links = get_all_links(url)
        found_words = []
        for link_data in links_datas:
            name = link_data.get("name")
            link = link_data.get("link")
            if link in links:
                found_words.append(name)
        return found_words

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def main():
    # Read JSON-like entries from a text file
    with open("SkyrimCharacters.json", "r") as file:
        links_datas = json.load(file)
    results = []
    # Search and write results for each link
    for link_data in links_datas:
        name = link_data.get("name")
        link = link_data.get("link")

        if name and link:
            found_words = search_words_in_url(link, links_datas)
            unique_list = list(set(found_words))
            if name in unique_list: unique_list.remove(name)
            results.append({"name": name, "link": link, "acquaintances": unique_list})
            with open("Acquaintances.json", "w") as result_file:
                json.dump(results, result_file, indent=2)

if __name__ == "__main__":
    main()

