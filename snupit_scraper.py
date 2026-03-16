import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import is_social_only

def scrape_snupit(city="johannesburg", category="barbers"):
    url = f"https://www.snupit.co.za/{city}/{category}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    print(f"Starting Snupit scrape for {category} in {city}...")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        data = []
        businesses = soup.find_all("div", class_="listing")

        for business in businesses:
            name_tag = business.find("h2")
            phone_tag = business.find("span", class_="phone")
            website_tag = business.find("a", class_="website")

            name = name_tag.text.strip() if name_tag else "N/A"
            phone = phone_tag.text.strip() if phone_tag else "N/A"
            website_link = website_tag.get("href") if website_tag else None

            # Lead qualification: NO website OR SOCIAL ONLY website
            social_link = is_social_only(website_link)
            
            if website_link is None or social_link:
                data.append({
                    "name": name,
                    "phone": phone,
                    "website": social_link if social_link else "N/A",
                    "source": "snupit"
                })

        df = pd.DataFrame(data)
        df.to_csv("snupit_leads.csv", index=False)
        print(f"Snupit: Found {len(data)} leads.")
        return data
    except Exception as e:
        print(f"Error scraping Snupit: {e}")
        return []


if __name__ == "__main__":
    scrape_snupit()