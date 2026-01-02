
import os
import sys
import json
from wp_client import WordPressClient
import collections

# Fake logic for testing
def run():
    print("Validating Front Page UI with sample data...")
    wp = WordPressClient()
    
    # 1. Get latest market analysis post
    cat_id = wp.get_category_id("market-analysis")
    posts = wp.get_posts(limit=1, category=cat_id, status="publish")
    
    if not posts:
        print("No market analysis posts found.")
        return

    target_post = posts[0]
    post_id = target_post['id']
    print(f"Target Post: {target_post['title']['rendered']} (ID: {post_id})")
    
    # 2. Prepare Sample Meta
    ai_summary = {
        "summary": "米雇用統計が市場予想を大幅に上回り、FRBの早期利下げ観測が後退しました。これを受けて米長期金利は4.16%へ急騰し、ハイテク株を中心に売り優勢の展開となっています。為替市場ではドル買いが加速し、ドル円は一時158円台へ突入。日経平均先物も下落しており、明日の東京市場は波乱含みのスタートとなりそうです。",
        "key_topics": ["US Jobs", "Interest Rates", "USD/JPY"]
    }
    
    meta_update = {
        "meta": {
            "_ai_structured_summary": json.dumps(ai_summary, ensure_ascii=False)
        }
    }
    
    # 3. Update Post
    print(f"Updating post {post_id} with sample meta: {json.dumps(ai_summary, ensure_ascii=False)}")
    res = wp.update_resource("posts", post_id, meta_update)
    
    if res:
        print("Update successful!")
        print("Please check the front page now.")
    else:
        print("Update failed.")

if __name__ == "__main__":
    run()
