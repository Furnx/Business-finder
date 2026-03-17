from scrapers import snupit_scraper, cylex_scraper, maps_scraper
import combine_data
import time

def run_pipeline():
    print("========================================")
    print("   BUSINESS FINDER: DATA PIPELINE")
    print("========================================\n")

    # 1. Run Snupit
    try:
        snupit_scraper.scrape_snupit()
    except Exception as e:
        print(f"Failed to run Snupit scraper: {e}")

    # 2. Run Cylex
    try:
        cylex_scraper.scrape_cylex()
    except Exception as e:
        print(f"Failed to run Cylex scraper: {e}")

    # 3. Run Google Maps
    try:
        # Note: This requires Chrome/ChromeDriver installed
        maps_scraper.scrape_google_maps()
    except Exception as e:
        print(f"Failed to run Google Maps scraper: {e}")

    print("\nScraping phase complete. Merging data...")
    time.sleep(1)

    # 4. Combine everything
    try:
        combine_data.combine_all_leads()
    except Exception as e:
        print(f"Failed to combine data: {e}")

    print("\n========================================")
    print("   PIPELINE EXECUTION FINISHED")
    print("========================================")

if __name__ == "__main__":
    run_pipeline()
