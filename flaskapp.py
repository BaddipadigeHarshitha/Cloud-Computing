from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# SQLite setup
# Use the full path to ensure the database is correctly located
DB_PATH = '/home/ubuntu/myflaskapp/users.db'

def init_db():
    conn = sqlite3.connect('/home/ubuntu/myflaskapp/users.db')

    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT, firstname TEXT, lastname TEXT, email TEXT)''')
    conn.commit()
    conn.close()

init_db()  # Call to initialize the database

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
                  (username, password, firstname, lastname, email))
        conn.commit()
        flash('Registration successful! Please log in.')
    except sqlite3.IntegrityError:
        flash('Username already exists. Please choose a different one.')
    conn.close()

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Attempting login with username: {username} and password: {password}")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Check for the user
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()

        if user:
            print("User found, checking password.")
            if user[1] == password:
	        # Compare with plain text password for testing
                print("Login successful!")
                return redirect(url_for('profile', username=username))
            else:
                print("Password does not match.")
                flash('Invalid username or password. Please try again.')
        else:
            print("User not found.")
            flash('Invalid username or password. Please try again.')

    return render_template('login.html')

@app.route('/profile/<username>')
def profile(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    return render_template('profile.html', user=user)




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

