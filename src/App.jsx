import React, { useState, useEffect } from 'react';
import './App.css';

// なんJ型タイトルテンプレート
const titleTemplates = [
  '【悲報】{subject}、{action}した結果ｗｗｗｗｗ',
  '【画像】{subject}が{action}してて草',
  '【急募】{subject}に自信ニキ',
  '【朗報】{subject}、{action}で無事死亡',
  '{subject}で打線組んだｗｗｗｗｗ',
  'ワイ、{action}して咽び泣く',
];

// 言語別掲示板ソース
const sources = {
  en: [
    { name: 'Reddit - r/all', url: 'https://reddit.com/r/all', type: 'reddit' },
    { name: 'Twitter Trending', url: 'https://twitter.com', type: 'twitter' },
  ],
  es: [
    { name: 'Forocoches', url: 'https://forocoches.com', type: 'forum' },
    { name: 'Menéame', url: 'https://meneame.net', type: 'reddit-like' },
  ],
  pt: [
    { name: 'Hardmob', url: 'https://hardmob.com.br', type: 'forum' },
    { name: 'Reddit BR', url: 'https://reddit.com/r/brasil', type: 'reddit' },
  ],
  fr: [
    { name: 'JeuxVideo.com Forum', url: 'https://jeuxvideo.com', type: 'forum' },
    { name: 'Reddit France', url: 'https://reddit.com/r/france', type: 'reddit' },
    { name: '18-25 (JVC)', url: 'https://jeuxvideo.com/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm', type: 'forum' },
  ],
  'zh-TW': [
    { name: 'PTT', url: 'https://ptt.cc', type: 'bbs' },
    { name: 'Dcard', url: 'https://dcard.tw', type: 'social' },
  ],
  'zh-CN': [
    { name: 'PTT (簡体版)', url: 'https://ptt.cc', type: 'bbs', converted: true },
    { name: 'Dcard (簡体版)', url: 'https://dcard.tw', type: 'social', converted: true },
  ],
};

// デモデータ（後でAPI実装）
const demoThreads = {
  en: [
    {
      id: 1,
      title: '【悲報】Redditor, bought $2000 PC and it doesn\'t boot wwwww',
      source: 'r/pcmasterrace',
      comments: 247,
      upvotes: 12500,
      thumbnail: '🖥️',
    },
    {
      id: 2,
      title: '【画像】American tried Japanese vending machine for the first time, reaction is 草',
      source: 'r/Japan',
      comments: 156,
      upvotes: 8900,
      thumbnail: '🇯🇵',
    },
    {
      id: 3,
      title: '【急募】How to tell my boss I quit - strategies needed wwwww',
      source: 'r/antiwork',
      comments: 892,
      upvotes: 34200,
      thumbnail: '💼',
    },
  ],
  es: [
    {
      id: 4,
      title: '【悲報】Español compró coche usado, encontró 10kg de jamón en el maletero wwwww',
      source: 'Forocoches',
      comments: 423,
      upvotes: 15600,
      thumbnail: '🚗',
    },
    {
      id: 5,
      title: '【画像】Argentino cocinó asado perfecto, los vecinos lloraron de envidia 草',
      source: 'Taringa',
      comments: 234,
      upvotes: 9800,
      thumbnail: '🥩',
    },
  ],
  pt: [
    {
      id: 6,
      title: '【悲報】Brasileiro instalou PC Gamer, conta de luz chegou R$800 wwwww',
      source: 'Hardmob',
      comments: 567,
      upvotes: 18900,
      thumbnail: '⚡',
    },
    {
      id: 7,
      title: '【朗報】Português descobriu praia secreta no Algarve, turistas em choque 草',
      source: 'Reddit PT',
      comments: 189,
      upvotes: 7200,
      thumbnail: '🏖️',
    },
  ],
  fr: [
    {
      id: 12,
      title: '【悲報】Français a acheté baguette, elle était molle wwwww',
      source: 'JVC 18-25',
      comments: 892,
      upvotes: 34500,
      thumbnail: '🥖',
    },
    {
      id: 13,
      title: '【画像】Congolais montre sa connexion internet, 2MB/s et il paye 100€/mois 草',
      source: 'Reddit France',
      comments: 445,
      upvotes: 18900,
      thumbnail: '📡',
    },
    {
      id: 14,
      title: '【急募】Québécois cherche comment survivre à -40°C, conseils recherchés wwwww',
      source: 'JeuxVideo.com',
      comments: 678,
      upvotes: 25600,
      thumbnail: '❄️',
    },
  ],
  'zh-TW': [
    {
      id: 8,
      title: '【悲報】台灣鄉民、買了雞排結果是素的wwwww',
      source: 'PTT八卦板',
      comments: 345,
      upvotes: 11200,
      thumbnail: '🍗',
    },
    {
      id: 9,
      title: '【畫像】Dcard網友曬台積電offer，薪水讓全場跪了草',
      source: 'Dcard',
      comments: 678,
      upvotes: 23400,
      thumbnail: '💰',
    },
  ],
  'zh-CN': [
    {
      id: 10,
      title: '【悲报】台湾乡民、买了鸡排结果是素的wwwww',
      source: 'PTT八卦板（简体版）',
      comments: 345,
      upvotes: 11200,
      thumbnail: '🍗',
      converted: true,
    },
    {
      id: 11,
      title: '【画像】Dcard网友晒台积电offer，薪水让全场跪了草',
      source: 'Dcard（简体版）',
      comments: 678,
      upvotes: 23400,
      thumbnail: '💰',
      converted: true,
    },
  ],
};

// アフィリエイトリンク設定
const affiliateLinks = {
  en: {
    amazon: 'https://amazon.com/?tag=yourid',
    ebay: 'https://ebay.com/affiliate',
  },
  es: {
    mercadolibre: 'https://mercadolibre.com/affiliate',
    aliexpress: 'https://aliexpress.com/?aff=yourid',
  },
  pt: {
    mercadolivre: 'https://mercadolivre.com.br/affiliate',
    amazon: 'https://amazon.com.br/?tag=yourid',
  },
  fr: {
    amazon: 'https://amazon.fr/?tag=yourid',
    cdiscount: 'https://cdiscount.com/affiliate',
    fnac: 'https://fnac.com/affiliate',
  },
  'zh-TW': {
    pchome: 'https://pchome.com.tw/affiliate',
    shopee: 'https://shopee.tw/?aff=yourid',
  },
  'zh-CN': {
    taobao: 'https://taobao.com/affiliate',
    jd: 'https://jd.com/?aff=yourid',
  },
};

const languageNames = {
  en: '🇺🇸 English',
  es: '🇪🇸 Español',
  pt: '🇧🇷 Português',
  fr: '🇫🇷 Français',
  'zh-TW': '🇹🇼 繁體中文',
  'zh-CN': '🇨🇳 简体中文',
};

function App() {
  const [currentLang, setCurrentLang] = useState('en');
  const [threads, setThreads] = useState([]);

  useEffect(() => {
    // デモデータ読み込み（後でAPI実装）
    setThreads(demoThreads[currentLang] || []);
  }, [currentLang]);

  return (
    <div className="App">
      <header className="header">
        <h1>🌍 Global Matome - 世界まとめ速報</h1>
        <p className="tagline">世界中の掲示板からヤバい投稿を毎日お届けｗｗｗｗｗ</p>
      </header>

      {/* 言語タブ */}
      <nav className="language-tabs">
        {Object.entries(languageNames).map(([lang, name]) => (
          <button
            key={lang}
            className={`tab ${currentLang === lang ? 'active' : ''}`}
            onClick={() => setCurrentLang(lang)}
          >
            {name}
          </button>
        ))}
      </nav>

      {/* ソース情報 */}
      <div className="sources-info">
        <p>
          📡 取得元: {sources[currentLang]?.map(s => s.name).join(', ')}
          {currentLang === 'zh-CN' && ' (⚠️ 繁体字から自動変換)'}
        </p>
      </div>

      {/* スレッド一覧 */}
      <main className="threads-container">
        {threads.map((thread) => (
          <article key={thread.id} className="thread-card">
            <div className="thread-header">
              <span className="thumbnail">{thread.thumbnail}</span>
              <div className="thread-info">
                <h2 className="thread-title">{thread.title}</h2>
                <div className="thread-meta">
                  <span className="source">📍 {thread.source}</span>
                  <span className="stats">
                    👍 {thread.upvotes.toLocaleString()} | 
                    💬 {thread.comments}
                  </span>
                  {thread.converted && (
                    <span className="badge">🔄 簡体字変換済み</span>
                  )}
                </div>
              </div>
            </div>
            <button className="read-more">続きを読むｗｗｗ →</button>
          </article>
        ))}
      </main>

      {/* アフィリエイトバナー */}
      <aside className="affiliate-sidebar">
        <h3>🛒 おすすめショップ</h3>
        {affiliateLinks[currentLang] && (
          <div className="affiliate-links">
            {Object.entries(affiliateLinks[currentLang]).map(([name, url]) => (
              <a key={name} href={url} className="affiliate-button" target="_blank" rel="noopener">
                {name.toUpperCase()}
              </a>
            ))}
          </div>
        )}
        <div className="adsense-placeholder">
          {/* Google AdSense 広告枠 */}
          <p>[ AdSense広告エリア ]</p>
        </div>
      </aside>

      <footer className="footer">
        <p>© 2024 Global Matome | 世界中の掲示板を自動収集中ｗｗｗ</p>
        <p className="disclaimer">
          ⚠️ 各掲示板の投稿を引用・翻訳したものです。著作権は元の投稿者に帰属します。
        </p>
      </footer>
    </div>
  );
}

export default App;
