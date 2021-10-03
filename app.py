from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email

app = Flask(__name__)

ENV = 'prod'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgrespass@localhost/planex'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ekgucbrioizozn:fd2e5017f9f9d31751c89f5ebaf27158ef655f4a4303ab60cfac13d19bdbae8e@ec2-44-194-201-94.compute-1.amazonaws.com:5432/d2a2rrftjl47b4'

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
        price = 120
        if email == '' or destination == '' or weight == '':
            return render_template('index.html', message='Please fill out all required fields')
        else:
            if destination == 'Mercury' or destination == 'Venus' or destination == 'Mars' or destination == 'Jupiter':
                price = 45
            if destination == 'Saturn' or destination == 'Uranus' or destination == 'Neptune' or destination == 'Pluto':
                price = 90
            data = Quote(email, destination, weight)
            db.session.add(data)
            db.session.commit()
            send_email(email, destination, weight, price)
        return render_template('success.html')

@app.route('/success')
def succes():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')