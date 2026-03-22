#!/usr/bin/env python3
"""
Reddit Auto-Fetcher for Global Matome
毎日4回自動でRedditから人気投稿を取得
"""

import json
import requests
from datetime import datetime

REDDIT_API = "https://www.reddit.com"
USER_AGENT = "GlobalMatome/1.0"

# 20サブレディットに拡大
SUBREDDITS = {
    'en': [
        'pcmasterrace',
        'antiwork',
        'todayilearned',
        'LifeProTips',
        'mildlyinteresting',
        'gaming',
        'technology',
        'Showerthoughts',
        'explainlikeimfive',
        'oddlysatisfying',
        'nextfuckinglevel',
        'Damnthatsinteresting',
        'interestingasfuck',
        'WTF',
        'facepalm',
        'therewasanattempt',
        'instant_regret',
        'Wellthatsucks',
        'PublicFreakout',
        'aww'
    ]
}

TITLE_TEMPLATES = {
    'sad': ['【Sad News】', '【Breaking】', '【Fail】'],
    'happy': ['【Good News】', '【Win】', '【Success】'],
    'pic': ['【Pic】', '【Image】', '【Look】'],
    'help': ['【Help】', '【Question】', '【Urgent】'],
    'wtf': ['【WTF】', '【Crazy】', '【Wild】']
}

ENDINGS = ['lmao', '💀', 'lol', 'fr fr']

def get_reddit_hot_posts(subreddit, limit=5):
    """Redditから人気投稿を取得（1回あたり5件に削減）"""
    url = f"{REDDIT_API}/r/{subreddit}/hot.json"
    headers = {'User-Agent': USER_AGENT}
    params = {'limit': limit}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for post in data['data']['children']:
            p = post['data']
            
            score = p.get('score', 0)
            comments = p.get('num_comments', 0)
            
            # 基準を緩和: アップ票500以上、またはコメント50以上
            if score >= 500 or comments >= 50:
                # 本文を取得（selftext）
                body = p.get('selftext', '')
                if len(body) > 500:
                    body = body[:500] + '...'
                
                posts.append({
                    'title': p['title'],
                    'body': body if body else '[No text content]',
                    'score': score,
                    'comments': comments,
                    'url': f"https://reddit.com{p['permalink']}",
                    'subreddit': subreddit
                })
        
        return posts
    except Exception as e:
        print(f"Error fetching {subreddit}: {e}")
        return []

def detect_post_mood(title, body=''):
    """投稿の雰囲気を自動判定"""
    text = (title + ' ' + body).lower()
    
    if any(word in text for word in ['broke', 'fail', 'broken', 'doesn\'t work', 'quit', 'fired', 'lost', 'died']):
        return 'sad'
    
    if any(word in text for word in ['wtf', 'crazy', 'insane', 'wild', 'unbelievable']):
        return 'wtf'
    
    if any(word in text for word in ['success', 'won', 'finally', 'achievement', 'proud', 'happy']):
        return 'happy'
    
    if any(word in text for word in ['picture', 'photo', 'image', 'look at', 'check out']):
        return 'pic'
    
    if any(word in text for word in ['how to', 'help', 'question', 'advice', 'eli5']):
        return 'help'
    
    return 'sad'

def convert_to_nanj_style(post):
    """なんJ風タイトルに変換"""
    mood = detect_post_mood(post['title'], post.get('body', ''))
    prefix = TITLE_TEMPLATES[mood][0]
    ending = ENDINGS[0]
    
    title = post['title']
    if len(title) > 80:
        title = title[:77] + '...'
    
    return f"{prefix} {title} {ending}"

def get_related_products(post_title, post_body=''):
    """投稿内容から関連商品を自動判定"""
    text = (post_title + ' ' + post_body).lower()
    
    if any(word in text for word in ['pc', 'computer', 'gaming', 'build']):
        return [
            {'icon': '🔧', 'text': 'PC Diagnostic Tools', 'keyword': 'pc+diagnostic+tools'},
            {'icon': '🛠️', 'text': 'PC Parts', 'keyword': 'gaming+pc+parts'}
        ]
    
    if any(word in text for word in ['quit', 'job', 'work', 'boss', 'career']):
        return [
            {'icon': '📚', 'text': 'Career Books', 'keyword': 'career+change+books'},
            {'icon': '💻', 'text': 'Work From Home', 'keyword': 'home+office+setup'}
        ]
    
    if any(word in text for word in ['food', 'cook', 'recipe', 'eat']):
        return [
            {'icon': '🍳', 'text': 'Cooking Tools', 'keyword': 'cooking+tools'},
            {'icon': '📖', 'text': 'Recipe Books', 'keyword': 'cookbook'}
        ]
    
    if any(word in text for word in ['game', 'gaming', 'play']):
        return [
            {'icon': '🎮', 'text': 'Gaming Gear', 'keyword': 'gaming+accessories'},
            {'icon': '🕹️', 'text': 'Controllers', 'keyword': 'gaming+controller'}
        ]
    
    return [
        {'icon': '🛒', 'text': 'Shop on Amazon', 'keyword': 'popular+items'}
    ]

def generate_emoji(subreddit, title):
    """絵文字を自動選択"""
    title_lower = title.lower()
    
    if 'pc' in title_lower or 'computer' in title_lower:
        return '🖥️'
    if 'cat' in title_lower or 'dog' in title_lower or 'pet' in title_lower:
        return '🐱'
    if 'food' in title_lower:
        return '🍔'
    if 'work' in title_lower or 'job' in title_lower:
        return '💼'
    if 'money' in title_lower or 'paid' in title_lower:
        return '💰'
    if 'game' in title_lower or 'gaming' in title_lower:
        return '🎮'
    
    subreddit_emojis = {
        'pcmasterrace': '🖥️',
        'antiwork': '💼',
        'todayilearned': '📚',
        'LifeProTips': '💡',
        'mildlyinteresting': '👀',
        'gaming': '🎮',
        'technology': '📱',
        'aww': '🐱'
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
    print(f"📡 Fetching from {len(SUBREDDITS['en'])} subreddits...")
    
    for subreddit in SUBREDDITS['en']:
        print(f"  📡 Fetching r/{subreddit}...")
        posts = get_reddit_hot_posts(subreddit, limit=10)
        
        # Top 5のみ取得
        for post in posts[:5]:
            emoji = generate_emoji(subreddit, post['title'])
            nanj_title = convert_to_nanj_style(post)
            products = get_related_products(post['title'], post.get('body', ''))
            
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
                'body': post.get('body', ''),
                'source': f"r/{subreddit}",
                'upvotes': post['score'],
                'comments': post['comments'],
                'products': product_links,
                'original_url': post['url']
            }
            
            all_content['en']['threads'].append(thread_data)
            print(f"    ✅ Added: {nanj_title[:50]}...")
    
    print(f"\n✅ Total posts fetched: {len(all_content['en']['threads'])}")
    print(f"📊 Target: 100 posts (20 subreddits × 5 posts)")
    return all_content

def save_to_json(content, filename='reddit_content.json'):
    """JSONファイルに保存"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved to {filename}")

if __name__ == '__main__':
    content = fetch_all_posts()
    save_to_json(content)
    print("\n🎉 Done! Content updated successfully.")
