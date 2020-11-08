from selenium import webdriver 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas
import time

def search():

    # Load ONE-Line Tracking Site
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://www.bestbuy.ca/en-ca/category/laptops-macbooks/20352")

    # Repeats for first 10 iterations of laptops on the best buy website
    for i in range(10):
        try:
            editor = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[3]/div[1]/div/main/a/div/button/span')))
            editor.click()
        except:
            break
    
    # Stores information for the name, price, and reviews
    title = driver.find_elements_by_css_selector('div.productItemName_3IZ3c')
    price = driver.find_elements_by_css_selector('span.screenReaderOnly_3anTj.large_3aP7Z')
    stars = driver.find_elements_by_css_selector('span.reviewCountContainer_2EO6o')
    
    # creates object for each laptop
    df = pandas.DataFrame(columns=[
            "Title",
            "Store",
            "Price",
            "Stars",
            "# of Reviews"
        ])

    # Goes through all objects in the bestbuy site
    for i in range(len(title)):

        time.sleep(0.01)

        # Stores relevant information
        data = {
            "Title": title[i].text,
            "Store": "BestBuy",
            "Price": price[i].text
        }
        
        for star in stars[i].find_elements_by_xpath('.//*'):
            if star.get_attribute("data-automation") == "rating-count":
                data["# of Reviews"] = star.text
            else:
                data["Stars"] = star.get_attribute("content")

        # Adds object to be displayed in csv
        df = df.append(data, ignore_index=True)


    # Repeats above process for stapes
    driver = webdriver.Chrome("chromedriver.exe")

    # Connects to staples site
    driver.get("https://www.staples.ca/search?query=laptops&page=1&configure%5BgetRankingInfo%5D=true&configure%5BuserToken%5D=3141209871171383&configure%5BclickAnalytics%5D=true&configure%5BhitsPerPage%5D=32&configure%5Bfilters%5D=tags%3A%22en_CA%22")

    time.sleep(0.1)

    # Repeats for 10 different staples pages
    for i in range (10):

        time.sleep(0.01)
        name = driver.find_elements_by_css_selector("a.product-thumbnail__title.product-link")
        price = driver.find_elements_by_css_selector("span.money.pre-money")
        totalRating = driver.find_elements_by_css_selector(".bv_main_container.bv_hover")

        # Goes through all objects in single page
        for i in range(len(name)):
            
            # Stores relevant data
            data = {
                    "Title": name[i].text,
                    "Store": "Staples Canada",
                    "Price": price[i].text,
                    "Stars": totalRating[i].get_attribute("aria-label")
                }

            # Adds object to be displayed in csv
            df = df.append(data, ignore_index=True)

        # Proceeds to next page to add laptops from the rest of the pages
        editor = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="algoliasearch-container"]/div/div[1]/div/div[3]/div[4]/div[2]/div/div/ul/li[10]/a')))
        editor.click()	


    # Exports all objects to csv
    df.to_csv("laptop_data.csv")
                
# Calls the program
search() 