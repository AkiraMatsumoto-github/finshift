
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from automation.gemini_client import GeminiClient
from dotenv import load_dotenv

# Force load .env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path, override=True)

def test():
    client = GeminiClient()
    print("Testing check_relevance_batch...")
    
    title = "Bitcoin hits $100k all time high"
    summary = "Cryptocurrency markets rally as institutional adoption grows."
    
    # Mock article dict
    article = {
        'url_hash': 'test_hash_123',
        'title': title,
        'summary': summary
    }
    
    results_map = client.check_relevance_batch([article])
    res = results_map.get('test_hash_123')
    
    print(f"Title: {title}")
    if res:
        print(f"Relevant: {res['is_relevant']}")
        print(f"Reason: '{res['reason']}'")
    else:
        print("Error: No result returned")

if __name__ == "__main__":
    test()
