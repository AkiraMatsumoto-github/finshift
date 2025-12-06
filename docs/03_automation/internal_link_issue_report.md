# Internal Link Issue Report & Fix Plan

## 1. Issue Description
Generated articles contain internal link suggestions (e.g., "See also: ..."), but they appear as plain text instead of clickable hyperlinks in WordPress.

**Symptom:**
Text appears like: `* 倉庫の自動化に関心がある方は「記事タイトル」`
instead of a clickable link.

## 2. Cause Analysis
The issue is caused by a conflict between the **Internal Link Prompt** and the **Content Cleaning Logic** in `automation/generate_article.py`.

1.  **Prompt Instruction:**
    The `InternalLinkSuggester` instructs Gemini to insert links using **HTML `<a>` tags**:
    > "include them in the article using standard HTML <a> tags."

    Gemini correctly generates: `... <a href="url">Title</a> ...`

2.  **Cleaning Logic (The Culprit):**
    Before converting Markdown to HTML, `generate_article.py` applies a regex to strip HTML tags (originally intended to clean up `<br>` tags in tables).
    
    ```python
    # automation/generate_article.py (Line ~364)
    content = re.sub(r'<([^>]+)>', '', content)
    ```
    
    **This regex aggressively removes ALL HTML tags**, including the `<a>` tags generated for internal links. As a result, `<a href="...">Title</a>` becomes just `Title`.

## 3. Proposed Fix Policy
We will modify the system to rely on **Markdown syntax** for linking, which is robust against the HTML cleaner and natively supported by the pipeline.

### Step 1: Update Prompt Instructions
Modify `automation/generate_article.py` to instruct Gemini to use **Markdown Link Format** instead of HTML tags.

**Current:**
```text
include them in the article using standard HTML <a> tags.
```

**New:**
```text
include them in the article using standard Markdown link syntax: [Title](URL).
```

### Step 2: Verification
Since `generate_article.py` already performs Markdown-to-HTML conversion (`markdown.markdown(...)`) *after* the regex cleaning, the Markdown links `[Title](URL)` will be preserved by the cleaner and then correctly converted to `<a href="URL">Title</a>` by the library.

## 4. Workaround (If HTML is strictly required)
If we must use HTML tags for some reason, we would need to edit the regex to **allow** `<a>` tags while stripping others.
However, **Step 1 (Markdown approach)** is cleaner and less error-prone.

## 5. Next Action
- Modify `automation/generate_article.py` to update the link instruction prompt.
- Verify with a dry-run.

## 6. Verification Results
- **Date**: 2025-12-06
- **Test**: Dry-run with keyword "物流倉庫 自動化 メリット"
- **Result**: Links were correctly generated in Markdown format and preserved in the final output.
  > ...例えば、搬送業務を自動化するAGVについては、[中国産AGVとは？メリットと注意点を物流担当者向けに徹底解説](https://logishift.net/2025/12/05/post-55/)で詳しく解説しています...
- **Status**: Fixed.
