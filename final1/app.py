from flask import Flask, render_template, request, redirect, url_for, g, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'private_key'
# Thay đổi các thông tin kết nối MySQL của bạn
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'QuangPhuc0609003',
    'database': 'Account'
}
# Kết nối đến cơ sở dữ liệu
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('introduction.html')

def check_login(username, password):
    # Thực hiện kiểm tra đăng nhập trong cơ sở dữ liệu
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    # Kiểm tra kết quả
    if result:
        return True
    else:
        return False 
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lấy thông tin đăng nhập từ form
        username = request.form['username']
        password = request.form['password']

        # Thực hiện kiểm tra đăng nhập ở đây
        if check_login(username, password):
            # Đăng nhập thành công, chuyển hướng đến trang comic.html
            return redirect(url_for('home'))
        else:
            # Đăng nhập thất bại, có thể xử lý thông báo lỗi hoặc chuyển hướng đến trang khác
            return redirect(url_for('login'))

    # Nếu là yêu cầu GET, render trang đăng nhập
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Lấy thông tin từ form
        username = request.form['username']
        password = request.form['password']

        # Thực hiện truy vấn để thêm người dùng mới vào cơ sở dữ liệu
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()
            return redirect(url_for('login'))  # Chuyển hướng sau khi tạo tài khoản thành công
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return "Error creating account"

    return render_template('signup.html')

def check_login(username, password):
    # Thực hiện kiểm tra đăng nhập trong cơ sở dữ liệu
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    # Kiểm tra kết quả
    if result:
        # Lưu thông tin người dùng vào session
        session['username'] = username
        return True
    else:
        return False

@app.route('/comic')
def comic():
    return render_template('comic.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username=username)
    else:
        return redirect(url_for('login'))

@app.route('/introduction')
def intro():
    return render_template('introduction')

# Đóng kết nối với cơ sở dữ liệu khi ứng dụng kết thúc
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'mysql_db'):
        g.mysql_db.close()

if __name__ == '__main__':
    app.run(debug=True)
