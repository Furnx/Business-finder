from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from utils import is_social_only

def scrape_google_maps(search_query="barbers in johannesburg"):
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Optional: run headless
    driver = webdriver.Chrome(options=chrome_options)

    print(f"Starting Google Maps scrape for '{search_query}'...")
    try:
        driver.get(f"https://www.google.com/maps/search/{search_query}")
        time.sleep(5)

        data = []
        businesses = driver.find_elements(By.CLASS_NAME, "Nv2PK")

        for business in businesses:
            try:
                name = business.find_element(By.CLASS_NAME, "qBF1Pd").text
            except:
                name = "N/A"

            # Try to find a phone number
            try:
                phone = "N/A"
                all_text = business.text.split('\n')
                for line in all_text:
                    if any(char.isdigit() for char in line) and len(line) > 8:
                        if '+' in line or line.replace(' ', '').isdigit():
                            phone = line
                            break
            except:
                phone = "N/A"

            try:
                links = business.find_elements(By.TAG_NAME, "a")
                website_link = None
                for link in links:
                    href = link.get_attribute("href")
                    if href and "google.com/maps" not in href:
                        website_link = href
                        break
            except:
                website_link = None

            # Lead qualification: NO website OR SOCIAL ONLY website
            social_link = is_social_only(website_link)

            if website_link is None or social_link:
                data.append({
                    "name": name,
                    "phone": phone,
                    "website": social_link if social_link else "N/A",
                    "source": "google_maps"
                })

        df = pd.DataFrame(data)
        df.to_csv("maps_leads.csv", index=False)
        print(f"Google Maps: Found {len(data)} leads.")
        return data
    except Exception as e:
        print(f"Error scraping Google Maps: {e}")
        return []
    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_google_maps()