from flask import Flask
from flask_mysqldb import MySQL
from flask_mail import Mail

secret_key = "sskz pzzh znjo tyes"

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'FYP'
app.config['MYSQL_UNIX_SOCKET'] = '/opt/lampp/var/mysql/mysql.sock'  

# Initialize MySQL
mysql = MySQL(app)

# Mail confuguration
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='emotiondetection68@gmail.com'
app.config['MAIL_PASSWORD']='bsor fmez wfws fmmn'

mail=Mail(app)

from app.auth import auth_blueprint
from app.main.routes import main_blueprint


app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(main_blueprint)
