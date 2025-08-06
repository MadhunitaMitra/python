from flask import Flask, render_template, request
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


if __name__ == '__main__':
    app.run(debug=True,port=5050)