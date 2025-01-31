import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# PostgreSQLデータベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key')  # セッション用の秘密鍵

# SQLAlchemyオブジェクトの初期化
db = SQLAlchemy(app)

# ユーザーモデル
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

# タスクモデル
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_date = db.Column(db.DateTime, nullable=True)  # 完了日を追加
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

# ログイン必須デコレータ
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('ログインが必要です')
            return redirect(url_for('register'))
        return f(*args, **kwargs)
    return decorated_function

# ルート：ユーザー登録画面
@app.route('/', methods=['GET'])
def register():
    return render_template('register.html')

# ルート：ユーザー登録処理
@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    
    # 文字数制限のチェック
    if len(username) > 20:
        flash('ユーザー名は20文字以下にしてください', 'error')
        return redirect(url_for('register'))
    
    if len(password) < 6 or len(password) > 20:
        flash('パスワードは6文字以上20文字以下にしてください', 'error')
        return redirect(url_for('register'))
    
    # ユーザー名の重複チェック
    if User.query.filter_by(username=username).first():
        flash('このユーザー名は既に使用されています', 'error')
        return redirect(url_for('register'))
    
    # ユーザーを作成
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    
    # 成功メッセージを表示して登録画面に戻る
    flash('アカウントの作成に成功しました。ログインしてください。', 'success')
    return redirect(url_for('register'))

# ルート：ログイン処理
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return redirect(url_for('tasks', user_id=user.id))
    
    flash('ユーザー名またはパスワードが正しくありません')
    return redirect(url_for('register'))

# ルート：ログアウト
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('register'))

# ルート：タスク一覧画面
@app.route('/tasks/<int:user_id>')
@login_required
def tasks(user_id):
    if session['user_id'] != user_id:
        flash('アクセス権限がありません')
        return redirect(url_for('register'))
    
    user = User.query.get_or_404(user_id)
    tasks = Task.query.filter_by(user_id=user_id, completed=False).all()
    completed_tasks = Task.query.filter_by(user_id=user_id, completed=True).all()
    now = datetime.now()
    return render_template('tasks.html', user=user, tasks=tasks, completed_tasks=completed_tasks, now=now)

# ルート：タスク追加
@app.route('/tasks/<int:user_id>/add', methods=['POST'])
@login_required
def add_task(user_id):
    if session['user_id'] != user_id:
        flash('アクセス権限がありません')
        return redirect(url_for('register'))
    
    title = request.form['title']
    due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
    task = Task(title=title, due_date=due_date, user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('tasks', user_id=user_id))

# ルート：タスク完了
@app.route('/tasks/<int:user_id>/complete/<int:task_id>', methods=['POST'])
@login_required
def complete_task(user_id, task_id):
    if session['user_id'] != user_id:
        flash('アクセス権限がありません')
        return redirect(url_for('register'))
    
    task = Task.query.get_or_404(task_id)
    # タスクの所有者確認
    if task.user_id != user_id:
        flash('アクセス権限がありません')
        return redirect(url_for('register'))
    
    task.completed = True
    task.completed_date = datetime.now()  # 完了日を設定
    db.session.commit()
    return redirect(url_for('tasks', user_id=user_id))

# ルート：タスク削除
@app.route('/tasks/<int:user_id>/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(user_id, task_id):
    if session['user_id'] != user_id:
        flash('アクセス権限がありません')
        return redirect(url_for('register'))
    
    task = Task.query.get_or_404(task_id)
    # タスクの所有者確認
    if task.user_id != user_id:
        flash('アクセス権限がありません')
        return redirect(url_for('register'))
    
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks', user_id=user_id))

# アプリケーションのエントリーポイント
if __name__ == '__main__':
    with app.app_context():
        # テーブルが存在しない場合のみ作成
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)