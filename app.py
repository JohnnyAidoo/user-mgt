from email.policy import default
from flask import Flask ,flash, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)

db = SQLAlchemy(app)

app.secret_key = 'djehhejed'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date, default=datetime.datetime.now)
    userName = db.Column(db.String(500))
    fileNumber = db.Column(db.String(500))
    blockName  = db.Column(db.String(500))
    price = db.Column(db.Integer)
    mobileNumber = db.Column(db.Integer)
    profit  = db.Column(db.Integer)
    



@app.route('/')
def home():
    users = User.query.all()
    return render_template('index.html' , users=users)

@app.route('/adduser')
def adduser():
    return render_template('add.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        userName=request.form.get('userName')
        fileNumber=request.form.get('fileNumber')
        blockName=request.form.get('blockName')
        price=request.form.get('price')
        mobileNumber=request.form.get('mobileNumber')
        profit=request.form.get('profit')
        
        newUser = User(userName=userName, fileNumber=fileNumber, blockName=blockName, price=price,mobileNumber=mobileNumber,profit=profit)
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/update/<int:user_id>')
def update(user_id):
    entry = User.query.filter_by(id=user_id).first()
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('adduser'))

@app.route('/delete/<int:user_id>')
def delete(user_id):
    entry = User.query.filter_by(id=user_id).first()
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('home'))
    


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)