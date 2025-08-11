from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "ffdtrdbbftdwqwasviuhihiugcghctr"

def get_db_connection():
    
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'py-demo'
    )

@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('view'))
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        # hashed_password = generate_password_hash(password)
        # Check if user already exists
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            return render_template('register.html', message="User already exists")
        # Insert new user
        cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('view'))
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and user['password'] == password:
            session['user'] = user['username']
            session['user_id'] = user['id']
            return redirect(url_for('view'))
        else:
            return render_template('login.html', message="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/view')
def view():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view.html', students=students)

@app.route('/delete/<int:id>')
def delete(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('view'))

@app.route('/edit/<int:id>')
def edit(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE student_id = %s", (id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit.html', student=student)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    name = request.form['full_name']
    dob = request.form['dob']
    gender = request.form['gender']
    department = request.form['department']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET full_name = %s, dob = %s, gender = %s, department = %s, email = %s, phone = %s, address = %s WHERE student_id = %s", (name, dob, gender, department, email, phone, address, id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('view'))

@app.route('/view/<int:id>')
def view_student(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE student_id = %s", (id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('view_student.html', student=student)

if __name__ == '__main__':
    app.run(debug=True,port=5050)