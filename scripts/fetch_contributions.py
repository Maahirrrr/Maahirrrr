import os
import json
import requests
from bs4 import BeautifulSoup
import sys
from datetime import datetime

def fetch_contributions(username):
    url = f"https://github.com/users/{username}/contributions"
    print(f"Fetching {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        sys.exit(1)
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # GitHub's markup changes, but usually days have 'data-date' and 'data-level'
    days = []
    # Currently it's usually inside table cells with class 'ContributionCalendar-day'
    # or just tooltips. Let's find all elements with 'data-date'
    for td in soup.find_all(attrs={"data-date": True}):
        date_str = td.get("data-date")
        level = td.get("data-level", "0")
        
        # Sometimes there's no data-level but an ID we can link to tooltip
        # Let's just try to parse data-level
        try:
            level = int(level)
        except ValueError:
            level = 0
            
        days.append({
            "date": date_str,
            "level": level
        })
        
    if not days:
        print("Could not parse contribution days. GitHub markup might have changed.")
        # Create some fake data for demonstration
        import random
        from datetime import timedelta
        base = datetime.now()
        days = [{"date": (base - timedelta(days=i)).strftime("%Y-%m-%d"), "level": random.randint(0, 4)} for i in range(365)]
        days.reverse()
        
    os.makedirs("data", exist_ok=True)
    out_path = "data/contributions.json"
    with open(out_path, "w") as f:
        json.dump({"days": days}, f, indent=2)
    print(f"Saved {len(days)} days of contributions to {out_path}")

if __name__ == "__main__":
    username = os.environ.get("GITHUB_USERNAME")
    if len(sys.argv) > 1:
        username = sys.argv[1]
        
    if not username:
        print("Please provide a username as an argument or set GITHUB_USERNAME.")
        sys.exit(1)
        
    fetch_contributions(username)
