# SEO実装計画: 構造化データ (Schema.org)

## 目的 (Goal)
検索やGoogle Discoverからのオーガニック流入を増やすために、**JSON-LD構造化データ**を実装します。これにより、Googleがコンテンツを「ニュース/記事」として理解し、「トップニュース」や「Discover（砲）」フィードに表示される可能性が大幅に高まります。

## ユーザー確認事項
- **検証**: 実装・デプロイ後、[Googleのリッチリザルトテスト](https://search.google.com/test/rich-results)を使用して正しく認識されるか検証してください。

## 変更内容 (Proposed Changes)

### [Theme] `finshift`

#### [MODIFY] [themes/finshift/header.php](file:///Users/matsumotoakira/Documents/Private_development/finshift/themes/finshift/header.php)
- `<head>`タグ内に新しい関数 `finshift_output_schema_json()` の呼び出しを追加します（またはfunctions.phpで `wp_head` にフックします）。

#### [MODIFY] [themes/finshift/functions.php](file:///Users/matsumotoakira/Documents/Private_development/finshift/themes/finshift/functions.php)
- `finshift_output_schema_json()` 関数を実装します。
- **ロジック**:
    - `is_single()` の場合: `NewsArticle` または `BlogPosting` スキーマを出力。
    - `is_front_page()` の場合: `WebSite` スキーマ（SearchAction付き）を出力。
    - `is_category()` の場合: `CollectionPage` スキーマを出力。
- **スキーマプロパティ**:
    - `headline`: 記事タイトル
    - `datePublished`: 公開日時 (ISO 8601形式)
    - `dateModified`: 更新日時 (ISO 8601形式)
    - `image`: アイキャッチ画像URL（Google Discover表示に必須）
    - `author`: 著者名 ("FinShift AI" 等)
    - `publisher`: 発行元組織 (FinShift) のロゴと名前

## 検証計画 (Verification Plan)

### 自動テスト
- なし（完全なWordPress環境がないとPHP出力のテストは困難なため）。

### 手動検証
1.  **ソースコード確認**: 記事ページやトップページのソースを表示し、`<script type="application/ld+json">` タグが出力されているか確認します。
2.  **バリデータ**: 出力されたJSON-LDコードをコピーし、[Schema Validator](https://validator.schema.org/) や [リッチリザルトテスト](https://search.google.com/test/rich-results) でエラーがないか検証します。
