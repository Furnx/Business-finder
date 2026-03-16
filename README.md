# Business Finder & Lead Generator

## Overview
Business Finder is a Python-based web scraper designed to help digital agencies and freelancers find sales leads. It identifies businesses listed in online directories that **do not currently have a website**, making them prime prospects for web development, SEO, and digital marketing services.

## Features
- **Targeted Scraping**: Specifically filters for businesses missing a website URL (identifying "low-hanging fruit" leads).
- **Lead Export**: Saves company names and phone numbers directly to a `leads.csv` for easy CRM integration or outreach tracking.
- **Lightweight & Fast**: Built with Python using `BeautifulSoup` and `Requests` for efficient parsing.

## Prerequisites
- Python 3.x
- Dependencies listed in `requirements.txt`

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Business-finder
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Open `lead_finder.py`.
2. Replace `DIRECTORY_PAGE_URL` in line 5 with the URL of the business directory page you wish to scrape.
3. Run the script:
   ```bash
   python lead_finder.py
   ```
4. View your leads in the generated `leads.csv` file.

## Tech Stack
- **Requests**: For handling HTTP requests.
- **BeautifulSoup4**: For parsing HTML and extracting listing data.
- **Pandas**: For structured data handling and CSV generation.
