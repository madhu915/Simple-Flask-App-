from flask import Flask, flash, render_template, request, session, redirect, json
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.secret_key = "madz-hulahoops-2022"

#mongoengine in flask
app.config['MONGODB_SETTINGS'] = {
    'db': 'usersdb',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class User(db.Document):
    name = db.StringField()
    email = db.StringField()
    password= db.StringField()


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        _name=request.form['inputName']
        _email=request.form['inputEmail']
        _password=request.form['inputPassword']

    #validation of users
        if _name and _email and _password:
            users=User.objects(email=_email).first()
            if not users:
                newuser=User(name=_name,email=_email,password=_password)
                newuser.save()
                msg='{"html":"Successfully Registered!"}'
                msghtml=json.loads(msg)
                return msghtml["html"]
            else:
                msg='{"html":"<h3>User already exists!</h3>"}'
                msghtml=json.loads(msg)
                return msghtml["html"]
        else:
            msg='{"html":"<h3>Please check the entered details</h3>"}'
            msghtml=json.loads(msg)
            return msghtml["html"]
    else:
        return render_template("signup.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        _user=request.form['inputEmail']
        _password=request.form['inputPassword']
        users=User.objects(email=_user).count()
        if users>0:
            user_=User.objects(email=_user).first()
            passwrd=user_['password']
            if passwrd==_password:
                session['sessionusername']=_user
                return render_template('home.html')
            else:
                flash('Invalid login!!!')            
                return render_template('signin.html',error='Invalid login!!!')

        else:
            return render_template('signin.html',error='Invalid username!!!')
    return render_template('signin.html')

@app.route('/home')
def userHome():
    print(session.get('sessionusername'))   
    if session.get('sessionusername'):
        return render_template('home.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')
 

@app.route('/logout')
def logout():
    session.pop('sessionusername',None)
    return redirect('/')

if(__name__=='__main__'):
    app.run(debug=True)










