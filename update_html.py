#!/usr/bin/env python3
"""
Update index.html with Reddit data
取得したRedditデータをindex.htmlに反映
"""

import json
import re

def update_index_html():
    """index.htmlを最新のRedditデータで更新"""
    
    # reddit_content.jsonを読み込み
    try:
        with open('reddit_content.json', 'r', encoding='utf-8') as f:
            new_content = json.load(f)
    except FileNotFoundError:
        print("❌ reddit_content.json not found")
        return False
    
    # index.htmlを読み込み
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("❌ index.html not found")
        return False
    
    # JavaScriptのcontentオブジェクトを更新
    # en の threads 部分だけを置き換え
    new_threads_json = json.dumps(new_content['en']['threads'], ensure_ascii=False, indent=20)
    
    # 正規表現でen: { threads: [...] } 部分を探して置き換え
    pattern = r"(en:\s*\{[^}]*threads:\s*\[).*?(\s*\])"
    replacement = f"\\1\n{new_threads_json}\n                \\2"
    
    updated_html = re.sub(
        pattern,
        replacement,
        html_content,
        flags=re.DOTALL
    )
    
    # 更新されたHTMLを保存
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    print("✅ index.html updated successfully")
    print(f"   Added {len(new_content['en']['threads'])} threads")
    return True

if __name__ == '__main__':
    success = update_index_html()
    exit(0 if success else 1)
