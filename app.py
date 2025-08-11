from flask import Flask, render_template, request, redirect,url_for
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'py-demo'
    )

@app.route('/')
def home():
    conn = get_db_connection()
    if not conn:
        message = "Database connection failed"
    else:
        message = "Database connection successful"
    return render_template('index.html',message=message)

@app.route('/about')
def about():
    name = "Madhunita"
    return render_template('about.html', name=name)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('register.html', message="User created successfully")
    return render_template('register.html')

@app.route('/view')
def view():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view.html', students=students)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('view'))

@app.route('/edit/<int:id>')
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE student_id = %s", (id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit.html', student=student)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE student_id = %s", (id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('view_student.html', student=student)

if __name__ == '__main__':
    app.run(debug=True,port=5050)