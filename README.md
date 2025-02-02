# タスク管理アプリ

このプロジェクトは、Flask と PostgreSQL を使用したシンプルなタスク管理アプリです。ユーザーはアカウントを作成し、タスクの追加・完了・削除ができます。

## 特徴
- ユーザー登録・ログイン機能
- タスクの追加・完了・削除機能
- PostgreSQL を使用したデータ管理
- セッションを利用したユーザー認証

## 環境構築と実行方法

### 1. 必要なツールのインストール
このアプリを実行するには、以下のツールが必要です。
- Python 3.x
- PostgreSQL
- pip（Python パッケージ管理ツール）

### 2. リポジトリのクローン
```sh
git clone https://github.com/your-repository/task-manager.git
cd task-manager
```

### 3. 仮想環境の作成と依存関係のインストール
sh
python -m venv venv
source venv/bin/activate  # Windows の場合: venv\Scripts\activate
pip install -r requirements.txt

### 4. データベースの設定
PostgreSQL に接続し、データベースとユーザーを作成します。
sql
CREATE DATABASE your_db_name;
CREATE USER your_db_username WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_username;

### 5. 環境変数の設定
.env ファイルを作成し、以下のようにデータベース情報を設定します。
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_NAME=your_db_name
SECRET_KEY=your_secret_key

### 6. データベースの初期化
sh
flask db init
flask db migrate -m "Initial migration."
flask db upgrade

### 7. アプリの起動
sh
python app.py

### 8. ブラウザでアクセス
アプリが起動したら、ブラウザで以下の URL にアクセスします。
http://127.0.0.1:5000/

## フォルダ構成
/task-manager
│── app.py  # メインアプリケーション
│── models.py  # データベースモデル
│── templates/  # HTMLテンプレート
│── static/  # CSS・JavaScript・画像
│── .env  # 環境変数ファイル
│── requirements.txt  # 依存パッケージ
│── README.md  # このファイル

## ライセンス
このプロジェクトは MIT ライセンスの下で提供されています。
