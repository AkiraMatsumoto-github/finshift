# FinShift - 金融市場分析・投資情報メディア

世界の金融市場（株式、為替、コモディティ、暗号資産）の情報を収集し、スイングトレーダー向けに「市場分析」と「シナリオ」を提供する情報メディアです。
Gemini APIを活用した高度な自動生成システムにより、客観的な市場分析と投資シナリオを迅速に配信します。

## プロジェクト構成

```
.
├── themes/finshift/           # WordPressテーマ（独自開発）
├── automation/                # 自動化システム
│   ├── collectors/            # データ収集モジュール (News, Market Data, Calendar)
│   ├── daily_briefing.py      # デイリーブリーフィング生成 (Main)
│   ├── pipeline.py            # 記事生成パイプライン (Traditional)
│   ├── gemini_client.py       # Gemini APIクライアント
│   └── ...
├── docs/                      # プロジェクトドキュメント
└── .github/workflows/         # GitHub Actions (CI/CD)
```

---

## 1. Automation System

FinShiftの自動化システムは、ニュース収集から市場分析、記事生成、WordPress投稿までを一貫して行います。

### セットアップ (ローカル)

#### 必須要件
- Python 3.10+
- Gemini API Key

#### 手順

1.  **Python環境の準備**
    ```bash
    cd automation
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **環境変数の設定**
    `automation/.env` を作成:
    ```bash
    GEMINI_API_KEY=your_apiKey
    WORDPRESS_URL=http://localhost:8002
    WORDPRESS_USERNAME=admin
    WORDPRESS_APP_PASSWORD=your_appPassword
    ```

### 実行ガイド

#### A. デイリーブリーフィング (`daily_briefing.py`)
毎日の市場分析記事を生成するメインスクリプトです。各国のニュースと市場データを分析し、シナリオを作成します。

```bash
# 基本実行 (全リージョン、収集から分析・投稿まで)
python automation/daily_briefing.py

# 特定フェーズのみ実行
# phase 1: データ収集のみ
python automation/daily_briefing.py --phase collect
# phase 2: 分析・記事生成のみ (収集済みデータを使用)
python automation/daily_briefing.py --phase analyze

# リージョン指定 (US, JP, CN, IN, Crypto など)
python automation/daily_briefing.py --region US

# オプション
--hours 24       # ニュース収集の過去遡り時間 (デフォルト: 24)
--dry-run        # 投稿・DB保存を行わず、ログ出力のみ (テスト用)
```

#### B. 汎用記事パイプライン (`pipeline.py`)
キーワードベースや従来のパイプライン処理を行います。

```bash
# 基本実行
python automation/pipeline.py --hours 12 --threshold 75 --limit 2

# 全ソースから収集
python automation/collector.py --source all > articles.json

# 特定ソースのみ (例: TechCrunch)
python automation/collector.py --source techcrunch --days 3
```

**Phase 2: スコアリング (`scorer.py`)**
```bash
# ファイル入力でスコアリング
python automation/scorer.py --input articles.json --threshold 80 --output scored.json
```

**Phase 3: 固定ページ生成 (`generate_static_pages.py`)**
```bash
python automation/generate_static_pages.py --all
```

---

## 4. トラブルシューティング

### サーバー運用

#### gcloud 認証ができてない
```bash 
gcloud auth application-default login
```

#### パーミッションエラーでテーマが反映されない
```bash
ssh -p 10022 xs937213@sv16718.xserver.jp
chmod -R 755 ~/finshift.net/public_html/wp-content/themes/finshift
```

#### GitHub Actions のデプロイ失敗
GitHub Secrets (`Settings > Secrets`) を確認してください：
- `SERVER_HOST`: sv16718.xserver.jp
- `SERVER_USER`: xs937213
- `SSH_PORT`: 10022
- `SSH_PRIVATE_KEY`: (正しい秘密鍵か)

### ローカル開発
#### 環境立ち上げ
```bash
source automation/venv/bin/activate
export GOOGLE_CLOUD_LOCATION=global   
```

#### 記事が生成されない (スコア不足)
`pipeline.py` の `--threshold` デフォルト値(85)が高すぎる可能性があります。`--threshold 60` 程度に下げてお試しください。

## 関連ドキュメント
- [テーマデプロイガイド](docs/00_meta/theme_deployment_guide.md)
- [本番環境デプロイガイド](docs/00_meta/production_deployment_guide.md)
