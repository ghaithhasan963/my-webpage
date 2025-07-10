import sqlite3
import hashlib

DB_NAME = 'users.db'

# إنشاء القاعدة وجدول المستخدمين
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# إنشاء مستخدم جديد
def create_user(username, password):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# التحقق من بيانات المستخدم عند تسجيل الدخول
def authenticate(username, password):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, hashed_pw))
    account = c.fetchone()
    conn.close()
    return account

# تغيير كلمة المرور
def update_password(username, new_password):
    hashed_pw = hashlib.sha256(new_password.encode()).hexdigest()
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('UPDATE users SET password=? WHERE username=?', (hashed_pw, username))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()