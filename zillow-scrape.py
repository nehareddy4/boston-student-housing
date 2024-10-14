import requests
from bs4 import BeautifulSoup
import csv

def scrape_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        else:
            return f"Failed to retrieve the page. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"

def scrape_property_details(url):
    return 0


def save_to_csv(properties_data, filename):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Address', 'Price', 'Bedrooms'])
            writer.writeheader()
            for property in properties_data:
                writer.writerow(property)
        
        print(f"Data successfully saved to {filename}")
    
    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")
url = "https://www.zillow.com/boston-ma/rentals/3_p/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A3%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-71.55232991334057%2C%22east%22%3A-70.89521016236401%2C%22south%22%3A42.17339433122132%2C%22north%22%3A42.53012781409444%7D%2C%22mapZoom%22%3A11%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A44269%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
scrape_property_details(url)
