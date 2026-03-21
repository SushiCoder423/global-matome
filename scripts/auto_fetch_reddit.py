#!/usr/bin/env python3
"""
Reddit Auto-Fetcher for Global Matome
毎日自動でRedditから人気投稿を取得してサイトを更新
"""

import json
import requests
from datetime import datetime

# Reddit API設定（認証不要の公開API使用）
REDDIT_API = "https://www.reddit.com"
USER_AGENT = "GlobalMatome/1.0"

# 取得するサブレディット
SUBREDDITS = {
    'en': [
        'pcmasterrace',
        'antiwork', 
        'todayilearned',
        'LifeProTips',
        'mildlyinteresting'
    ]
}

# なんJ風タイトルテンプレート
TITLE_TEMPLATES = {
    'sad': ['【Sad News】', '【Breaking】'],
    'happy': ['【Good News】', '【Win】'],
    'pic': ['【Pic】', '【Image】'],
    'help': ['【Help】', '【Question】']
}

ENDINGS = ['lmao', '💀', 'lol']

def get_reddit_hot_posts(subreddit, limit=5):
    """Redditから人気投稿を取得"""
    url = f"{REDDIT_API}/r/{subreddit}/hot.json"
    headers = {'User-Agent': USER_AGENT}
    params = {'limit': limit}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for post in data['data']['children']:
            p = post['data']
            
            # 伸びてる記事を判別
            score = p.get('score', 0)
            comments = p.get('num_comments', 0)
            
            # 基準: アップ票1000以上、またはコメント100以上
            if score >= 1000 or comments >= 100:
                posts.append({
                    'title': p['title'],
                    'score': score,
                    'comments': comments,
                    'url': f"https://reddit.com{p['permalink']}",
                    'subreddit': subreddit
                })
        
        return posts
    except Exception as e:
        print(f"Error fetching {subreddit}: {e}")
        return []

def detect_post_mood(title):
    """投稿の雰囲気を自動判定"""
    title_lower = title.lower()
    
    # ネガティブワード
    if any(word in title_lower for word in ['broke', 'fail', 'broken', 'doesn\'t work', 'quit', 'fired']):
        return 'sad'
    
    # ポジティブワード
    if any(word in title_lower for word in ['success', 'won', 'finally', 'achievement', 'proud']):
        return 'happy'
    
    # 画像系
    if any(word in title_lower for word in ['picture', 'photo', 'image', 'look at']):
        return 'pic'
    
    # 質問・ヘルプ
    if any(word in title_lower for word in ['how to', 'help', 'question', 'advice']):
        return 'help'
    
    # デフォルトはsad（なんJっぽい）
    return 'sad'

def convert_to_nanj_style(post):
    """なんJ風タイトルに変換"""
    mood = detect_post_mood(post['title'])
    prefix = TITLE_TEMPLATES[mood][0]
    ending = ENDINGS[0]  # lmao
    
    # タイトルを短縮（長すぎる場合）
    title = post['title']
    if len(title) > 80:
        title = title[:77] + '...'
    
    nanj_title = f"{prefix} {title} {ending}"
    
    return nanj_title

def get_related_products(post_title):
    """投稿内容から関連商品を自動判定"""
    title_lower = post_title.lower()
    
    # キーワードマッチング
    if 'pc' in title_lower or 'computer' in title_lower:
        return [
            {'icon': '🔧', 'text': 'PC Diagnostic Tools', 'keyword': 'pc+diagnostic+tools'},
            {'icon': '🛠️', 'text': 'PC Parts', 'keyword': 'gaming+pc+parts'}
        ]
    
    if 'quit' in title_lower or 'job' in title_lower or 'work' in title_lower:
        return [
            {'icon': '📚', 'text': 'Career Books', 'keyword': 'career+change+books'},
            {'icon': '💻', 'text': 'Work From Home', 'keyword': 'home+office+setup'}
        ]
    
    if 'food' in title_lower or 'cook' in title_lower or 'recipe' in title_lower:
        return [
            {'icon': '🍳', 'text': 'Cooking Tools', 'keyword': 'cooking+tools'},
            {'icon': '📖', 'text': 'Recipe Books', 'keyword': 'cookbook'}
        ]
    
    # デフォルト
    return [
        {'icon': '🛒', 'text': 'Shop on Amazon', 'keyword': 'popular+items'}
    ]

def generate_emoji(subreddit, title):
    """絵文字を自動選択"""
    title_lower = title.lower()
    
    if 'pc' in title_lower or 'computer' in title_lower:
        return '🖥️'
    if 'cat' in title_lower or 'dog' in title_lower:
        return '🐱'
    if 'food' in title_lower:
        return '🍔'
    if 'work' in title_lower or 'job' in title_lower:
        return '💼'
    if 'money' in title_lower:
        return '💰'
    
    # サブレディット別デフォルト
    subreddit_emojis = {
        'pcmasterrace': '🖥️',
        'antiwork': '💼',
        'todayilearned': '📚',
        'LifeProTips': '💡',
        'mildlyinteresting': '👀'
    }
    
    return subreddit_emojis.get(subreddit, '📰')

def fetch_all_posts():
    """全サブレディットから投稿を取得"""
    all_content = {
        'en': {
            'siteTitle': '🌍 Global Matome',
            'tagline': 'Daily viral posts from discussion boards worldwide!',
            'productsTitle': '💡 Related:',
            'footerText': '© 2024 Global Matome | Aggregating discussion boards worldwide',
            'footerDisclaimer': 'Content sourced from public discussion boards. Original posts belong to their respective authors.',
            'threads': []
        }
    }
    
    print(f"🌍 Starting Reddit fetch at {datetime.now()}")
    
    for subreddit in SUBREDDITS['en']:
        print(f"📡 Fetching r/{subreddit}...")
        posts = get_reddit_hot_posts(subreddit, limit=10)
        
        # Top 3のみ取得
        for post in posts[:3]:
            emoji = generate_emoji(subreddit, post['title'])
            nanj_title = convert_to_nanj_style(post)
            products = get_related_products(post['title'])
            
            # 商品リンク生成
            product_links = []
            for p in products:
                product_links.append({
                    'icon': p['icon'],
                    'text': p['text'],
                    'url': f"https://amazon.com/s?k={p['keyword']}&tag=livewellpicks-20"
                })
            
            thread_data = {
                'emoji': emoji,
                'title': nanj_title,
                'source': f"r/{subreddit}",
                'upvotes': post['score'],
                'comments': post['comments'],
                'products': product_links
            }
            
            all_content['en']['threads'].append(thread_data)
            print(f"  ✅ Added: {nanj_title[:50]}...")
    
    print(f"\n✅ Total posts fetched: {len(all_content['en']['threads'])}")
    return all_content

def save_to_json(content, filename='reddit_content.json'):
    """JSONファイルに保存"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved to {filename}")

if __name__ == '__main__':
    # 投稿を取得
    content = fetch_all_posts()
    
    # JSONに保存
    save_to_json(content)
    
    print("\n🎉 Done! Content updated successfully.")
    print("Next: Update index.html with this content")
