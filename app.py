from flask import Flask, render_template, url_for, redirect, session, flash, request
from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from flask_wtf import FlaskForm
# from wtforms import StringsField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Length, ValidationError
# from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


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
   session.pop('username')
   if 'username' in session:
       return redirect (url_for('dashboard'))
   


   return render_template('loginhtml')

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

    




 


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    


