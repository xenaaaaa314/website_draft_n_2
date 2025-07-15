from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Required for flash and session

# Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'info@oramatech.ai'
app.config['MAIL_PASSWORD'] = 'ckhk olqp npws kzha'  # Use env variable in prod
app.config['MAIL_DEFAULT_SENDER'] = 'info@oramatech.ai'

mail = Mail(app)

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/article')
def article():
    return render_template('article.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/leaderboard_extended')
def leaderboard_extended():
    if not session.get('authenticated'):
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('leaderboard.html')


@app.route('/join_us')
def join_us():
    return render_template('join_us.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = Message(f'Contact Form Message from {name}',
                      recipients=['info@oramatech.ai'])
        msg.body = f"From: {name} <{email}>\n\n{message}"

        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            print(e)
            flash('Failed to send message.', 'error')

        return redirect('/contact')

    return render_template('contact.html')

# --- Login and Protected Page ---

PASSWORD = "orama2025" 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['authenticated'] = True
            flash('Login successful.', 'success')
            return redirect(url_for('leaderboard_extended'))  # Default redirect
        else:
            flash('Incorrect password.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    flash('Logged out.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
