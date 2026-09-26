import requests

def extract_username_from_email(query):
    """Extracts prefix if email, and cleans spaces."""
    query = query.strip()
    if "@" in query:
        query = query.split("@")[0]
    return query.replace(" ", "").lower()

def scan_platforms(query, platforms_dict):
    """Checks platforms including Facebook and Snapchat with strict validation."""
    username = extract_username_from_email(query)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }
    
    found_accounts = []

    for platform, url_pattern in platforms_dict.items():
        target_url = url_pattern.format(username)
        try:
            # Kuch badi sites ke liye timeout thoda adjust kiya hai
            timeout_limit = 6 if platform in ["Instagram", "Facebook", "Snapchat"] else 5
            response = requests.get(target_url, headers=headers, timeout=timeout_limit)
            
            if response.status_code == 200:
                page_text = response.text.lower()
                is_valid = True
                
                # Platform-specific validation rules
                if platform == "Facebook":
                    # Facebook aksar user na hone par login page ya error throw karta hai
                    if "this page isn't available" in page_text or "content not found" in page_text or "log in to facebook" in page_text:
                        is_valid = False
                elif platform == "Snapchat":
                    # Snapchat par public profile na ho ya invalid ho toh yeh terms aati hain
                    if "page not found" in page_text or "add friends on snapchat" in page_text and len(page_text) < 1000:
                        is_valid = False
                elif platform == "Instagram":
                    if "page isn't available" in page_text or "sorry, this page isn't available" in page_text:
                        is_valid = False
                elif platform == "Reddit":
                    if "this account has been suspended" in page_text or "page not found" in page_text or len(page_text.strip()) < 500:
                        is_valid = False
                elif platform == "GitHub":
                    if "block-user" in page_text or "you may be looking for" in page_text:
                        is_valid = False
                elif platform == "TikTok":
                    if "could not find this account" in page_text or "user not found" in page_text:
                        is_valid = False
                elif platform == "Pinterest":
                    if "sorry we couldn't find" in page_text or "oops!" in page_text:
                        is_valid = False
                elif platform == "Twitter (X)":
                    if "this account doesn't exist" in page_text or "user not found" in page_text:
                        is_valid = False
                else:
                    not_found_keywords = ["not found", "doesn't exist", "page not found", "user not found", "oops", "sorry"]
                    if any(keyword in page_text for keyword in not_found_keywords):
                        is_valid = False

                if is_valid:
                    found_accounts.append({
                        "platform": platform,
                        "url": target_url
                    })
                    
        except requests.exceptions.RequestException:
            pass

    return username, found_accounts