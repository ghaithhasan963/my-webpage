from flask import Flask, render_template, request, redirect, session
from db import init_db, create_user, authenticate, update_password

app = Flask(__name__)
app.secret_key = 'digital_shadow_secret'
app.permanent_session_lifetime = 3600  # مدة الجلسة ساعة واحدة

init_db()  # إنشاء الجدول عند التشغيل

# تسجيل الدخول
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        account = authenticate(username, password)
        if account:
            session['user'] = username
            session.permanent = True
            return redirect('/dashboard')
        else:
            return render_template('index.html', error="❌ اسم المستخدم أو كلمة المرور غير صحيحة")
    return render_template('index.html')

# إنشاء حساب جديد
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success = create_user(username, password)
        if success:
            return redirect('/')
        else:
            return render_template('register.html', error="⚠️ اسم المستخدم موجود مسبقاً")
    return render_template('register.html')

# لوحة التحكم
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect('/')

# تغيير كلمة المرور
@app.route('/change', methods=['GET', 'POST'])
def change_password():
    if 'user' not in session:
        return redirect('/')
    if request.method == 'POST':
        old_pw = request.form['old_password']
        new_pw = request.form['new_password']
        user = session['user']
        if authenticate(user, old_pw):
            success = update_password(user, new_pw)
            if success:
                return render_template('change.html', success="✅ تم تغيير كلمة المرور بنجاح")
            else:
                return render_template('change.html', error="❌ فشل التحديث")
        else:
            return render_template('change.html', error="❌ كلمة المرور القديمة غير صحيحة")
    return render_template('change.html')

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)