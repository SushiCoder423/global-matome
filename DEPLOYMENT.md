# 🚀 完全無料デプロイ手順

## ステップ1: GitHubリポジトリ作成

1. https://github.com/new にアクセス
2. リポジトリ名: `global-matome`
3. Public を選択
4. "Create repository" をクリック

## ステップ2: コードをアップロード

```bash
# ローカルでGit初期化
cd /path/to/global-matome
git init
git add .
git commit -m "Initial commit: Global Matome site"

# GitHubにプッシュ
git remote add origin https://github.com/YOUR_USERNAME/global-matome.git
git branch -M main
git push -u origin main
```

## ステップ3: API キー取得

### Reddit API（必須）

1. https://www.reddit.com/prefs/apps にアクセス
2. 下部の "are you a developer? create an app..." をクリック
3. 以下を入力:
   - name: Global Matome Bot
   - App type: **script** を選択
   - description: Data fetcher for matome site
   - about url: (空欄でOK)
   - redirect uri: http://localhost:8000
4. "create app" をクリック
5. 表示された情報をメモ:
   - **Client ID**: アプリ名の下の英数字
   - **Secret**: "secret" の右の値

### Twitter API（オプション）

1. https://developer.twitter.com/en/portal/dashboard
2. "Create Project" → "Create App"
3. Bearer Token をコピー

## ステップ4: GitHub Secrets設定

1. GitHubリポジトリページで Settings → Secrets and variables → Actions
2. "New repository secret" をクリック
3. 以下を1つずつ追加:

```
Name: REDDIT_CLIENT_ID
Value: (Reddit APIのClient ID)

Name: REDDIT_CLIENT_SECRET
Value: (Reddit APIのSecret)

Name: TWITTER_BEARER_TOKEN
Value: (Twitter APIのBearer Token) ※オプション
```

## ステップ5: GitHub Pages有効化

1. Settings → Pages
2. Source: **GitHub Actions** を選択
3. 保存

## ステップ6: 初回デプロイ

### 方法A: 自動デプロイ（推奨）

GitHub Actionsが自動で実行されます:
1. Actions タブをクリック
2. "Auto Fetch Global Threads" ワークフローを確認
3. 緑のチェックマークが付けば成功

### 方法B: 手動デプロイ

```bash
# ローカルで実行
npm install
npm run build
npm run deploy
```

## ステップ7: サイト確認

デプロイ完了後、以下のURLでアクセス可能:

```
https://YOUR_USERNAME.github.io/global-matome/
```

## ステップ8: 独自ドメイン設定（オプション）

1. ドメインを取得（例: Namecheap, Google Domains）
2. DNS設定で以下を追加:
   ```
   A    185.199.108.153
   A    185.199.109.153
   A    185.199.110.153
   A    185.199.111.153
   CNAME www YOUR_USERNAME.github.io
   ```
3. GitHub Settings → Pages → Custom domain に入力
4. `.github/workflows/auto-fetch.yml` の `cname:` を更新

## ステップ9: 収益化設定

### Google AdSense

1. https://www.google.com/adsense/ で審査申請
2. 審査通過後、広告コードを取得
3. `public/index.html` に貼り付け:
   ```html
   <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXX"
        crossorigin="anonymous"></script>
   ```

### アフィリエイト登録

#### 英語圏
- Amazon Associates: https://affiliate-program.amazon.com/
- eBay Partner Network: https://partnernetwork.ebay.com/

#### スペイン語圏
- MercadoLibre: https://afiliados.mercadolibre.com/

#### ポルトガル語圏
- Mercado Livre: https://afiliados.mercadolivre.com.br/

#### 中国語圏
- 淘宝联盟: https://pub.alimama.com/

### アフィリエイトリンク設定

`src/App.jsx` の `affiliateLinks` を更新:

```javascript
const affiliateLinks = {
  en: {
    amazon: 'https://amazon.com/?tag=YOUR_AMAZON_TAG',
  },
  // ...
};
```

## 運用スケジュール

### 自動化（GitHub Actions）
- **毎日 UTC 0:00**: 新規データ取得 + デプロイ
- **手動トリガー**: いつでも実行可能

### 手作業
- **週1回**: アフィリエイトリンク最適化
- **月1回**: パフォーマンス分析、人気記事チェック

## トラブルシューティング

### デプロイが失敗する

```bash
# ログ確認
GitHub → Actions → 失敗したワークフロー → 詳細ログ

# よくある原因:
# 1. Secretsが未設定 → ステップ4を再確認
# 2. package.json の homepage が間違い → 修正してpush
# 3. APIキーが無効 → 再発行
```

### サイトが表示されない

1. GitHub Pages設定を確認（Settings → Pages）
2. URLが正しいか確認
3. 数分待ってから再アクセス（初回は時間がかかる）

### データが更新されない

```bash
# ローカルでテスト
node scripts/fetch-data.js

# エラーが出たら:
# - APIキーを確認
# - ネットワーク接続を確認
```

## コスト

- **GitHub Pages**: $0（無料・無制限）
- **GitHub Actions**: 月2,000分まで無料（このプロジェクトは1日5分程度 = 月150分）
- **API使用**: 全て無料枠内
- **ドメイン**: 年$10-20（オプション）

**合計: $0/月**（独自ドメイン無しの場合）

## 次のステップ

1. ✅ 基本デプロイ完了
2. 📊 Google Analytics設定（トラフィック分析）
3. 💰 AdSense審査申請（10記事以上推奨）
4. 🔗 アフィリエイト登録
5. 📱 SNS アカウント作成（拡散用）
6. 🎨 デザインカスタマイズ

---

**おめでとうございます！🎉**
あなたの世界まとめサイトが完成しました。
