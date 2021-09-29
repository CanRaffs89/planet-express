from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email

app = Flask(__name__)

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgrespass@localhost/planex'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Quote(db.Model):
    __tablename__ = 'quote'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    destination = db.Column(db.String(200))
    weight = db.Column(db.String(200))

    def __init__(self, email, destination, weight):
        self.email = email
        self.destination = destination
        self.weight = weight

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        email = request.form['email']
        destination = request.form['destination']
        weight = request.form['weight']
        if email == '' or destination == '' or weight == '':
            return render_template('index.html', message='Please fill out all required fields')
        else:
            data = Quote(email, destination, weight)
            db.session.add(data)
            db.session.commit()
            send_email(email, destination, weight)
        return render_template('success.html')

@app.route('/success')
def succes():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')