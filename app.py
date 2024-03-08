from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '6c70755e8ff61cd0a6b48228f3754a689a18bd2cd26770a1' 


db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app)


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(255))
    bot_response = db.Column(db.String(255))

admin.add_view(ModelView(ChatMessage, db.session))







class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Add this line for email column
    password = db.Column(db.String(80), nullable=False)
admin.add_view(ModelView(User, db.session))

def simple_chatbot(user_message):
    greetings = ['hi', 'hello', 'hey']
    farewells = ['bye', 'goodbye']
    about = ['ravikiran', 'sir']
    students = ['vijay', 'chandra', 'bharadwaj', 'pavan', 'subbarao', 'uday']
    virat=['virat','kohli','virat kohli','king']
    pavan=['pen','marker','stylograph']
    bharat=['facebook fonder']
    vijay=['capital of chhattisgarh']
    chandra=['potato','tomato','carrot','bean','onion']
    uday=['india','bharat']
    kanth=['python']
    bhumi=['chandrayan','launch','moon mission']

    user_message_lower = user_message.lower()

    if any(greeting in user_message_lower for greeting in greetings):
        return 'Hello! How can I help you?'

    if any(farewell in user_message_lower for farewell in farewells):
        return 'Goodbye! Have a great day.'
    if any(abouting in user_message_lower for abouting in about):
        return 'Lecturer in The ICFAI University'
    if any(student in user_message_lower for student in students):
        return 'Final year student of The ICFAI University'
    if any(kohli in user_message_lower for kohli in virat):
        return 'Virat Kohli, an Indian cricketer, is a prolific batsman and former captain, inspiring with consistent performances.'
    if any(pavans in user_message_lower for pavans in pavan):
        return 'an instument for writing or drawing with ink'
    if any(chandras in user_message_lower for chandras in chandra):
        return 'edible portion of a plant .usually used to eat'
    if any(bharats in user_message_lower for bharats in bharat):
        return 'Mark Zuckerberg'
    if any(vijays in user_message_lower for vijays in vijay):
        return 'capital of chhattisgarh is Raipur'
    if any(udays in user_message_lower for udays in uday):
        return ' Independant nation Declared In August'
    if any(kanths in user_message_lower for kanths in kanth):
        return 'python is a high-level general purpose programming language.Python is dynamically typed and garbage collected'
    if any(bhumis in user_message_lower for bhumis in bhumi):
        return 'Chadrayaan three lanuched on 14th July 2023'
    return 'I didn\'t understand that. Can you please rephrase?'


@app.route('/chat')
def index():
    return render_template('index.html')


@app.route('/get_response', methods=['GET'])
def get_response():
    user_message = request.args.get('userMessage')
    bot_response = simple_chatbot(user_message)

    
    with app.app_context():
        db.create_all() 
        chat_message = ChatMessage(user_message=user_message, bot_response=bot_response)
        db.session.add(chat_message)
        db.session.commit()

    return jsonify({'response': bot_response})


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            return redirect(url_for('index'))  
        else:
            error = 'Invalid credentials. Please try again.'

    return render_template('login.html', error=error)


@app.route('/', methods=['GET', 'POST'])
def register():
    error = None  

    if request.method == 'POST':
        new_username = request.form.get('new_username')
        new_email = request.form.get('new_email')
        new_password = request.form.get('new_password')

        existing_user = User.query.filter_by(username=new_username).first()

        if existing_user:
            error = 'Username already exists. Please choose another one.'
        else:
            new_user = User(username=new_username,email=new_email, password=new_password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))  

    return render_template('register.html', error=error)

if __name__ == '__main__':
    with app.app_context():
        if db.engine.url.drivername != 'sqlite':
            db.create_all()
        else:
            print("You are using SQLite, the database will be created automatically.")

    app.run(debug=True)
