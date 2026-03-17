import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import is_social_only, get_random_proxy

def scrape_cylex(city="johannesburg", category="barber"):
    url = f"https://www.cylex.net.za/{city}/{category}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    print(f"Starting Cylex scrape for {category} in {city}...")
    
    proxy = get_random_proxy()
    if proxy:
        print(f"Using proxy: {proxy['http']}")

    try:
        response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        
        data = []
        businesses = soup.find_all("div", class_="company-card")

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
                    "source": "cylex"
                })

        df = pd.DataFrame(data)
        df.to_csv("cylex_leads.csv", index=False)
        print(f"Cylex: Found {len(data)} leads.")
        return data
    except Exception as e:
        print(f"Error scraping Cylex: {e}")
        return []

if __name__ == "__main__":
    scrape_cylex()
