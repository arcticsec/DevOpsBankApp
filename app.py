from flask import Flask, render_template, request, redirect, url_for, session, flash

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

@app.route('/create_account', methods=['POST'])
def create_account():
    if 'username' not in session:
        flash('You must be logged in to create an account.', 'error')
        return redirect(url_for('index'))

    username = session['username']
    new_account_number = f"{int(users[username]['accounts'][-1]['account_number']) + 1:05d}"
    users[username]['accounts'].append({
        'account_number': new_account_number,
        'balance': 0,
        'transactions': []  # Initialize the transactions list
    })
    flash('New account created successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/transfer', methods=['POST'])
def transfer():
    if 'username' not in session:
        flash('You must be logged in to transfer funds.', 'error')
        return redirect(url_for('index'))

    from_account_num = request.form.get('from_account')
    to_account_num = request.form.get('to_account')
    amount = float(request.form.get('amount'))

    # Helper function to find an account by number across all users
    def find_account_by_number(account_number):
        for user_accounts in users.values():
            for account in user_accounts['accounts']:
                if account['account_number'] == account_number:
                    return account
        return None

    from_account = find_account_by_number(from_account_num)
    to_account = find_account_by_number(to_account_num)

    if from_account and to_account and from_account['balance'] >= amount:
        # Perform the transfer
        from_account['balance'] -= amount
        to_account['balance'] += amount

        # Record the transactions
        from_account.setdefault('transactions', []).append({'type': 'Transfer Out', 'amount': -amount})
        to_account.setdefault('transactions', []).append({'type': 'Transfer In', 'amount': amount})

        flash('Transfer successful!', 'success')
    else:
        flash('Transfer failed. Check account numbers and balance.', 'error')

    return redirect(url_for('dashboard'))

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
