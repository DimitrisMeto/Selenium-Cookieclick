from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

chrome_driver_path = "/Users/dimitris/Development/chromedriver"

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")

items = driver.find_elements(By.CSS_SELECTOR, "div#store div")
items_ids = [item.get_attribute("id") for item in items]

time_out = time.time() + 5
fiv_min = time.time() + 5*60

while True:
    cookie.click()

    if time.time() > time_out:
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip("").replace(",", ""))
                item_prices.append(cost)
        # print(item_prices)
        # print(items_ids)

        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = items_ids[n]

        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
            print(money_element)
        cookie_count = int(money_element)

        affordable_upgrades = {}

        for cost, item_id in cookie_upgrades.items():
            if cost < cookie_count:
                affordable_upgrades[cost] = item_id

        highest_affordable_upgrade = max(affordable_upgrades)
        print(highest_affordable_upgrade)
        id_to_click = affordable_upgrades[highest_affordable_upgrade]

        driver.find_element(By.ID, id_to_click).click()

        time_out = time.time() + 5

    if time.time() > fiv_min:
        cookies_per_second = driver.find_element(By.ID, "cps").text
        print(cookies_per_second)
        break

