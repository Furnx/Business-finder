from urllib.parse import urlparse

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
