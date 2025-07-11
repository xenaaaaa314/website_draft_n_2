from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)  # ✅ Create app first
app.secret_key = 'super-secret-key'

# ✅ Then configure mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'info@oramatech.ai'
app.config['MAIL_PASSWORD'] = 'your_app_password'  # Replace with your actual app password
app.config['MAIL_DEFAULT_SENDER'] = 'info@oramatech.ai'

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/article')
def article():
    return render_template('article.html')

@app.route('/leaderboard')
def leaderboard():
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
                      recipients=['recipient@example.com'])  # Replace with your target email
        msg.body = f"From: {name} <{email}>\n\n{message}"
        
        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            print(e)
            flash('Failed to send message.', 'error')

        return redirect('/contact')

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
