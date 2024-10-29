from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
#driver = webdriver.Chrome()
#from selenium import webdriver


def scrape_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    
    try:
        #response = requests.get(url, headers=headers, verify=False)
        driver.execute_cdp_cmd(
        'Network.setExtraHTTPHeaders',
        {'headers': headers}
        )
        driver.get(url)
        scroll = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, '[class="SearchPageListContainer__StyledSearchPageListContainer-srp-8-105-2__sc-4vf8s4-0 iudnrF search-page-list-container short-list-cards"]')))
        scroll_steps = 50 
        scroll_pause_time = 0.1
        for step in range(scroll_steps):
            driver.execute_script("arguments[0].scrollBy(0, arguments[0].scrollHeight / arguments[1])", scroll, scroll_steps)
            time.sleep(scroll_pause_time)
        print(0)
        response = driver.page_source
        if response is not None:
            soup = BeautifulSoup(response, 'html.parser')
            return soup
        else:
            return f"Failed to retrieve the page. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"

def scrape_property_details(url):
    property_data=[]
    t = scrape_html(url)
    props = t.find_all("li", {"class": "ListItem-c11n-8-105-0__sc-13rwu5a-0 StyledListCardWrapper-srp-8-105-0__sc-wtsrtn-0 gpgmwS cXzrsE"})
    for i in range(len(props)):
        if props[i].find("address") != None:
            address = props[i].find("address").text
            prop_details = props[i].find("div", {"class": "StyledPropertyCardFlexWrapper-c11n-8-105-0__sc-38h0t9-0 bLBlIw"})
            if prop_details is not None:
                details = prop_details.find_all("a", {"class": "Anchor-c11n-8-105-0__sc-hn4bge-0 PropertyCardInventoryBox__StyledAnchor-srp-8-105-0__sc-1jotqb7-0 eccwKW bCbPDg"})
                for prop in details:
                    price = prop.find("span", {"class": "Text-c11n-8-105-0__sc-aiai24-0 PropertyCardInventoryBox__PriceText-srp-8-105-0__sc-1jotqb7-3 ipLfim iHUmOr"})
                    bhk = prop.find("span", {"class": "Text-c11n-8-105-0__sc-aiai24-0 PropertyCardInventoryBox__BedText-srp-8-105-0__sc-1jotqb7-2 gfVizO icfgfO"})
                    property_data.append([address,bhk.text,price.text])
            else:
                price = props[i].find("span", {"class": "PropertyCardWrapper__StyledPriceLine-srp-8-105-0__sc-16e8gqd-1 dHAgxu"})
                details = props[i].find("ul", {"class": "StyledPropertyCardHomeDetailsList-c11n-8-105-0__sc-1j0som5-0 ldtVy"})
                bhk = details.find("b").text + " " + details.find("abbr").text
                property_data.append([address,bhk,price.text])
    return property_data
property_data_master = []
for page in range(11,21):
    driver = uc.Chrome()
    driver.maximize_window()
    url = f"https://www.zillow.com/boston-ma/rentals/5_p/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-71.55232991334057%2C%22east%22%3A-70.89521016236401%2C%22south%22%3A42.17339433122132%2C%22north%22%3A42.53012781409444%7D%2C%22mapZoom%22%3A11%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A44269%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22pagination%22%3A%7B%22currentPage%22%3A{page}%7D%7D"
    property_data = scrape_property_details(url)
    property_data_master += property_data
    driver.quit()
columns = ['address', 'bds', 'cost']
df = pd.DataFrame(property_data_master, columns=columns)
df.to_csv('property_data.csv')
