#!/usr/bin/env node

/**
 * Global Matome Data Fetcher
 * 世界中の掲示板から自動でデータ取得
 * 
 * 実行: node scripts/fetch-data.js
 * GitHub Actionsで1日1回自動実行
 */

const fs = require('fs');
const path = require('path');

// なんJ型タイトル生成
const titleTemplates = {
  sad: ['【悲報】', '【速報】', '【悲報】'],
  happy: ['【朗報】', '【速報】'],
  request: ['【急募】', '【相談】'],
  image: ['【画像】', '【動画】'],
  question: ['【疑問】', '【質問】'],
};

const endings = [
  'した結果ｗｗｗｗｗ',
  'してて草',
  'で打線組んだｗｗｗ',
  'ンゴｗｗｗ',
  '、無事死亡',
];

function generateNanJTitle(originalTitle, mood = 'sad') {
  const prefix = titleTemplates[mood][Math.floor(Math.random() * titleTemplates[mood].length)];
  const ending = endings[Math.floor(Math.random() * endings.length)];
  
  return `${prefix}${originalTitle}${ending}`;
}

// 繁体字→簡体字変換マップ（簡易版）
const t2sMap = {
  '繁體': '繁体',
  '網友': '网友',
  '臺灣': '台湾',
  '鄉民': '乡民',
  '畫像': '画像',
  '電腦': '电脑',
  '軟體': '软件',
  '資訊': '资讯',
  // ... 実際には完全な変換ライブラリを使用
};

function convertToSimplified(text) {
  let result = text;
  Object.entries(t2sMap).forEach(([trad, simp]) => {
    result = result.replace(new RegExp(trad, 'g'), simp);
  });
  return result;
}

// Reddit API取得（実装例）
async function fetchReddit(subreddit = 'all', limit = 25) {
  try {
    const url = `https://www.reddit.com/r/${subreddit}/hot.json?limit=${limit}`;
    console.log(`Fetching Reddit: ${url}`);
    
    // 実際のAPI呼び出し（要認証設定）
    // const response = await fetch(url, {
    //   headers: { 'User-Agent': 'GlobalMatome/1.0' }
    // });
    // const data = await response.json();
    
    // デモデータ（実装時は上記をアンコメント）
    return [
      {
        title: 'My PC build cost $2000 and won\'t boot',
        subreddit: 'pcmasterrace',
        score: 12500,
        num_comments: 247,
        url: 'https://reddit.com/r/pcmasterrace/example',
        created_utc: Date.now() / 1000,
      },
      {
        title: 'Tried Japanese vending machine for the first time',
        subreddit: 'Japan',
        score: 8900,
        num_comments: 156,
        url: 'https://reddit.com/r/japan/example',
        created_utc: Date.now() / 1000,
      },
    ];
  } catch (error) {
    console.error('Reddit fetch error:', error);
    return [];
  }
}

// Twitter API取得
async function fetchTwitter(lang = 'en', count = 20) {
  try {
    console.log(`Fetching Twitter trending (${lang})`);
    
    // 実際のTwitter API v2呼び出し
    // const response = await fetch('https://api.twitter.com/2/tweets/search/recent', {
    //   headers: { 'Authorization': `Bearer ${process.env.TWITTER_BEARER_TOKEN}` }
    // });
    
    return [
      {
        text: 'Just built my first PC and it exploded',
        author: '@techbro',
        likes: 5600,
        retweets: 890,
        created_at: new Date().toISOString(),
      },
    ];
  } catch (error) {
    console.error('Twitter fetch error:', error);
    return [];
  }
}

// PTT取得（台湾掲示板）
async function fetchPTT(board = 'Gossiping', limit = 20) {
  try {
    console.log(`Fetching PTT board: ${board}`);
    
    // PTT APIまたはスクレイピング
    // const response = await fetch(`https://www.ptt.cc/bbs/${board}/index.html`);
    
    return [
      {
        title: '買了雞排結果是素的',
        author: 'anonymous',
        push_count: 345,
        board: 'Gossiping',
        url: 'https://ptt.cc/example',
        date: new Date().toISOString(),
      },
    ];
  } catch (error) {
    console.error('PTT fetch error:', error);
    return [];
  }
}

// JeuxVideo.com取得（フランス - 超巨大掲示板）
async function fetchJeuxVideoCom(forum = '18-25', limit = 20) {
  try {
    console.log(`Fetching JeuxVideo.com: ${forum}`);
    
    return [
      {
        title: 'J\'ai acheté une baguette molle au supermarché',
        author: 'khey123',
        replies: 892,
        views: 34500,
        url: 'https://jeuxvideo.com/example',
        created: new Date().toISOString(),
      },
      {
        title: 'Ma connexion internet en Afrique: 2MB/s pour 100€/mois',
        author: 'user_cd',
        replies: 445,
        views: 18900,
        url: 'https://jeuxvideo.com/example2',
        created: new Date().toISOString(),
      },
    ];
  } catch (error) {
    console.error('JeuxVideo.com fetch error:', error);
    return [];
  }
}

// Forocoches取得（スペイン）
async function fetchForocoches(section = 'general', limit = 20) {
  try {
    console.log(`Fetching Forocoches: ${section}`);
    
    return [
      {
        title: 'Compré un coche usado y encontré jamón en el maletero',
        author: 'usuario123',
        replies: 423,
        views: 15600,
        url: 'https://forocoches.com/example',
        created: new Date().toISOString(),
      },
    ];
  } catch (error) {
    console.error('Forocoches fetch error:', error);
    return [];
  }
}

// Hardmob取得（ブラジル）
async function fetchHardmob(forum = 'geral', limit = 20) {
  try {
    console.log(`Fetching Hardmob: ${forum}`);
    
    return [
      {
        title: 'Instalei PC Gamer e a conta de luz veio R$800',
        author: 'user_br',
        replies: 567,
        likes: 18900,
        url: 'https://hardmob.com.br/example',
        created: new Date().toISOString(),
      },
    ];
  } catch (error) {
    console.error('Hardmob fetch error:', error);
    return [];
  }
}

// データ統合・変換
async function aggregateData() {
  console.log('🌍 Starting global data aggregation...\n');
  
  const data = {
    en: [],
    es: [],
    pt: [],
    fr: [],
    'zh-TW': [],
    'zh-CN': [],
    lastUpdate: new Date().toISOString(),
  };
  
  // 英語圏データ
  console.log('📡 Fetching English sources...');
  const redditData = await fetchReddit('all', 25);
  const twitterData = await fetchTwitter('en', 20);
  
  data.en = redditData.map(post => ({
    id: Math.random().toString(36).substr(2, 9),
    title: generateNanJTitle(post.title, 'sad'),
    originalTitle: post.title,
    source: `r/${post.subreddit}`,
    comments: post.num_comments,
    upvotes: post.score,
    url: post.url,
    thumbnail: getEmojiForTopic(post.title),
    lang: 'en',
  }));
  
  // スペイン語圏データ
  console.log('📡 Fetching Spanish sources...');
  const forocochesData = await fetchForocoches();
  
  data.es = forocochesData.map(post => ({
    id: Math.random().toString(36).substr(2, 9),
    title: generateNanJTitle(post.title, 'sad'),
    originalTitle: post.title,
    source: 'Forocoches',
    comments: post.replies,
    upvotes: post.views,
    url: post.url,
    thumbnail: getEmojiForTopic(post.title),
    lang: 'es',
  }));
  
  // ポルトガル語圏データ
  console.log('📡 Fetching Portuguese sources...');
  const hardmobData = await fetchHardmob();
  
  data.pt = hardmobData.map(post => ({
    id: Math.random().toString(36).substr(2, 9),
    title: generateNanJTitle(post.title, 'sad'),
    originalTitle: post.title,
    source: 'Hardmob',
    comments: post.replies,
    upvotes: post.likes,
    url: post.url,
    thumbnail: getEmojiForTopic(post.title),
    lang: 'pt',
  }));
  
  // フランス語圏データ
  console.log('📡 Fetching French sources...');
  const jvcData = await fetchJeuxVideoCom();
  
  data.fr = jvcData.map(post => ({
    id: Math.random().toString(36).substr(2, 9),
    title: generateNanJTitle(post.title, 'sad'),
    originalTitle: post.title,
    source: 'JVC 18-25',
    comments: post.replies,
    upvotes: post.views,
    url: post.url,
    thumbnail: getEmojiForTopic(post.title),
    lang: 'fr',
  }));
  
  // 繁体字（台湾）データ
  console.log('📡 Fetching Traditional Chinese sources...');
  const pttData = await fetchPTT();
  
  data['zh-TW'] = pttData.map(post => ({
    id: Math.random().toString(36).substr(2, 9),
    title: generateNanJTitle(post.title, 'sad'),
    originalTitle: post.title,
    source: 'PTT八卦板',
    comments: post.push_count,
    upvotes: post.push_count * 30,
    url: post.url,
    thumbnail: getEmojiForTopic(post.title),
    lang: 'zh-TW',
  }));
  
  // 簡体字（中国本土向け）データ - 台湾データを変換
  console.log('🔄 Converting to Simplified Chinese...');
  data['zh-CN'] = data['zh-TW'].map(post => ({
    ...post,
    id: Math.random().toString(36).substr(2, 9),
    title: convertToSimplified(post.title),
    originalTitle: convertToSimplified(post.originalTitle),
    source: convertToSimplified(post.source) + '（简体版）',
    lang: 'zh-CN',
    converted: true,
  }));
  
  return data;
}

// トピックから絵文字選択
function getEmojiForTopic(text) {
  const lower = text.toLowerCase();
  if (lower.includes('pc') || lower.includes('computer')) return '🖥️';
  if (lower.includes('japan') || lower.includes('日本')) return '🇯🇵';
  if (lower.includes('food') || lower.includes('comida')) return '🍔';
  if (lower.includes('car') || lower.includes('coche')) return '🚗';
  if (lower.includes('money') || lower.includes('薪')) return '💰';
  if (lower.includes('game')) return '🎮';
  return '📰';
}

// メイン実行
async function main() {
  try {
    const data = await aggregateData();
    
    // データをJSONファイルに保存
    const outputPath = path.join(__dirname, '../public/data/threads.json');
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, JSON.stringify(data, null, 2));
    
    console.log('\n✅ Data aggregation complete!');
    console.log(`📊 Total threads: ${Object.values(data).flat().length}`);
    console.log(`💾 Saved to: ${outputPath}`);
    console.log(`🕐 Last update: ${data.lastUpdate}`);
  } catch (error) {
    console.error('❌ Error:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { aggregateData, generateNanJTitle, convertToSimplified };
