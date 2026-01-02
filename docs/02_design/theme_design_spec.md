# FinShift テーマ実装仕様書 (Simplified)

メディアプランに基づき、"Financial Terminal" コンセプトを具体化するためのWordPressテーマ設計書です。
**「過度なカスタマイズを避け、まずは自動化されたコンテンツを最大限魅力的に見せる」** ことを最優先とします。

## 1. デザインコンセプト (Financial Terminal)
- **キーワード**: High Density, Data-Driven, Professional.
- **ビジュアル**: Bloomberg端末やTradingViewのような「黒基調」「数値重視」。
- **配色**:
    - **Background**: `#0F172A` (Slate 900) - Deep Navy.
    - **Card Surface**: `#1E293B` (Slate 800) - With brighter borders.
    - **Text Primary**: `#FFFFFF` (White) - Pure White for maximum contrast.
    - **Text Secondary**: `#CBD5E1` (Slate 300) - High readability gray.
    - **Border**: `#475569` (Slate 600) - Visible separation.
    - **Accent**: `#38BDF8` (Sky 400) - Links, highlights.
    - **Bull / Rise**: `#34D399` (Emerald 400).
    - **Bear / Fall**: `#F87171` (Red 400).
- **フォント**: `Inter` (英数字) + `Noto Sans JP` (日本語)。

## 2. サイト構造 (Page Hierarchy)

### A. トップページ (`front-page.php`)
サイトのダッシュボード。全ての重要情報が一目でわかる場所。

1.  **Global Ticker Widget (Top Bar)**
    - TradingView Ticker Tape Widgetを埋め込む。
    - 表示: S&P500, Nasdaq, Nikkei225, Nifty50, USDJPY, Bitcoin.
2.  **Market Pulse (Hero Section)**
    - **Left**: **"Global Sentiment"** (Fear & Greed).
        - データソース: Automationが `wp_options` に保存した最新スコアを表示。
        - ビジュアル: メーターゲージ または 単純な数値 ("Extreme Greed: 85")。
    - **Right**: **"Today's Scenarios"** (最新のDaily Briefingへのリンク).
        - US, JP, Crypto の最新記事をカード表示。
3.  **Latest News Stream**
    - 全記事のタイムライン。タブ切り替え (All / Stocks / Crypto / FX)。

### B. 記事詳細 (`single.php`)
スイングトレーダーが分析を行うワークスペース。

1.  **Header Area**
    - タイトル (H1)
    - **Meta Info**: 
        - Region Tag (例: `US`, `India`)
        - Market Regime (例: "Risk-Off") - カスタムフィールドから取得。
2.  **Content Area**
    - **Markdown Content**: Automationが生成したHTMLを表示。
    - **Tables**: マークダウンテーブルをCSSで美しく整形 (Sticky Header, Stripe)。
3.  **Sidebar (PC only)**
    - **Mini Chart**: 記事のRegionに応じた代表指数チャート (TradingView Mini Chart)。
    - **Related Scenarios**: 同一Regionの過去記事リンク。

### C. リージョンアーカイブ (`archive.php`) / (`taxonomy-region.php`)
特定の市場（例: インド株）だけを追いかけるためのページ。

1.  **Region Header**
    - リージョン名 (例: "India Market").
    - **Key Chart**: その国の代表指数チャート (TradingView Symbol Info)。
2.  **Article List**
    - そのリージョンの記事一覧。

## 3. データ連携仕様 (Data Binding)

Automation側からWordPressへ渡されるデータとその表示場所の定義です。

### 戦略的意義 (Strategic Value)
これらのメタデータ連携は、単なる「飾り」ではなく、本サイトを「ブログ」ではなく「金融ツール」に昇華させるために必須です。
1.  **Scan-ability (速報性)**: トレーダーはタイトルを読む前に「色（赤/緑）」と「数字（80）」で市場の温度感を0.5秒で判断できる。
2.  **Data Asset (資産価値)**: 「過去にRisk-Offだった日の記事」のような検証的検索が可能になり、再来訪の理由を作る。

| データ項目 | ソース (Python) | 保存先 (WordPress) | 表示場所 (Theme) | 実装ステータス |
| :--- | :--- | :--- | :--- | :--- |
| **記事本文** | `daily_briefing.py` | `post_content` | `single.php` | ✅ Implemented |
| **アイキャッチ** | `gemini_client.py` | `_thumbnail_id` | `front-page`, `archive` | ✅ Implemented |
| **Sentiment Score** | `daily_briefing.py` | **Post Meta**: `_finshift_sentiment` | `single.php` (Header) | ⚠️ **To Do** |
| **Market Regime** | `daily_briefing.py` | **Post Meta**: `_finshift_regime` | `single.php` (Header) | ⚠️ **To Do** |
| **Global Sentiment** | `daily_briefing.py` (US run) | **Option**: `finshift_global_sentiment` | `front-page.php` (Hero) | ⚠️ **To Do** |
| **Region Tag** | `daily_briefing.py` | **Tag**: `US`, `JP`, etc. | `single.php`, `archive` | ✅ Implemented |

## 4. 推奨コンポーネント実装順序

1.  **Data Binding補完**: Automation側で `To Do` のメタデータ送信を実装する (これが無いとFrontendで表示できない)。
2.  **Base Setup**: `functions.php` でCSS/JS読み込み、フォント設定。
3.  **Single Page**: 記事が正しく読める状態にする (Markdown Styleの整備)。
4.  **Front Page**: ダッシュボード化 (TradingView Widget埋め込み)。

この構成により、ミニマムで「使える」金融ターミナル用メディアを立ち上げます。
