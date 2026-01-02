
import os
import sys
import json
from wp_client import WordPressClient

def run():
    print("Checking metadata for latest Market Analysis post...")
    wp = WordPressClient()
    
    # Get latest post ID dynamically
    cat_id = wp.get_category_id("market-analysis")
    print(f"Category ID for market-analysis: {cat_id}")
    posts = wp.get_posts(limit=1, category=cat_id, status="publish")
    
    if not posts:
        print("No market analysis posts found!")
        return
        
    post_id = posts[0]['id']
    print(f"Latest Post ID: {post_id} - {posts[0]['title']['rendered']}")
    
    # Authenticated request to see protected meta
    # Note: api_url already contains ?, so use & for parameters
    url = f"{wp.api_url}/posts/{post_id}&context=edit"
    print(f"Requesting URL: {url}")
    
    try:
        response = requests.get(url, auth=wp.auth)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return
            
        post = response.json()
        meta = post.get('meta', {})
        
        print("--- Meta Keys Found ---")
        for k, v in meta.items():
            if k.startswith('_finshift') or k.startswith('_ai'):
                print(f"{k}: {v}")
                
        # Check specific key
        summary_raw = meta.get('_ai_structured_summary')
        if summary_raw:
            print(f"\n_ai_structured_summary (Raw type: {type(summary_raw)}):")
            print(summary_raw)
            try:
                parsed = json.loads(summary_raw)
                print("JSON Parsed successfully:")
                print(parsed)
            except:
                print("Failed to parse JSON string.")
        else:
            print("\n_ai_structured_summary KEY NOT FOUND in meta.")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    import requests # Need to import locally if not available globally in this snippet scope, or ensure wp_client imports are enough
    run()
