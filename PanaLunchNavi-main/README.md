# 🍱 Panasonic Lunch Navi（パナラン）

社内のランチ情報を共有するWebアプリケーション

## 📋 プロジェクト概要

Panasonic社員向けのランチ情報共有アプリです。外部のランチ店情報を社内で共有し、社員同士の情報交換を促進します。

## 🚀 セットアップ

### 必要な環境

- Python 3.8以上
- Streamlit

### インストール

1. リポジトリをクローン
```bash
git clone https://github.com/YunSeunghwan/PanaLunchNavi.git
cd PanaLunchNavi
```

2. 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

3. アプリを起動
```bash
streamlit run app.py
```

4. ブラウザで `http://localhost:8501` を開く

## 📁 プロジェクト構造

```
20251109_PanaLaunchNavi/
├── app.py                 # メインアプリケーション
├── stores.json            # 店舗データ
├── requirements.txt       # Pythonパッケージ一覧
├── plan.md               # 開発計画・進捗管理
├── README.md             # プロジェクト説明
├── .gitignore            # Git除外設定
├── .streamlit/           # Streamlit設定
│   └── config.toml       # Streamlit設定ファイル
└── docs/                 # ドキュメント
    ├── project_v2.md     # 企画書
    └── project_specifications.md  # 仕様書
```

## 🎯 機能

- 店舗リスト表示
- 店舗詳細表示
- 新規店舗投稿
- 検索・フィルター機能
- 評価・コメント機能

## 📚 ドキュメント

詳細なドキュメントは `docs/` フォルダーを参照してください。

- 企画書: `docs/project_v2.md`
- 仕様書: `docs/project_specifications.md`
- 開発計画: `plan.md`

## 👥 開発チーム

ゆんチーム（開発者2名）

## 🚀 Streamlit Cloudへのデプロイ

### デプロイ手順

1. **Streamlit Cloudにアクセス**
   - https://streamlit.io/cloud にアクセス
   - GitHubアカウントでサインイン（まだアカウントがない場合は作成）

2. **新しいアプリを作成**
   - ダッシュボードから "New app" をクリック
   - 以下の情報を入力：
     - **Repository**: `YunSeunghwan/PanaLunchNavi`
     - **Branch**: `main`
     - **Main file**: `app.py`
     - **App URL**: 自動生成されます（例: `pana-lunch-navi.streamlit.app`）

3. **デプロイ開始**
   - "Deploy" をクリック
   - デプロイが完了するまで数分待ちます
   - デプロイが完了すると、自動的にアプリのURLが表示されます

4. **動作確認**
   - デプロイされたアプリのURLにアクセス
   - 各機能が正常に動作することを確認

### デプロイ後の注意事項

- **データの永続化**: Streamlit Cloudでは、ファイルシステムへの書き込みは一時的なものです。永続的なデータ保存が必要な場合は、データベース（Firestore等）の使用を検討してください。
- **環境変数**: 必要に応じて、Streamlit Cloudの設定で環境変数を追加できます。

### トラブルシューティング

- デプロイが失敗する場合：
  - `requirements.txt`が正しく設定されているか確認
  - ログを確認してエラー内容を確認
  - 必要に応じて `.streamlit/config.toml` の設定を確認

## 📝 ライセンス

社内利用のみ

---

**Panasonic Lunch Navi** - 社員同士の情報が温かく循環するランチ紹介アプリ

