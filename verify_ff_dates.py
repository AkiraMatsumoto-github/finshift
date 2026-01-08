import requests
import re
import json
from datetime import datetime, timedelta

def verify_dates():
    # Target Dates
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    target_dates = {
        today.strftime('%Y-%m-%d'),
        yesterday.strftime('%Y-%m-%d')
    }
    
    print(f"Checking for events on: {target_dates}")
    
    # URL (Monthly view)
    month_str = today.strftime("%b.%Y").lower()
    url = f"https://www.forexfactory.com/calendar?month={month_str}"
    print(f"Fetching {url}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        matches = re.finditer(r'(\{?"id":\d+,[^}]*?"impactName":"[^"]+"[^}]*?\})', resp.text)
        
        found_events = {}
        
        for m in matches:
            obj_str = m.group(1)
            if not obj_str.startswith('{'): obj_str = '{' + obj_str
            try:
                data = json.loads(obj_str)
                ts = data.get('dateline')
                if ts:
                    dt = datetime.fromtimestamp(int(ts))
                    d_str = dt.strftime('%Y-%m-%d')
                    
                    if d_str in target_dates:
                        if d_str not in found_events: found_events[d_str] = []
                        found_events[d_str].append(data)
            except:
                pass
                
        # Report
        for d in sorted(target_dates):
            events = found_events.get(d, [])
            print(f"\nDate: {d} - Found {len(events)} events.")
            for e in events:
                print(f"  [{e.get('currency')}] {e.get('name')} (Act: {e.get('actual')})")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_dates()
