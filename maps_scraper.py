from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome()

search = "barbers in johannesburg"
driver.get(f"https://www.google.com/maps/search/{search}")

time.sleep(5)

data = []

businesses = driver.find_elements(By.CLASS_NAME, "Nv2PK")

for business in businesses:

    try:
        name = business.find_element(By.CLASS_NAME, "qBF1Pd").text
    except:
        name = "N/A"

    try:
        website = business.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        website = None

    if website is None:
        data.append({
            "name": name,
            "source": "google_maps"
        })

df = pd.DataFrame(data)
df.to_csv("maps_leads.csv", index=False)

driver.quit()

print("Google Maps leads saved")