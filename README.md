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
```sh
python -m venv venv
source venv\Scripts\activate
pip install -r requirements.txt
```

### 4. データベースの設定
PostgreSQL に接続し、データベースとユーザーを作成します。
```sql
CREATE DATABASE your_db_name;
CREATE USER your_db_username WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_username;
```
### 5. 環境変数の設定
.env ファイルを作成し、以下のようにデータベース情報を設定します。
```dotenv
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_NAME=your_db_name
SECRET_KEY=your_secret_key
```
### 6. データベースの初期化
```sh
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### 7. アプリを実行する
```sh
python app.py
```
実行すると二つのURLが表示されます
```flask run
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://XXX.XXX.XX.XXX:5000　(同じネットワーク内の他のデバイスからもアクセス可能になります。)
Press CTRL+C to quit
```
が表示される
### 8. ブラウザでアクセス
アプリが起動したら、ブラウザで以下の URL にアクセスできます。
```url
http://127.0.0.1:5000/
```
同じネットワーク内の他のデバイスからアクセスしたい時はブラウザで以下のURLにアクセスしてください。
```sh
http://XXX.XXX.XX.XXX:5000
```
## フォルダ構成
```bash
/venv_webapp
│── app.py  # メインアプリケーション
│── templates/  # HTMLテンプレート
│── static/  # CSS
│── .env  # 環境変数ファイル
│── requirements.txt  # 依存パッケージ
│── README.md  # このファイル
```
## .envファイルの内容
```dotenv
DB_USERNAME=postgres
DB_PASSWORD=kansei
DB_HOST=localhost
DB_NAME=dbname
```
