import json
from flask import Flask ,flash, render_template, request, redirect,url_for
from flask_login import UserMixin, LoginManager,login_required,logout_user,login_user
from werkzeug.security import generate_password_hash ,check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

db = SQLAlchemy(app)

app.secret_key = 'djehhejed'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'



class Auth(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    passcode = db.Column(db.String)
    


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date, default=datetime.datetime.now)
    userName = db.Column(db.String(500))
    fileNumber = db.Column(db.String(500))
    blockName  = db.Column(db.String(500))
    price = db.Column(db.Integer)
    mobileNumber = db.Column(db.Integer)
    profit  = db.Column(db.Integer)
    


@app.route('/registerPassword', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        password = request.form.get('password')
        old = Auth.query.filter_by(passcode = old_password).first()
        if old:
            db.session.delete(old)
            db.session.commit()
            new = Auth(passcode = password)
            db.session.add(new)
            db.session.commit()
            flash('passcode changed succesfully', category='success')            
            return redirect(url_for('home'))
        else:flash('acces denied', category='error')
    return render_template('registerPasword.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        passco = Auth.query.filter_by(passcode=password).first()

        if password == 'IAMADMIN':
            return redirect(url_for('register'))
        elif not passco:
            flash('Incorrect credintials')
            return render_template('login.html')
        elif password:
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect credentials')
            return render_template('login.html')                
    return render_template('login.html')


@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
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
        return redirect(url_for('dashboard'))

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
    return redirect(url_for('dashboard'))
    

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)