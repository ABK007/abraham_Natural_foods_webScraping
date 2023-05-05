# 1. Import Libraries
import time
import pandas as pd
import csv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import string

# 2. Load Webpage in Selenium

# Calling the chrome browser
driver = webdriver.Chrome()
driver.maximize_window()  # maximizing windows

# Loading the web page
driver.get("https://abrahamnaturalfoods.com/")

# 3. Logging In

# The login form was hidden by the CSS style (display:block/none) and we execute javascript command to display it
driver.execute_script("javascript:document.getElementById('lgm').click();")

time.sleep(2)

username = driver.find_element(By.CSS_SELECTOR, "#userid")
password = driver.find_element(By.CSS_SELECTOR, "#password")

username.send_keys("sales@kspacificusa")
password.send_keys("52eblockpmc")

driver.find_element(By.CSS_SELECTOR, "#form0 > div > div.text-center.mb-4 > div > input").click()

# The webpage is logged in now

time.sleep(3)

# 4. Opening the page will all brands in alphabetical order

driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")  # Scroll to bottom of the page

driver.find_element(By.XPATH, "/html/body/div[5]/div/div[3]/div[12]/span[2]/a").click()  # click on view all link

# 5. Iterating through the brand pages sorted in alphbetical order and scraping products.

time.sleep(2)

get_url = driver.current_url  # getting current url

aplhabet_list = string.ascii_uppercase

sale_price = []
unit_price = []
size = []
upc = []
brand_name = []
product_description = []

for letter in aplhabet_list:
    # iterating through every alphabet
    driver.get(f"{get_url}?brandid={letter}")
    time.sleep(3)

    # getting all the brands on the each alphabet page
    brands_list = driver.find_elements(By.CLASS_NAME, "brandlist_container")

    # opening the product listing page for each brand
    for ele in brands_list:
        brand_id = ele.get_attribute('data-brandid')  # getting value of 'data-brandid' attribute
        brands_products_url = str(
            f"https://abrahamnaturalfoods.com/plst/bl?bid={brand_id}")  # url for each brand listing page
        driver.get(brands_products_url)  # loading the brand listing page
        time.sleep(2)

        # creating lists containing the unit price and sale price of each product
        items = driver.find_elements(By.CLASS_NAME, "ppr-container")
        for each in items:
            text = each.text.split("\n")
            sale_price.append(text[3])
            unit_price.append(text[2])

        # creating list containing the size of each product
        size_items = driver.find_elements(By.CLASS_NAME, "product_size")
        for i in size_items:
            text = i.text.split(':')[1]
            size.append(text)

        # creating lists containing the product title of each product
        items = driver.find_elements(By.CLASS_NAME, "product_title")
        for j in items:
            text = j.text
            product_description.append(text)

        # creating lists containing the brand name of each product
        items = driver.find_elements(By.CLASS_NAME, "product_brand_title")
        for k in items:
            text = k.text
            brand_name.append(text)

        print(sale_price)
        print(unit_price)
        print(size)
        print(product_description)
        print(brand_name)

        # iterating through each product popup in the list
        products = driver.find_elements(By.CLASS_NAME, "itemimage")
        for elem in products:
            driver.execute_script("javascript:arguments[0].click();", elem)
            time.sleep(2)
            # creating a list of upc for each product
            upc.append(driver.find_element(By.CSS_SELECTOR,
                                           "#productdetail > div > div:nth-child(2) > div.detailpanel_desc.detail_decription").text.split(
                '\n')[3])

            time.sleep(2)
        print(upc)

        driver.back()

        # Converting to dictionary
        abraham_foods_dict = {"product": product_description,
                              "upc": upc,
                              "unit price": unit_price,
                              "brand": brand_name,
                              "sale price": sale_price,
                              "size": size}

        # converting to dataframe
        df = pd.DataFrame.from_dict(abraham_foods_dict)

        # Saving as csv file
        df.to_csv("abraham_foods_data.csv")

time.sleep(10)
