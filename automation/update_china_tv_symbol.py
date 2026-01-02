#!/usr/bin/env python3
"""
Update China Market Symbol
Updates the 'market_tv_symbol' and 'market_tv_desc' meta fields for the China Market page.
Target Symbol: 000888 (Shenzhen Component) or 000001 (Shanghai Composite) 
User requested 000888. It's likely 000888.SZ in TradingView, but user said "000888". 
We will use "000888" as symbol which usually maps to SZSE Component in TV.
"""

import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

try:
    from automation.wp_client import WordPressClient
except ImportError:
    print("Error: Could not import WordPressClient. Make sure you are in the project root.")
    sys.exit(1)

def update_china_symbol():
    wp = WordPressClient()
    
    # 1. Find the China Market Page
    print("Searching for China Market page...")
    pages = wp.get_pages_by_meta("market_region_tag", "china-market")
    
    if not pages:
        print("Error: China Market page not found.")
        return

    page = pages[0]
    page_id = page['id']
    print(f"Found page: {page['title']['rendered']} (ID: {page_id})")
    
    # 2. Update Meta
    # User requested 000888. 
    # In TradingView, 000888 is typically Shenzhen Component (if SZSE).
    # Common tickers: 000001.SS (Shanghai), 399001.SZ (Shenzhen).
    # However, user explicitly asked for "000888".
    # Often "000888" is a specific stock (e.g. EMS in China?). 
    # Wait, usually indices are 000001 (SSEC). 
    # But maybe user means 000888 stock? Or maybe an index like CSI 300? 
    # CSI 300 is 000300.
    # 
    # Let's assume user input "000888" is what they want passed to the widget.
    # We will use "000888" as symbol.
    
    new_symbol = "000888" 
    new_desc = "China Market" 

    meta_update = {
        "market_tv_symbol": new_symbol,
        "market_tv_desc": new_desc
    }
    
    print(f"Updating symbol to: {new_symbol}")
    
    result = wp.update_resource('pages', page_id, {"meta": meta_update})
    
    if result:
        print("✅ Successfully updated China Market symbol.")
    else:
        print("❌ Failed to update page.")

if __name__ == "__main__":
    update_china_symbol()
