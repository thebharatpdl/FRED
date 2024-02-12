from flask import render_template, url_for,redirect,request,jsonify,session
from . import main_blueprint
from app import mysql
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
import subprocess,sys
from app.face_registration import FaceRecognize 
import os


class NameForm:
    def __init__(self):
        self.name = ""

class FaceRegister(FlaskForm):
    face_name = StringField("Name",validators=[DataRequired()])
    submit = SubmitField("Register Face")

def run_face_registration():
    '''Function to trigger face registration file'''
    subprocess.Popen([sys.executable, 'app/main/face_registration.py'])

def pass_name():
    return request.args.get('name', '')

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/chart')
def chart():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where id=%s",(user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template('chart.html',user=user)
    return render_template('chart.html')

# Endpoint to get list of CSV files
@main_blueprint.route('/csv-files')
def csv_files():
    csv_folder = 'app/static/captured_emotions_data'  # Path to the folder containing CSV files
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
    return jsonify(csv_files)

@main_blueprint.route('/face_register', methods=['GET', 'POST'])
def face_register():
    form = NameForm()

    if request.method == 'POST' and 'name' in request.form:
        name = request.form['name']
        object = FaceRecognize()
        object.face_register(name)

    return render_template('dashboard.html')

# @main_blueprint.route('/face_register',methods=['GET','POST'])
# def face_register():
#     form = FaceRegister()
#     if form.validate_on_submit():
#         name = form.face_name.data
#         return redirect(url_for('run_face_registration_script'))
#     return render_template('face_register.html')

# @main_blueprint.route('/run_face_registration_script', methods=['POST'])
# def run_face_registration_script():
#     # Run your Python script
#     run_face_registration()
#     return render_template('face_register.html')

