from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        blood_group = request.form['blood_group']
        phone = request.form['phone']
        email = request.form['email']
        city = request.form['city']
        role = request.form['role']
        password = request.form['password']

        conn = get_db_connection()
        try:
            conn.execute("""INSERT INTO users (name, age, gender, blood_group, phone, email, city, role, password)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                         (name, age, gender, blood_group, phone, email, city, role, password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists. Please choose another."
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE name = ? AND password = ?', (name, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            return redirect('/dashboard')
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    groups = conn.execute('SELECT blood_group, COUNT(*) as count FROM users GROUP BY blood_group').fetchall()
    chart_data = {
        'labels': [row['blood_group'] for row in groups],
        'values': [row['count'] for row in groups]
    }

    conn.close()
    return render_template('dashboard.html', user=user, chart_data=chart_data, results=None)

@app.route('/search', methods=['POST'])
def search():
    if 'user_id' not in session:
        return redirect('/login')
    blood_group = request.form['blood_group']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    results = conn.execute('SELECT * FROM users WHERE blood_group = ? AND id != ?', (blood_group, session['user_id'])).fetchall()

    groups = conn.execute('SELECT blood_group, COUNT(*) as count FROM users GROUP BY blood_group').fetchall()
    chart_data = {
        'labels': [row['blood_group'] for row in groups],
        'values': [row['count'] for row in groups]
    }

    conn.close()
    return render_template('dashboard.html', user=user, results=results, chart_data=chart_data)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

