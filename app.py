from flask import Flask, request, render_template, redirect, url_for, redirect, session, flash, request
from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from flask_wtf import FlaskForm
# from wtforms import StringsField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Length, ValidationError
# from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits_test.db'
db = SQLAlchemy(app)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit = db.Column(db.String(100), nullable=False)
    habit_description = db.Column(db.String(300), nullable=False)
    frequency = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

def insert_values():
    with app.app_context():
        db.create_all()

        # Insert random values
        random_profiles = [
            Profile(habit="Exercise", habit_description="Daily morning run", frequency="Daily", difficulty="Medium", email="user1@example.com"),
            Profile(habit="Reading", habit_description="Read 20 pages of a book", frequency="Daily", difficulty="Easy", email="user2@example.com"),
            Profile(habit="Meditation", habit_description="Meditate for 15 minutes", frequency="Daily", difficulty="Hard", email="user3@example.com")
        ]

        for profile in random_profiles:
            db.session.add(profile)
        
        db.session.commit()

        # Query the database to check if values are inserted
        profiles = Profile.query.all()
        for profile in profiles:
            print(f"ID: {profile.id}, Habit: {profile.habit}, Description: {profile.habit_description}, Frequency: {profile.frequency}, Difficulty: {profile.difficulty}, Email: {profile.email}")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)


# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view ="login"

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(80), nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    
# class RegisterForm(FlaskForm):
#     username = StringsField(ValidationError=[InputRequired(), Length(
#         min=4, max=20)], render_kw={"placeholder": "Username"})
#     password = PasswordField(validators=[InputRequired(), Length(
#         min=4, max=20)], render_kw={"placeholder": "Password"})
    
#     sumbit = SubmitField("Register")

#     def validate_username(self, username):
#         existing_user_username = User.query.filter_by(
#             username=username.data).first()
        
#         if existing_user_username:
#             raise ValidationError(
#                 "That username already exists. PLease choose a different one.")

        

# class LoginForm(FlaskForm):
#     username = StringsField(ValidationError=[InputRequired(), Length(
#         min=4, max=20)], render_kw={"placeholder": "Username"})
#     password = PasswordField(validators=[InputRequired(), Length(
#         min=4, max=20)], render_kw={"placeholder": "Password"})
    
#     sumbit = SubmitField("login")

@app.route('/', methods=['GET'])
def home():
   return render_template('homePage.html')
   session.pop('username', None)
   if 'username' in session:
       return redirect (url_for('dashboard'))
   


   return render_template('login.html')

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

    
    # form = LoginForm()
    # if form.vaildate_on_submit():
    #     user=User.query.filter_by(username=form.username.data).first()
    #     if user:
    #         if bcrypt.check_password_hash(user.password, form.password.data):
    #             login_user(user)
    #             return redirect(url_for('dashboard'))
    


@app.route ('/dashboard')

def dashboard():
    if 'username' not in session:
        return redirect (url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])

def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

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

        new_user=User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        flash("Registed Successful")
        return redirect(url_for('login'))

    return render_template('register.html')

    # form = RegisterForm()

    # if form.validate_on_username():
    #     hashed_password = bcrypt.generate_password_hash(form.password.data)
    #     new_user = User(username=form.username.data, password=hashed_password)
    #     db.session.add(new_user)
    #     db.session.commit()
    #     return redirect(url_for('login'))

    




 

@app.route('/dashboard')
def dashboard():
    return render_template('dashboardPage.html')

@app.route('/habitPage', methods=['GET', 'POST'])
def habitPage():
    
    if request.method == "POST":
        habit = request.form['habit']
        habit_description = request.form['habit_description']
        frequency = request.form['frequency']
        difficulty = request.form['difficulty']
        email = request.form['email']
        print(habit)
        print(habit_description)
        print(frequency)
        print(difficulty)
        print(email)


        new_habit = Profile(
            habit=habit,
            habit_description=habit_description,
            frequency=frequency,
            difficulty=difficulty,
            email=email
        )
        db.session.add(new_habit)
        db.session.commit()

        return render_template('dashboardPage.html', habit_name=habit, habit_description=habit_description, frequency=frequency, difficulty=difficulty)
        #return redirect(url_for('dashboard', habit_name=habit, habit_description=habit_description, frequency=frequency, difficulty=difficulty))  # Redirect to the form page or another page after submission
        
    return render_template('habitPage.html')

@app.route('/submit', methods=['POST'])
def submit():
    return "Form submitted"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    


