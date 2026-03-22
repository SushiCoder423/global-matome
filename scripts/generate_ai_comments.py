#!/usr/bin/env python3
"""
AI Comment Generator for Global Matome
本物のコメント70% + AI生成30% でボリューム増強
"""

import json
import requests

def generate_ai_comments(original_post, real_comments, target_count=100):
    """
    AI でコメントを生成（Claude API使用）
    
    Args:
        original_post: 元投稿の本文
        real_comments: 本物のコメントリスト
        target_count: 生成するコメント数
    
    Returns:
        生成されたコメントのリスト
    """
    
    # 本物のコメントから雰囲気を学習
    sample_comments = real_comments[:10] if len(real_comments) >= 10 else real_comments
    
    prompt = f"""Generate {target_count} Reddit-style comments for this post. 
Make them feel natural and varied like real Reddit users.

Original Post:
{original_post}

Example of real comments from this thread:
{chr(10).join([f'- "{c}"' for c in sample_comments])}

Requirements:
1. Mix of helpful advice, jokes, sarcasm, and empathy
2. Vary length: some 5 words, some 50 words
3. Use casual language: "lol", "lmao", "fr fr", "💀"
4. Some should reference other comments (e.g., ">>45 this")
5. About 10% should be extremely funny/memorable
6. Keep them realistic - like actual Reddit users wrote them

Return ONLY a JSON array of comment texts, nothing else.
Example format: ["comment 1", "comment 2", ...]
"""

    # Claude API呼び出し（実際のAPIキーは不要、GitHubに設定済み）
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": "API_KEY_PLACEHOLDER"  # GitHub Secretsから注入
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 4000,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['content'][0]['text']
            
            # JSONをパース
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                comments = json.loads(json_match.group())
                return comments[:target_count]
        
        print(f"⚠️  AI generation failed, using fallback")
        return generate_fallback_comments(real_comments, target_count)
        
    except Exception as e:
        print(f"⚠️  AI API error: {e}, using fallback")
        return generate_fallback_comments(real_comments, target_count)


def generate_fallback_comments(real_comments, count):
    """
    API失敗時のフォールバック: テンプレートベース生成
    """
    templates = [
        "This happened to me too",
        "lmao",
        "www",
        "💀💀💀",
        "fr fr",
        "Classic mistake",
        "Been there",
        "F in the chat",
        "RIP",
        "How did you even",
        "I can't even",
        "This is why I",
        "Never doing that again",
        "Oof",
        "Big oof",
        "That's rough buddy",
        "You live and you learn",
        "Expensive lesson",
        "Could be worse",
        "At least you tried"
    ]
    
    # 本物のコメントを変形
    variations = []
    for comment in real_comments:
        # 語尾を変える
        variations.append(comment + " lol")
        variations.append(comment + " fr")
        variations.append(comment + " 💀")
    
    # テンプレートと変形を混ぜる
    all_options = templates + variations
    
    import random
    return random.sample(all_options * 10, min(count, len(all_options) * 10))


def detect_highlight_comments(comments, top_n=10):
    """
    特に面白いコメントを検出（強調表示用）
    
    Args:
        comments: コメントリスト
        top_n: 強調するコメント数
    
    Returns:
        コメントリスト（highlightフラグ付き）
    """
    scored_comments = []
    
    for idx, comment in enumerate(comments):
        score = 0
        text = comment.lower()
        
        # 短くてパンチがある
        if 5 < len(comment) < 30:
            score += 5
        
        # 笑いワード
        if any(w in text for w in ['lmao', 'lol', '💀', 'wwww', 'www']):
            score += 3
        
        # 全て大文字（叫んでる）
        if comment.isupper() and len(comment) > 3:
            score += 4
        
        # w が連続
        if 'www' in text or 'lol' in text:
            score += 2
        
        scored_comments.append({
            'index': idx,
            'text': comment,
            'score': score
        })
    
    # スコア順にソート
    scored_comments.sort(key=lambda x: x['score'], reverse=True)
    
    # Top N を強調
    highlight_indices = set([c['index'] for c in scored_comments[:top_n]])
    
    result = []
    for idx, comment in enumerate(comments):
        result.append({
            'text': comment,
            'highlight': idx in highlight_indices
        })
    
    return result


def augment_comments(original_post, real_comments, target_total=200):
    """
    本物のコメントをAI生成で増強
    
    Args:
        original_post: 元投稿
        real_comments: 本物のコメント（30-50個想定）
        target_total: 目標総数
    
    Returns:
        本物 + AI生成のコメントリスト
    """
    real_count = len(real_comments)
    needed = target_total - real_count
    
    print(f"📊 Real comments: {real_count}")
    print(f"🤖 Generating AI comments: {needed}")
    
    if needed <= 0:
        return real_comments
    
    # AI生成
    ai_comments = generate_ai_comments(original_post, real_comments, needed)
    
    # 統合
    all_comments = real_comments + ai_comments
    
    # 強調コメント検出
    enhanced = detect_highlight_comments(all_comments, top_n=15)
    
    # レス番号を付ける
    numbered = []
    for idx, comment in enumerate(enhanced, start=2):  # 1番は元投稿
        numbered.append({
            'num': idx,
            'text': comment['text'],
            'highlight': comment['highlight']
        })
    
    print(f"✅ Total comments: {len(numbered)}")
    print(f"⭐ Highlighted: {sum(1 for c in numbered if c['highlight'])}")
    
    return numbered


if __name__ == '__main__':
    # テスト
    test_post = "Spent $2000 on a PC and it doesn't boot"
    test_comments = [
        "Did you plug it in?",
        "Check RAM",
        "lmao",
        "Try reseating GPU"
    ]
    
    result = augment_comments(test_post, test_comments, target_total=50)
    
    print("\nSample output:")
    for comment in result[:10]:
        highlight_mark = "⭐" if comment['highlight'] else "  "
        print(f"{highlight_mark} {comment['num']}: {comment['text']}")
