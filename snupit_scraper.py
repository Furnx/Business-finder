import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.snupit.co.za/johannesburg/barbers"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

data = []

# NOTE: selectors may change depending on page structure
businesses = soup.find_all("div", class_="listing")

for business in businesses:

    name_tag = business.find("h2")
    phone_tag = business.find("span", class_="phone")
    website_tag = business.find("a", class_="website")

    name = name_tag.text.strip() if name_tag else "N/A"
    phone = phone_tag.text.strip() if phone_tag else "N/A"

    if website_tag is None:
        data.append({
            "name": name,
            "phone": phone,
            "source": "snupit"
        })

df = pd.DataFrame(data)
df.to_csv("snupit_leads.csv", index=False)

print("Snupit leads saved")