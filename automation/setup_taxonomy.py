#!/usr/bin/env python3
"""
Setup WordPress Categories and Tags based on content_strategy.md
"""

try:
    from automation.wp_client import WordPressClient
except ImportError:
    from wp_client import WordPressClient

import requests

def create_categories(wp):
    """Create all categories defined in content strategy."""
    categories = [
        {
            "name": "物流DX・トレンド",
            "slug": "logistics-dx",
            "description": "物流DX（デジタルトランスフォーメーション）の最新トレンドから、2024年問題をはじめとする法規制への対応策、AI・IoT・ロボティクスを活用した次世代の物流戦略まで、業界変革に不可欠な情報を網羅。経営層や現場リーダーが知っておくべき、持続可能な物流構築のための実践的なノウハウをお届けします。"
        },
        {
            "name": "倉庫管理・WMS",
            "slug": "warehouse-management",
            "description": "WMS（倉庫管理システム）の選定・導入ガイドから、在庫管理の適正化、ピッキング作業の効率化、庫内オペレーションの改善手法までを徹底解説。人手不足を解消し、生産性を最大化するための倉庫DXノウハウを提供します。"
        },
        {
            "name": "輸配送・TMS",
            "slug": "transportation",
            "description": "TMS（輸配送管理システム）による配車計画の自動化、求荷求車システムの活用、ラストワンマイル配送の最適化など、輸送効率を劇的に改善するソリューションを紹介。2024年問題に伴うドライバー不足対策や、運送コスト削減の実践的なアプローチを提案します。"
        },
        {
            "name": "マテハン・ロボット",
            "slug": "material-handling",
            "description": "自動倉庫（AS/RS）、AGV（無人搬送車）、AMR（自律走行搬送ロボット）、RFIDなど、最新のマテリアルハンドリング機器とロボティクス技術を網羅。省人化・無人化を実現する自動化設備の導入事例や、投資対効果を高めるための選定ポイントを解説します。"
        },
        {
            "name": "サプライチェーン",
            "slug": "supply-chain",
            "description": "SCM（サプライチェーン・マネジメント）の全体最適化、調達物流の改善、グローバルロジスティクスの戦略立案まで、サプライチェーン強靱化のための知見を深掘り。不確実性の高い現代において、リスクヘッジと競争優位性を両立するための戦略的ロジスティクス論を展開します。"
        },
        {
            "name": "事例・インタビュー",
            "slug": "case-studies",
            "description": "物流改革に成功した先進企業の具体的な取り組み事例や、業界トップランナーへの独占インタビューを掲載。DX推進の苦労話から成功の秘訣、現場のリアルな声まで、他社の実践から学べる貴重な一次情報をお届けします。"
        },
        {
            "name": "ニュース・海外",
            "slug": "news-global",
            "description": "米国、中国、欧州など、世界の物流テック最前線をレポート。海外の最新スタートアップ動向、ユニコーン企業の戦略、クロスボーダーECのトレンドなど、日本の物流業界に影響を与えるグローバルニュースをいち早く解説します。"
        },
    ]
    
    print("Creating/Updating categories...")
    for cat in categories:
        try:
            # 1. Try to create
            url = f"{wp.api_url}/categories"
            response = requests.post(url, json=cat, auth=wp.auth)
            
            if response.status_code == 201:
                print(f"✓ Created category: {cat['name']}")
            elif response.status_code == 400 and "term_exists" in response.text:
                # 2. If exists, update
                print(f"- Category already exists: {cat['name']}. Updating...")
                
                # Get existing category ID
                # Since api_url already contains ?rest_route=..., we must use & for parameters
                get_url = f"{wp.api_url}/categories&slug={cat['slug']}"
                get_res = requests.get(get_url, auth=wp.auth)
                
                if get_res.status_code == 200 and len(get_res.json()) > 0:
                    cat_id = get_res.json()[0]['id']
                    update_url = f"{wp.api_url}/categories/{cat_id}"
                    # Update description
                    update_res = requests.post(update_url, json={'description': cat['description']}, auth=wp.auth)
                    
                    if update_res.status_code == 200:
                         print(f"  ✓ Updated description for: {cat['name']}")
                    else:
                         print(f"  ✗ Failed to update description: {update_res.text}")
                else:
                    print(f"  ✗ Could not find existing category ID for slug: {cat['slug']}")

            else:
                print(f"✗ Failed to create {cat['name']}: {response.text}")
        except Exception as e:
            print(f"✗ Error processing {cat['name']}: {e}")

def create_tags(wp):
    """Create all tags defined in content strategy."""
    tags = [
        # Industry
        {"name": "製造業", "slug": "manufacturing"},
        {"name": "小売・流通", "slug": "retail"},
        {"name": "EC・通販", "slug": "ecommerce"},
        {"name": "3PL・倉庫", "slug": "3pl-warehouse"},
        {"name": "食品・飲料", "slug": "food-beverage"},
        {"name": "アパレル", "slug": "apparel"},
        {"name": "医薬品・医療", "slug": "medical"},
        # Theme
        {"name": "コスト削減", "slug": "cost-reduction"},
        {"name": "人手不足対策", "slug": "labor-shortage"},
        {"name": "品質向上・誤出荷防止", "slug": "quality-improvement"},
        {"name": "環境・SDGs", "slug": "environment-sdgs"},
        {"name": "安全・BCP", "slug": "safety-bcp"},
        {"name": "補助金・助成金", "slug": "subsidy"},
        # Region/Country
        {"name": "日本", "slug": "japan"},
        {"name": "アメリカ", "slug": "usa"},
        {"name": "ヨーロッパ", "slug": "europe"},
        {"name": "中国", "slug": "china"},
        {"name": "東南アジア", "slug": "southeast-asia"},
        {"name": "グローバル", "slug": "global"},
    ]
    
    print("\nCreating tags...")
    for tag in tags:
        try:
            url = f"{wp.api_url}/tags"
            response = requests.post(url, json=tag, auth=wp.auth)
            if response.status_code == 201:
                print(f"✓ Created tag: {tag['name']}")
            elif response.status_code == 400 and "term_exists" in response.text:
                print(f"- Tag already exists: {tag['name']}")
            else:
                print(f"✗ Failed to create {tag['name']}: {response.text}")
        except Exception as e:
            print(f"✗ Error creating {tag['name']}: {e}")

def main():
    print("=== WordPress Taxonomy Setup ===\n")
    try:
        wp = WordPressClient()
        create_categories(wp)
        create_tags(wp)
        print("\n✓ Setup complete!")
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")

if __name__ == "__main__":
    main()
