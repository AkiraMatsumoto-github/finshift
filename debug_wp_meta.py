
import os
import sys
from dotenv import load_dotenv
import requests
import json

# Load env
load_dotenv("automation/.env")

WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_PASSWORD = os.getenv("WP_APP_PASSWORD")

if WP_URL.endswith('/'): WP_URL = WP_URL[:-1]

def check_latest_post():
    auth = (WP_USER, WP_PASSWORD)
    # Get latest post in 'market-analysis' category
    # first get category id
    print("Fetching category ID...")
    cat_res = requests.get(f"{WP_URL}/wp-json/wp/v2/categories?slug=market-analysis", auth=auth)
    cat_data = cat_res.json()
    if not cat_data:
        print("Category not found")
        return

    cat_id = cat_data[0]['id']
    
    print(f"Fetching latest post in category {cat_id}...")
    posts_res = requests.get(f"{WP_URL}/wp-json/wp/v2/posts?categories={cat_id}&per_page=1", auth=auth)
    posts = posts_res.json()
    
    if not posts:
        print("No posts found.")
        return

    post = posts[0]
    print(f"Latest Post: {post['title']['rendered']} (ID: {post['id']})")
    
    # Check meta - NOTE: Standard API might not expose protected meta keys (starting with _)
    # We might need to use the custom endpoint or context=edit if user has permission
    # Let's try standard 'meta' field first, often empty for protected.
    print(f"Standard Meta: {json.dumps(post.get('meta', {}), indent=2)}")
    
    # If custom fields are not exposed in 'meta', we can try the FinShift API endpoint if available, 
    # or just assume if I can't see it here, I might need to use a custom endpoint.
    # But wait, db/client.py uses /finshift/v1/daily-analysis which might return it?
    # No, daily-analysis endpoint returns the DB record, not WP Post Meta.
    # The WP Post Meta is stored in WP.
    
    # As an authorized user, I should be able to see meta if exposed.
    # But keys starting with _ are usually hidden from REST API unless explicitly registered.
    # I probably created the post with these keys using the exact same user.
    
    # Let's try to fetch via the custom finshift endpoint if I can query by ID? No.
    
    # Wait, simple test: `market-dashboard.php` uses `get_post_meta`.
    # I can write a small PHP script to check it if I could run PHP, but I have python.
    
    # I'll rely on the fact that I just pushed it. 
    # Let's check the 'daily-analysis' custom table record first via our DBClient.
    # Because `daily_briefing.py` saves to BOTH DB and WP.
    # If it is in the DB (daily-analysis endpoint), it *should* have been in the JSON used to create the post.
    
    pass

if __name__ == "__main__":
    check_latest_post()
