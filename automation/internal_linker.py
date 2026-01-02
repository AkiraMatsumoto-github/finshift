import json
from typing import List, Dict, Optional

class InternalLinkSuggester:
    """
    Suggests relevant internal links for a new article based on existing content.
    Phase 1: One-way linking (New Article -> Existing Articles).
    """

    def __init__(self, wp_client, gemini_client):
        self.wp = wp_client
        self.gemini = gemini_client

    def fetch_candidates(self, limit: int = 100) -> List[Dict]:
        """
        Fetch existing posts from WordPress to serve as link candidates.
        Mixes recent posts and popular posts.
        """
        candidates = []
        seen_ids = set()

        # 1. Fetch Popular Posts (High PV)
        print("Fetching popular posts for internal linking...")
        try:
            popular_posts = self.wp.get_popular_posts(days=30, limit=20)
            if popular_posts:
                print(f"Found {len(popular_posts)} popular posts.")
                for post in popular_posts:
                    if post['id'] not in seen_ids:
                        candidates.append(self._process_post(post))
                        seen_ids.add(post['id'])
        except Exception as e:
            print(f"Warning: Failed to fetch popular posts: {e}")

        # 2. Fetch Recent Posts (Latest)
        # Reduce limit by number of popular posts found to keep total reasonable, or just add on top.
        # Let's target total 'limit' count.
        remaining_limit = max(10, limit - len(candidates))
        
        print(f"Fetching last {remaining_limit} recent posts...")
        recent_posts = self.wp.get_posts(limit=remaining_limit, status="publish")
        
        if recent_posts:
            for post in recent_posts:
                 if post['id'] not in seen_ids:
                    candidates.append(self._process_post(post))
                    seen_ids.add(post['id'])

        print(f"Total candidates loaded: {len(candidates)}")
        return candidates

    def _process_post(self, post) -> Dict:
        """Helper to process raw WP post into candidate dict."""
        ai_summary_json = None
        # Check meta location - standard API vs custom endpoint structure might differ slightly
        # get_posts returns dict directly. get_popular_posts returns similar struct.
        
        meta = post.get('meta', {})
        if '_ai_structured_summary' in meta:
             try:
                 # Check if it's already a dict (API sometimes expands) or string
                 summary_val = meta['_ai_structured_summary']
                 if isinstance(summary_val, str):
                    ai_summary_json = json.loads(summary_val)
                 elif isinstance(summary_val, dict):
                    ai_summary_json = summary_val
             except:
                 pass
        
        summary_text = ""
        title = post['title']['rendered']
        # Handle excerpt which might be an object {'rendered': ...} or string depending on endpoint
        excerpt_raw = post.get('excerpt', '')
        excerpt_text = excerpt_raw['rendered'] if isinstance(excerpt_raw, dict) else str(excerpt_raw)

        if ai_summary_json:
            summary_text = f"Title: {title}\nSummary: {ai_summary_json.get('summary', '')}\nTopics: {', '.join(ai_summary_json.get('key_topics', []))}"
        else:
            summary_text = f"Title: {title}\nExcerpt: {self._clean_excerpt(excerpt_text)}"

        return {
            "id": post['id'],
            "title": title,
            "url": post['link'] if 'link' in post else post.get('guid', {}).get('rendered', ''),
            "summary_context": summary_text,
            "excerpt": self._clean_excerpt(excerpt_text)
        }

    def score_relevance(self, new_article_keyword: str, new_article_context: str, candidates: List[Dict]) -> List[Dict]:
        """
        Score the relevance of candidate articles against the new article's topic.
        Returns a list of highly relevant articles (score >= 80).
        """
        if not candidates:
            return []

        print("Scoring candidate relevance with Gemini (Enhanced Context)...")
        
        # Prepare candidates for the prompt
        candidates_text = ""
        for c in candidates:
            # Use the rich summary context if available
            candidates_text += f"- ID: {c['id']} | {c['summary_context']}\n"

        prompt = f"""
        You are an SEO expert. We are writing a new article about "{new_article_keyword}".
        Context/Outline of new article: {new_article_context[:500]}...

        Evaluate the following existing articles and determine which ones are HIGHLY RELEVANT to the new article.
        Relevance means the existing article provides valuable supplementary information, detailed explanation of a sub-topic, or a related case study.
        
        Existing Articles:
        {candidates_text}

        Task:
        1. Rate each article's relevance from 0 to 100.
        2. Select only articles with valid relevance >= 80.
        3. Return the result in JSON format:
        [
            {{"id": 123, "title": "Title", "score": 95, "reason": "Explains the specific tech mentioned in new article"}},
            ...
        ]
        
        Output JSON only. If no articles are relevant, output [].
        """

        try:
            response = self.gemini.generate_content(prompt)
            if not response or not response.text:
                print("No response from Gemini for relevance scoring.")
                return []
                
            response_text = response.text
            # basic cleanup for code blocks if gemini adds them
            clean_text = response_text.replace('```json', '').replace('```', '').strip()
            results = json.loads(clean_text)
            
            # Map back to full candidate objects
            relevant_posts = []
            for res in results:
                if res['score'] >= 80:
                    # Find original candidate data
                    original = next((c for c in candidates if c['id'] == res['id']), None)
                    if original:
                        original['relevance_score'] = res['score']
                        original['relevance_reason'] = res.get('reason', '')
                        relevant_posts.append(original)
            
            # Sort by score desc
            relevant_posts.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            print(f"Found {len(relevant_posts)} highly relevant articles.")
            return relevant_posts[:5] # Return top 5 max

        except Exception as e:
            print(f"Error during relevance scoring: {e}")
            return []

    def _clean_excerpt(self, html_excerpt: str) -> str:
        """Remove HTML tags from excerpt for cleaner prompt usage."""
        # Simple tag removal
        import re
        clean = re.sub('<[^<]+?>', '', html_excerpt)
        return clean.strip()
