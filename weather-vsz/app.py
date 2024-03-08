# app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Index Route
@app.route('/')
def index():
    return render_template('index.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        username = request.form['username']
        password = request.form['password']
        # Perform authentication checks
        # ...
        # Redirect to appropriate page after successful login
        return redirect(url_for('index'))
    return render_template('login.html')

# Register Route

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic here
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Perform registration steps
        # ...
        # Redirect to appropriate page after successful registration
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)