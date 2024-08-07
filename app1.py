from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits_test2.db'
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

if __name__ == '__main__':
    insert_values()
    import os # Print the current working 
    print("Current working directory:", os.getcwd())