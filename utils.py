from urllib.parse import urlparse
import random
import os

SOCIAL_DOMAINS = {
    "facebook.com", "instagram.com", "linkedin.com", "twitter.com", 
    "x.com", "tiktok.com", "youtube.com", "pinterest.com", 
    "wa.me", "linktr.ee"
}

def is_social_only(url):
    """
    Returns the URL if it is a social media page, otherwise returns None.
    Also returns None if the URL is empty or None.
    """
    if not url:
        return None
    
    try:
        domain = urlparse(url).netloc.lower()
        # Remove 'www.' if present
        if domain.startswith("www."):
            domain = domain[4:]
            
        if any(social in domain for social in SOCIAL_DOMAINS):
            return url
    except:
        pass
        
    return None

def get_random_proxy():
    """
    Reads proxies from proxies.txt and returns a random one in requests format.
    Returns None if no proxies are found.
    """
    proxy_file = "proxies.txt"
    if not os.path.exists(proxy_file):
        return None
        
    try:
        with open(proxy_file, "r") as f:
            # Filter out comments and empty lines
            proxies = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            
        if not proxies:
            return None
            
        proxy = random.choice(proxies)
        
        # Return in dictionary format for requests
        return {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }
    except Exception as e:
        print(f"Warning: Could not read proxies: {e}")
        return None
