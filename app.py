from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # This is a basic check; in real applications, you'll need more secure ways to handle this
    if username == "user" and password == "pass":
        return render_template('dashboard.html', username=username)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
