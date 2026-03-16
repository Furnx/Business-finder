import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "DIRECTORY_PAGE_URL"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

businesses = soup.find_all("div", class_="listing")

data = []

for business in businesses:

    name = business.find("h2").text

    phone = business.find("span", class_="phone")

    website = business.find("a", class_="website")

    if website is None:
        data.append({
            "name": name,
            "phone": phone.text if phone else "N/A"
        })

df = pd.DataFrame(data)

df.to_csv("leads.csv", index=False)

print("Leads saved!")