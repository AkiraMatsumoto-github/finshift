# Wireframe: Single Post Page - Phase 1

## 概要
- **ファイル名**: `single.php`
- **役割**: 記事を読ませ、具体的な市場認識を提供する。
- **重要要素**: Disclaimer (免責), Readable Markdown Content, Region Context.

## Layout (Mobile First)

```text
+--------------------------------------------------+
| [Header (Sticky)]                                |
| [ < ]  Category / Title ...                      |
+--------------------------------------------------+
| [Hero Image (Vertex AI Gen)]                     |
| Text overlay: 記事タイトル                       |
+--------------------------------------------------+
| [Title Section]                                  |
| [Region: India] [Jan 01, 2026]                   |
| [Sentiment: Greed 80] [Regime: Risk-On]          |
| TATA Motors Q3 Earnings Surge                    |
+--------------------------------------------------+
| [ ! Disclaimer Box (Warning Color) ]             |
| "本記事は投資助言ではありません..."              |
+--------------------------------------------------+
| [Article Content (Markdown rendered)]            |
|                                                  |
| <h2>1. Market Pulse</h2>                         |
| 今日の市場は...                                  |
|                                                  |
| <h2>2. Analysis</h2>                             |
| テキスト...                                      |
| > **Important**: 引用や強調表示                   |
|                                                  |
| (Cross-Asset Impactなども本文内に記述)           |
+--------------------------------------------------+
| [Regional Chart Widget]                          |
| (TradingView Widget for Region e.g., NIFTY50)    |
| *記事ごとの個別銘柄ではなく地域代表指数を表示*   |
+--------------------------------------------------+
| [Actionable Insight (Text/Link)]                 |
| "インド市場を取引するなら..."                    |
| [Affiliate Link / Button]                        |
+--------------------------------------------------+
| [Related Scenarios]                              |
| - 同地域の過去記事リンク 1                       |
| - 同地域の過去記事リンク 2                       |
+--------------------------------------------------+
| [Footer]                                         |
+--------------------------------------------------+
```

## Desktop Layout
- **2 Column**:
    - **Main**: Article Content.
    - **Sidebar (Sticky)**:
        - **Regional Chart** (Nifty 50, S&P 500 etc).
        - **Related News**.
