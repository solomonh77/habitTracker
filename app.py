from flask import Flask, render_template, url_for, redirect, session, flash, request
from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from flask_wtf import FlaskForm
# from wtforms import StringsField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Length, ValidationError
# from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
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
    sg = sendgrid.SendGridAPIClient(api_key='sendgrid api')
    from_email = Email('helana12358@gmail.com')
    to_email = To(email)
    subject = 'Hello! this is a reminder from Habit Tracker website!'
    content = Content("text/plain", "Remember to do your habit today! Your habit you want to develop is: " + habit_description + "  -- Have Fun!!")

    mail = Mail(from_email, to_email, subject, content)
    response = sg.send(mail)
   
    try:
        response = sg.send(mail)
        # Check the response
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.body}")
        print(f"Response Headers: {response.headers}")

        # Check if the status code indicates success
        if response.status_code == 202:
            print("Email sent successfully!")
        else:
            print("Failed to send email.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Schedule email every other day
def schedule_email():
    '''
    if frequency == "daily" or frequency== "7" or frequency == "everyday":
        scheduler.add_job(send_email_task, 'interval', days=7)
    if frequency == "1" or frequency == "one day a week":
        scheduler.add_job(send_email_task, 'interval', days=1)
    if frequency == "2":
        scheduler.add_job(send_email_task, 'interval', days=2)
    if frequency == "3":
        scheduler.add_job(send_email_task, 'interval', days=3)
    if frequency == "4":
        scheduler.add_job(send_email_task, 'interval', days=4)
    if frequency == "5":
        scheduler.add_job(send_email_task, 'interval', days=5)
    if frequency == "6":
        scheduler.add_job(send_email_task, 'interval', days=6)
    '''
    scheduler.add_job(send_email_task, 'interval', seconds=10)
   


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits_test.db'
db = SQLAlchemy(app)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit = db.Column(db.String(100), nullable=False)
    habit_description = db.Column(db.String(300), nullable=False)
    frequency = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'


#
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(80), nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    

@app.route('/', methods=['GET'])
def home():
   
   session.pop('username', None)
   if 'username' in session:
       return redirect (url_for('dashboard'))
   


   return render_template('homePage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username= request.form['username']
        password= request.form['password']
        user= User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username']=username
            return redirect(url_for('dashboard'))
        flash("Invaild Username Or Password")
    return render_template('login.html')


@app.route ('/dashboard')
def dashboard():
   
    if 'username' not in session:
        return redirect (url_for('login'))
    return render_template('dashboardPage.html')
 

@app.route('/logout', methods=['GET', 'POST'])

def logout():
    session.pop('username', None)
    
    return render_template('logout.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username= request.form['username']
        password= request.form['password']
        if User.query.filter_by(username=username).first():
            flash("User already taken.")
            return redirect(url_for('register'))
        global new_user
        new_user=User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        flash("Registed Successful")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/habitPage', methods=['GET', 'POST'])
def habitPage():
    global email
    global habit_description
    global frequency
    if request.method == "POST":
        habit = request.form['habit']
        habit_description = request.form['habit_description']
        frequency = request.form['frequency']
        difficulty = request.form['difficulty']
        email = request.form['email']
        
    # form = RegisterForm()

    # if form.validate_on_username():
    #     hashed_password = bcrypt.generate_password_hash(form.password.data)
    #     new_user = User(username=form.username.data, password=hashed_password)
    #     db.session.add(new_user)
    #     db.session.commit()
    #     return redirect(url_for('login'))
    
        new_habit = Profile(
            habit=habit,
            habit_description=habit_description,
            frequency=frequency,
            difficulty=difficulty,
            email=email
        )
        try:
            db.session.add(new_habit)
            db.session.commit()
            print("it was successful!")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
        schedule_email()

        return render_template('dashboardPage.html', habit_name=habit, habit_description=habit_description, frequency=frequency, difficulty=difficulty)
        #return redirect(url_for('dashboard'))  # Redirect to the form page or another page after submission
       
    return render_template('habitPage.html')

@app.route('/submit', methods=['POST'])
def submit():
    return "Form submitted"




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5447)

    
