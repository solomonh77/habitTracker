from flask import Flask, request, render_template_string, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

app = Flask(__name__)

# Global variable to store email details
email_details = {}

# Set up APScheduler
scheduler = BackgroundScheduler()
scheduler.start()

def send_email_task():
    sg = sendgrid.SendGridAPIClient(api_key='YOUR_SENDGRID_API_KEY')
    from_email = Email(email_details['from_email'])
    to_email = To(email_details['to_email'])
    subject = email_details['subject']
    content = Content("text/plain", email_details['body'])

    mail = Mail(from_email, to_email, subject, content)
    response = sg.send(mail)

    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.body}")
    print(f"Response Headers: {response.headers}")

# Schedule email every other day
def schedule_email():
    scheduler.add_job(send_email_task, 'interval', days=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global email_details
        email_details = {
            'from_email': request.form['from_email'],
            'to_email': request.form['to_email'],
            'subject': request.form['subject'],
            'body': request.form['body']
        }
        schedule_email()  # Schedule the email
        return redirect(url_for('success'))
    return render_template_string('''
        <form method="post">
            From Email: <input type="email" name="from_email" required><br>
            To Email: <input type="email" name="to_email" required><br>
            Subject: <input type="text" name="subject" required><br>
            Body: <textarea name="body" required></textarea><br>
            <input type="submit" value="Schedule Email">
        </form>
    ''')

@app.route('/success')
def success():
    return 'Email has been scheduled successfully!'

if __name__ == '__main__':
    app.run(debug=True)