from datetime import timedelta
from flask import Flask, redirect, render_template, request, url_for, session
from hashlib import md5
import pyodbc

app = Flask(__name__)
app.config["SECRET_KEY"] = 'skapp'
# app.permanent_session_lifetime = timedelta(minutes=2)

def connection():
    s = 'DESKTOP-O4OB08D\MAYCHU' 
    d = 'db_app' 
    u = 'sa'
    p = '123456'
    db_app = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    
    conn = pyodbc.connect(db_app)
    return conn

@app.route('/')
def home_page():
    cate = []

    conn1 = connection()
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT * FROM dbo.category")
    for row in cursor1.fetchall():
        cate.append({"id_cate": row[0], "name_cate": row[1], "image_cate": row[2]})

    if "user" in session:
        name_us = session['user']
        r = session['roll']
        return render_template('index.html', usname=name_us, roll=r, category=cate)
    else:
        return render_template('index.html', category=cate)

@app.route('/<id>')
def category_page(id):
    name = ''
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name_cate FROM dbo.category WHERE id_cate = '{id_cate}' ".format(id_cate = id))
    for row in cursor.fetchall():
        name = row[0]
        break
    return render_template('category.html', category=name)


@app.route('/login')
def login_page():
    if "user" in session:
        return redirect(url_for('home_page'))

    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def check_login():
    user_name = ''
    user_id = ''
    name = ''
    roll = 1
    conn = connection()

    us_login = request.form['Username']
    pw_login = request.form['Password']
    pw_hash = md5(pw_login.encode()).hexdigest()
    cursor1 = conn.cursor()
    cursor1.execute("SELECT * FROM dbo.user_login where us = '{username}' AND pw = '{password}'".format(username = us_login, password = pw_hash))
    for row in cursor1.fetchall():
        user_name = row[0]
        user_id = row[2]
        roll = row[3]
        break

    cursor2 = conn.cursor()
    cursor2.execute("SELECT name_user FROM dbo.user_app where id_user = '{id}'".format(id = user_id))
    for row in cursor2.fetchall():
        name = row[0]
        break
    conn.close()

    if user_name:
        session['user'] = name
        session['roll'] = roll
        return redirect(url_for('home_page'))
    else:
        session['login-err'] = 'Tài khoản hoặc mật khẩu không đúng'
        return render_template('login.html', err=session['login-err'])
    
@app.route('/register')
def register_page():
    return render_template("register.html")


@app.route('/register', methods = ['POST', 'GET'])
def register():
    lis_us = []

    conn = connection()
    
    cursor1 = conn.cursor()
    query1 = "SELECT us FROM dbo.user_login"
    cursor1.execute(query1)
    for row in cursor1.fetchall():
        lis_us.append(row[0])

    fullname = request.form['Name']
    phone = request.form['Phone']
    username = request.form['Username']
    password = request.form['Password']

    if len(phone) != 10:
        session['register-err'] = 'SĐT chưa đúng'
        conn.close()
        return render_template('register.html', err=session['register-err'], fullname=fullname, phone=phone, username=username)
    elif username in lis_us:
        session['register-err'] = 'tên tài khoản đã tồn tại'
        conn.close()
        return render_template('register.html', err=session['register-err'], fullname=fullname, phone=phone, username=username)
    elif len(password) < 6:
        session['register-err'] = 'Mật khẩu phải dài hơn 6 kí tự'
        conn.close()
        return render_template('register.html', err=session['register-err'], fullname=fullname, phone=phone, username=username)
    else:
        try:
            id = ''

            pw_hash = md5(password.encode()).hexdigest()
            
            cursor2 = conn.cursor()
            cursor2.execute("INSERT INTO dbo.user_app (name_user, phone_user) VALUES (N'{name_user}', '{phone_user}')".format(name_user=fullname, phone_user=phone))
            conn.commit()

            cursor3 = conn.cursor()
            query2 = "SELECT id_user FROM dbo.user_app WHERE name_user = N'{name_user}' AND phone_user = '{phone_user}'".format(name_user=fullname, phone_user=phone)
            cursor3.execute(query2)
            for row in cursor3.fetchall():
                id = row[0]
                break

            cursor4 = conn.cursor()
            cursor4.execute("INSERT INTO dbo.user_login (us, pw, id_user, roll) VALUES ('{us}', '{pw}', '{id_user}', {roll})".format(us=username, pw=pw_hash, id_user=id, roll=2))
            conn.commit()

            conn.close()

            return 'Đăng ký tài khoản ' + fullname + ' Thành công <br> <a href="/">Trang chủ</a> <br> <a href="/login">Đăng nhập</a>'
        except Exception as e:
            return(str(e))

@app.route('/logout')
def logout_page():
    session.pop("user", None)
    return render_template('logout.html')

@app.route('/add-admin')
def add_admin_page():
    if 'roll' in session:
        if session['roll'] == 0:
            return render_template('admin.html')
        else:
            return '<h1> Error </h1>'
    return redirect(url_for('home_page'))

@app.route('/add-admin', methods = ['POST', 'GET'])
def add_admin():
    lis_us = []

    conn = connection()
    
    cursor1 = conn.cursor()
    query1 = "SELECT us FROM dbo.user_login"
    cursor1.execute(query1)
    for row in cursor1.fetchall():
        lis_us.append(row[0])

    fullname = request.form['Name']
    phone = request.form['Phone']
    username = request.form['Username']
    password = request.form['Password']

    if len(phone) != 10:
        session['register-admin-err'] = 'SĐT chưa đúng'
        conn.close()
        return render_template('register.html', err=session['register-admin-err'])
    elif username in lis_us:
        session['register-admin-err'] = 'tên tài khoản đã tồn tại'
        conn.close()
        return render_template('register.html', err=session['register-admin-err'])
    elif len(password) < 6:
        session['register-admin-err'] = 'Mật khẩu phải dài hơn 6 kí tự'
        conn.close()
        return render_template('register.html', err=session['register-admin-err'])
    else:
        try:
            id = ''

            cursor2 = conn.cursor()

            pw_hash = md5(password.encode()).hexdigest()
            
            cursor2.execute("INSERT INTO dbo.user_app (name_user, phone_user) VALUES (N'{name_user}', '{phone_user}')".format(name_user=fullname, phone_user=phone))
            conn.commit()

            cursor3 = conn.cursor()
            query2 = "SELECT id_user FROM dbo.user_app WHERE name_user = N'{name_user}' AND phone_user = '{phone_user}'".format(name_user=fullname, phone_user=phone)
            cursor3.execute(query2)
            for row in cursor3.fetchall():
                id = row[0]
                break

            cursor4 = conn.cursor()
            cursor4.execute("INSERT INTO dbo.user_login (us, pw, id_user, roll) VALUES ('{us}', '{pw}', '{id_user}', {roll})".format(us=username, pw=pw_hash, id_user=id, roll=1))
            conn.commit()

            conn.close()

            return 'Tạo tài khoản QTV ' + fullname + ' Thành công <br> <a href="/">Trang chủ</a> <br> <a href="/logout">Đăng xuất</a>'
        except Exception as e:
            return(str(e))

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/brand/<id>')
def product_page(id):
    name = ''
    logo = ''
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name_brand, logo_brand FROM dbo.brand WHERE id_brand = '{id_brand}' ".format(id_brand = id))
    for row in cursor.fetchall():
        name = row[0]
        logo = row[1]
        break
    return render_template('product.html', name_brand=name, logo_brand=logo)


@app.route('/acc-manager', methods = ['POST', 'GET'])
def manager_account():
    r = session['roll']
    db = []

    conn = connection()
    cursor = conn.cursor()

    if r == 0:
        cursor.execute("SELECT user_app.id_user, name_user, phone_user, us, pw, roll FROM dbo.user_app INNER JOIN dbo.user_login ON user_app.id_user = user_login.id_user")
    else:
        cursor.execute("SELECT user_app.id_user, name_user, phone_user, us, pw, roll FROM dbo.user_app INNER JOIN dbo.user_login ON user_app.id_user = user_login.id_user WHERE roll = 2")
    
    for row in cursor.fetchall():
        db.append({"id": row[0], "name_user": row[1], "phone_user": row[2], "us": row[3],"pw": row[4], "roll": row[5]})
    conn.close()
    return render_template('acc_manager.html', table=db)

@app.route('/acc-manager/edit/<record_id>')
def edit(record_id):
    lis_acc = []
    conn = connection()
    
    cursor1 = conn.cursor()
    query1 = "SELECT user_login.us, name_user, phone_user FROM dbo.user_app INNER JOIN dbo.user_login ON user_app.id_user = user_login.id_user WHERE user_app.id_user = '{id}'".format(id=record_id)
    cursor1.execute(query1)
    for row in cursor1.fetchall():
        lis_acc.append({"us": row[0], "name_user": row[1], "phone_user": row[2]})
    return render_template('acc_edit.html', action='edit', account=lis_acc)

@app.route('/acc-manager/edit/<record_id>', methods = ['POST', 'GET'])
def edit_form(record_id):
    db_us = ''
    db_name = ''
    db_phone = ''
    lis_us = []

    conn = connection()
    
    cursor1 = conn.cursor()
    query1 = "SELECT user_login.us, name_user, phone_user FROM dbo.user_app INNER JOIN dbo.user_login ON user_app.id_user = user_login.id_user WHERE user_app.id_user = '{id}'".format(id=record_id)
    cursor1.execute(query1)
    for row in cursor1.fetchall():
        db_us = row[0]
        db_name = row[1]
        db_phone = row[2]
        break
    
    cursor2 = conn.cursor()
    query2 = "SELECT us FROM dbo.user_login WHERE id_user != '{id}'".format(id=record_id)
    cursor2.execute(query2)
    for row in cursor2.fetchall():
        lis_us.append(row[0])

    fullname = request.form['Name']
    phone = request.form['Phone']
    username = request.form['Username']

    if len(phone) != 10:
        session['edit-err'] = 'SĐT không hợp lệ'
        conn.close()
        return render_template('acc_edit.html', action='edit', err=session['edit-err'], fullname=fullname, phone=phone, username=username)
    elif fullname == db_name and phone == db_phone and username == db_us:
        session['edit-err'] = 'Thông tin chưa thay đổi'
        conn.close()
        return render_template('acc_edit.html', action='edit', err=session['edit-err'], fullname=fullname, phone=phone, username=username)
    elif username in lis_us:
        session['edit-err'] = 'Tài khoản đã tồn tại'
        conn.close()
        return render_template('acc_edit.html', action='edit', err=session['edit-err'], fullname=fullname, phone=phone, username=username)
    else:
        try:           
            cursor2 = conn.cursor()
            cursor2.execute("UPDATE dbo.user_app SET name_user = N'{name_user}', phone_user = '{phone_user}' WHERE id_user = '{id}'".format(name_user=fullname, phone_user=phone, id=record_id))
            conn.commit()

            cursor3 = conn.cursor()
            cursor3.execute("UPDATE dbo.user_login SET us = '{usname}' WHERE id_user = '{id}'".format(usname=username, id=record_id))
            conn.commit()

            conn.close()

            return 'Thay đổi tài khoản ' + fullname + ' thành công <br> <a href="/">Trang chủ</a> <br> <a href="/acc-manager">Quản lý tài khoản</a>'
        except Exception as e:
            return(str(e))

@app.route('/acc-manager/change-pw/<record_id>')
def change_pw(record_id):
    return render_template('acc_edit.html', action='change-password')

@app.route('/acc-manager/change-pw/<record_id>', methods = ['POST', 'GET'])
def change_pw_form(record_id):
    password = ''
    fullname = ''

    conn = connection()
    
    cursor1 = conn.cursor()
    query1 = "SELECT pw FROM dbo.user_login WHERE id_user = '{id}'".format(id=record_id)
    cursor1.execute(query1)
    for row in cursor1.fetchall():
        password = row[0]
        break

    pw = request.form['Password']
    pw_hash = md5(pw.encode()).hexdigest()
    re_pw = request.form['Re_Password']

    if len(pw) < 6:
        session['edit-err'] = 'Mật khẩu phải dài hơn 6 kí tự'
        conn.close()
        return render_template('acc_edit.html', action='change-password', err=session['edit-err'])
    elif pw != re_pw:
        session['edit-err'] = 'Mật khẩu không giống nhau'
        conn.close()
        return render_template('acc_edit.html', action='change-password', err=session['edit-err'])
    elif pw_hash == password:
        session['edit-err'] = 'Bạn đang sử dụng mật khẩu này'
        conn.close()
        return render_template('acc_edit.html', action='change-password', err=session['edit-err'])
    else:
        try:           
            cursor2 = conn.cursor()
            cursor2.execute("UPDATE dbo.user_login SET pw = N'{password}' WHERE id_user = '{id}'".format(password=pw_hash, id=record_id))
            conn.commit()

            cursor3 = conn.cursor()
            query3 = "SELECT name_user FROM dbo.user_app WHERE id_user = '{id}'".format(id=record_id)
            cursor3.execute(query3)
            for row in cursor3.fetchall():
                fullname = row[0]
                break

            conn.close()

            return 'Thay đổi mật khẩu tài khoản ' + fullname + ' thành công <br> <a href="/">Trang chủ</a> <br> <a href="/acc-manager">Quản lý tài khoản</a>'
        except Exception as e:
            return(str(e))

@app.route('/acc-manager/delete/<record_id>', methods = ['POST', 'GET'])
def delete(record_id):
    usname = ''
    conn = connection()
    
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    cursor3 = conn.cursor()

    query1 = "SELECT us FROM dbo.user_login WHERE id_user = '{id}'".format(id=record_id)
    cursor1.execute(query1)
    for row in cursor1.fetchall():
        usname = row[0]
        break

    query2 = "DELETE FROM dbo.user_login WHERE id_user = '{id}'".format(id=record_id)
    cursor2.execute(query2)
    conn.commit()

    query3 = "DELETE FROM dbo.user_app WHERE id_user = '{id}'".format(id=record_id)
    cursor3.execute(query3)
    conn.commit()

    conn.close()
    return 'Xóa tài khoản ' + usname + ' Thành công <br> <a href="/">Trang chủ</a> <br> <a href="/acc-manager">Quản lý tài khoản</a>'

if __name__ == '__main__':
    app.run(debug=True)