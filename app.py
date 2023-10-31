from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '12345678'  # Change this to a real secret key in production

# Hardcoded user credentials and their accounts
users = {
    'user1': {
        'password': 'pass1',
        'accounts': [
            {'account_number': '00001', 'balance': 1000},
            {'account_number': '00002', 'balance': 2500},
        ]
    },
    'user2': {
        'password': 'pass2',
        'accounts': [
            {'account_number': '00003', 'balance': 3000},
        ]
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    # If user is already logged in, redirect to the dashboard
    if 'username' in session:
        return redirect(url_for('dashboard'))
    # Handle login
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Login Failed', 401
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']
    user_accounts = users[username]['accounts']
    return render_template('dashboard.html', username=username, accounts=user_accounts)

@app.route('/logout')
def logout():
    # Remove user from session
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
