# ペットサロン予約システム バックエンド

## セットアップ手順

1. Python仮想環境の作成と有効化
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

3. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集して必要な設定を行う
```

4. アプリケーションの起動
```bash
python app.py
```

## APIエンドポイント

### お問い合わせ
- POST `/api/contact`
  - リクエストボディ: `name`, `email`, `phone`, `message`

### 予約
- POST `/api/reservation`
  - リクエストボディ: `pet_type`, `service_type`, `desired_date`, `desired_time`, `owner_name`, `owner_email`, `owner_phone`

## テストの実行
```bash
pytest
```