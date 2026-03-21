# 🌍 Global Matome - 世界まとめ速報

世界中の掲示板（Reddit, Twitter, PTT, Forocoches, Hardmob等）から面白投稿を自動収集してなんJ風にまとめるサイト

## 🎯 特徴

- **5言語対応**: 英語🇺🇸 / スペイン語🇪🇸 / ポルトガル語🇧🇷 / 繁体中文🇹🇼 / 简体中文🇨🇳
- **完全無料**: GitHub Pages（サーバーコスト0円）
- **自動更新**: 1日1回自動でデータ取得
- **繁体字→簡体字変換**: 台湾掲示板を中国本土でも閲覧可能に
- **なんJ風タイトル**: 【悲報】【朗報】【急募】形式
- **多通貨アフィリエイト**: 各国のECサイト対応

## 🚀 クイックスタート

### 1. リポジトリをフォーク

```bash
# このリポジトリをGitHubでフォーク
# または
git clone https://github.com/yourusername/global-matome.git
cd global-matome
```

### 2. 必要なAPIキーを取得

#### Reddit API
1. https://www.reddit.com/prefs/apps にアクセス
2. "Create App" をクリック
3. "script" を選択
4. Client IDとSecretをコピー

#### Twitter API v2（オプション）
1. https://developer.twitter.com/en/portal/dashboard
2. Bearer Tokenを取得

### 3. GitHub Secretsに設定

GitHubリポジトリの Settings → Secrets and variables → Actions で以下を設定:

```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

### 4. GitHub Pagesを有効化

1. Settings → Pages
2. Source: "GitHub Actions" を選択
3. 保存

### 5. デプロイ

```bash
npm install
npm run build
npm run deploy
```

または、mainブランチにpushすれば自動デプロイされます。

## 📊 データソース

### 英語圏
- Reddit (r/all, r/todayilearned, r/LifeProTips など)
- Twitter trending topics

### スペイン語圏
- Forocoches (スペイン最大掲示板)
- Menéame (スペイン版Reddit)
- Taringa! (中南米)

### ポルトガル語圏
- Hardmob (ブラジル最大PC系掲示板)
- Reddit Brasil

### 中国語圏
- PTT (台湾最大掲示板)
- Dcard (台湾SNS)
- → 自動で簡体字に変換

## 💰 収益化設定

### Google AdSense

`public/index.html` に広告コードを追加:

```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXX"
     crossorigin="anonymous"></script>
```

### アフィリエイトリンク

`src/App.jsx` の `affiliateLinks` オブジェクトを編集:

```javascript
const affiliateLinks = {
  en: {
    amazon: 'https://amazon.com/?tag=YOUR_TAG',
    ebay: 'https://ebay.com/affiliate?YOUR_ID',
  },
  es: {
    mercadolibre: 'https://mercadolibre.com/affiliate?YOUR_ID',
  },
  // ...
};
```

### 対応アフィリエイトプログラム

| 言語 | プラットフォーム | 報酬率 |
|------|----------------|--------|
| 英語 | Amazon Associates | 1-10% |
| 英語 | eBay Partner Network | 50-70%/購入 |
| スペイン | MercadoLibre | 2-8% |
| ポルトガル | Mercado Livre | 3-10% |
| 中国語 | 淘宝联盟 | 3-20% |

## 🔄 自動更新の仕組み

GitHub Actionsが毎日UTC 0:00（日本時間9:00）に実行:

1. 各掲示板APIからデータ取得
2. なんJ風タイトルに変換
3. 繁体字→簡体字変換
4. JSONファイル生成
5. React ビルド
6. GitHub Pagesにデプロイ

手動実行も可能:
- GitHubリポジトリ → Actions → "Auto Fetch Global Threads" → "Run workflow"

## 🎨 カスタマイズ

### タイトルテンプレート変更

`scripts/fetch-data.js` の `titleTemplates` を編集:

```javascript
const titleTemplates = {
  sad: ['【悲報】', '【速報】'],
  happy: ['【朗報】'],
  // 追加したいパターン
};
```

### 取得する掲示板変更

`scripts/fetch-data.js` の `aggregateData()` 関数を編集:

```javascript
const redditData = await fetchReddit('your_favorite_subreddit', 25);
```

### デザイン変更

`src/App.css` を編集してスタイルをカスタマイズ

## 📈 収益予測

### 月間50万PV達成時の収益例

| 収益源 | 英語 | スペイン語 | ポルトガル語 |
|--------|------|-----------|-------------|
| AdSense | $2,000 | $500 | $600 |
| アフィリ | $800 | $300 | $400 |
| **合計** | **$2,800** | **$800** | **$1,000** |

### 成長戦略

1. **初月**: 英語版のみ、Reddit特化（目標:10万PV）
2. **2-3ヶ月**: スペイン語・ポルトガル語追加（目標:30万PV）
3. **4-6ヶ月**: 中国語版追加、SEO最適化（目標:50万PV）
4. **7-12ヶ月**: SNS拡散、コミュニティ形成（目標:100万PV）

## ⚠️ 注意事項

### 著作権
- 各掲示板の投稿は引用の範囲内で使用
- 元の投稿URLを必ず記載
- 過度な転載は避ける

### API利用制限
- Reddit API: 60リクエスト/分
- Twitter API v2: 500,000リクエスト/月（Free tier）
- 制限超過時は自動リトライ

### 禁止事項
- スパム行為
- 虚偽情報の拡散
- 著作権侵害
- ヘイトスピーチ

## 🛠️ トラブルシューティング

### ビルドエラー

```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

### GitHub Actionsが失敗する

- Secretsが正しく設定されているか確認
- APIキーの有効期限をチェック
- リポジトリのActionsが有効になっているか確認

### データが更新されない

- `scripts/fetch-data.js` を手動実行してエラーチェック:
  ```bash
  node scripts/fetch-data.js
  ```

## 📞 サポート

- Issues: https://github.com/yourusername/global-matome/issues
- Discussions: https://github.com/yourusername/global-matome/discussions

## 📜 ライセンス

MIT License

---

**作成者**: あなたの名前
**デモサイト**: https://yourusername.github.io/global-matome
**最終更新**: 2024年
