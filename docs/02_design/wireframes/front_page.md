# Wireframe: Front Page (Dashboard) - Phase 1

## 概要
- **ファイル名**: `front-page.php`
- **役割**: "Pocket Bloomberg" - 一目で市場センチメントと今日のシナリオへのアクセスを提供する。
- **デザインコンセプト**: Dark Mode, High Density, Financial Terminal Style.

## Layout (Mobile First)

```text
+--------------------------------------------------+
| [Header (Sticky)]                                |
| [≡]  FINSHIFT  [🔍]                              |
| ------------------------------------------------ |
| [Global Ticker Widget (TradingView)]             |
| S&P500: 4,780 (+0.5%) | NK225: 38,500 (-0.2%) ...|
+--------------------------------------------------+
| [Hero Section: Market Pulse]                     |
|                                                  |
|  [ Global Sentiment Meter ]                      |
|  FEAR <-------[ 75 GREED ]------->               |
|  "Risk-On Environment"                           |
|                                                  |
|  [ Today's Scenarios (Latest Briefings) ]        |
|  +--------------------------------------------+  |
|  | �� US Briefing (Jan 01)                [>] |  |
|  | Risk-Off | Sentiment: Neutral              |  |
|  +--------------------------------------------+  |
|  | 🇯🇵 JP Briefing (Jan 01)                [>] |  |
|  | Risk-On  | Sentiment: Greed                |  |
|  +--------------------------------------------+  |
|  | ₿ Crypto Briefing (Jan 01)             [>] |  |
|  | Neutral  | Sentiment: Fear                 |  |
|  +--------------------------------------------+  |
+--------------------------------------------------+
| [Latest News Stream (Tabs)]                      |
| [ All ] [ Stocks ] [ Crypto ] [ FX ]             |
|                                                  |
| 20:30  [US] 米雇用統計、予想上回る強い数字       |
| 18:15  [Crypto] ビットコイン、節目をブレイク     |
| 15:00  [JP] 海外勢の買い越し幅が拡大             |
| ...                                              |
| [View All News >]                                |
+--------------------------------------------------+
| [Footer]                                         |
| [Terms] [Privacy] [Disclaimer]                   |
+--------------------------------------------------+
```

## Desktop Layout (> 768px)
- **2 Column Layout**:
    - **Main (Left/Center)**: Hero Section (Sentiment + Scenarios) & News Stream.
    - **Sidebar (Right)**:
        - **Market Movers / Watchlist Link**: (Phase 2 feature placeholer)
        - **AdSense / Affiliate Banners**.
- **Visuals**:
    - Dark background (`#0F172A`).
    - Use Red/Green colors only for data changes.
