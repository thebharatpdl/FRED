from flask import render_template,redirect,url_for,session,flash,request
from app import mysql,secret_key,mail
from . import auth_blueprint
from flask_wtf import FlaskForm
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email, ValidationError,EqualTo
import bcrypt,subprocess,sys


class ResetRequestForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(), Email()])
    submit = SubmitField("Reset Password",validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField("Submit",validators=[DataRequired()])

class User:
    def __init__(self, id):
        self.id = id

    def get_token(self):
        print(self.id)
        serial = Serializer(secret_key, expires_in=300)
        token=serial.dumps({'user_id': self.id}).decode('utf-8')
        return token

    
    @staticmethod
    def verify_token(token):
        serial = Serializer(secret_key)
        try:
            user_id = serial.loads(token)['user_id']
            print('verify_token',user_id)
        except Exception as e:
            print(f"Error verifying token: {e}")
            return None

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            print('id =',user)
            return user
        except Exception as e:
            print(f"Error querying database: {e}")
        finally:
            cursor.close()
            print('cursor')

def send_mail(user,token):
    msg=Message('Password Reset Request',recipients=[user[2]],sender='noreplyemotiondetection68@gmail.com')
    msg.body=f''' To reset your password. Please follow the link below.
    
    {url_for('auth.reset_password',token=token,_external=True)}

    If you didn't send a password reset request. Please ignore this message.
    
    '''
    mail.send(msg)

class RegisterForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField("Register")

    def validate_email(self,field):
        cursor = mysql.connection.cursor()
       # Use COUNT to check if the email already exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE LOWER(email) = LOWER(%s)", (field.data,))
        user_count = cursor.fetchone()[0]

        cursor.close()
        if user_count > 0:
            raise ValidationError('Email Already Taken')

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Login")

def run_emotion_detection():
    '''Function to trigger emotion detection file'''
    subprocess.Popen([sys.executable, 'app/main/emot_face_updated.py'])


@auth_blueprint.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        # store data into database 
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",(name,email,hashed_password))
        mysql.connection.commit()
        cursor.close()

        flash("User registerd successfully!","success")

        return redirect(url_for('auth.login'))

    return render_template('register.html',form=form)

@auth_blueprint.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cursor.fetchone()
        cursor.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('auth.dashboard'))
        else:
            flash("Login failed. Please check your email and password")
            return redirect(url_for('auth.login'))

    return render_template('login.html',form=form)

@auth_blueprint.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where id=%s",(user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template('dashboard.html',user=user)
            
    return redirect(url_for('auth.login'))

@auth_blueprint.route('/run_emotion_detection_script', methods=['POST'])
def run_emotion_detection_script():
    # Run emotion detection script
    run_emotion_detection()
    return redirect(url_for('auth.dashboard'))

@auth_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out successfully.")
    return redirect(url_for('auth.login'))

@auth_blueprint.route('/reset_request',methods=['GET','POST'])
def reset_request():
    form = ResetRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cursor.fetchone()
        id=user[0]
        cursor.close()
        if user:
            token=User(id).get_token()
            send_mail(user,token)
            flash('Reset request sent. Check your email')
            return redirect(url_for('auth.login'))


    return render_template("reset_request.html",title='Reset Request',form=form,legend="Reset Password")

@auth_blueprint.route('/reset_token/<token>',methods=['GET','POST'])
def reset_password(token):
    print('token',token)
    user=User(token).verify_token(token)
    if user is None:
        flash('That is invalid token or already expired. Please try again.')
        return redirect(url_for('auth.reset_request'))
    
    form=ResetPasswordForm()
    print('form1',form)
    if form.validate_on_submit():
        password = form.password.data
        confirm_password = form.confirm_password.data
        if password==confirm_password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

            # update new password into database  
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE users SET password = %s WHERE id = %s",(hashed_password,user[0]))
            mysql.connection.commit()
            cursor.close()

            flash('Password changed! Please login!')
            return redirect(url_for('auth.login'))
            
    return render_template('change_password.html',title="Change Password",form=form)