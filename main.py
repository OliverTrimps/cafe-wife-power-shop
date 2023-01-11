from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, URLField, SelectField, FileField
from wtforms.validators import DataRequired, URL
import csv
from flask_bootstrap import Bootstrap
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'static/images'
Bootstrap(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
date = datetime.now()


class ShopForm(FlaskForm):
    shop_name = StringField('Shop Name', validators=[DataRequired()])
    location = URLField('Location', validators=[DataRequired(), URL(message='Enter a valid url')])
    open_time = SelectField('Open', validators=[DataRequired()], choices=['', '7:00AM', '8:00AM', '9:00AM', '10:00AM', '11:00AM', 'Unspecified'])
    close_time = SelectField('Close', validators=[DataRequired()], choices=['', '7:00PM', '8:00PM', '9:00PM', '10:00PM', 'Unspecified'])
    wifi = SelectField('Wifi', validators=[DataRequired()], choices=['', '✅', '❎'])
    power_sockets = SelectField('Power Sockets', validators=[DataRequired()], choices=['', '✅', '❎'])
    image = FileField(label="Upload Image", validators=[DataRequired()])
    submit = SubmitField('Done')


@app.route("/")
def home():
    year = date.year
    with open('shop-data.csv', newline='', encoding='utf8') as data:
        file = csv.reader(data, delimiter=',')
        list_of_row = []
        for row in file:
            list_of_row.append(row)
        # print(list_of_row[0][0][0:5])
    return render_template('index.html', cafe=list_of_row, year=year)


@app.route("/add_cafe", methods=['POST', 'GET'])
def add_cafe():
    form = ShopForm()
    if form.validate_on_submit():
        shop = form.shop_name.data
        location = form.location.data
        opening = form.open_time.data
        closing = form.close_time.data
        wifi = form.wifi.data
        power = form.power_sockets.data

        # if wifi == '...' or power == '...':
        #     flash("Select a valid option for wifi and power!")

        with open('shop-data.csv', 'a', encoding='utf8') as data:
            data.write(f"\n{shop.title()},{location},{opening},{closing},{wifi},{power}")
        with open('shop-data.csv', newline='', encoding='utf8') as data:
            data_file = csv.reader(data, delimiter=',')
            list_row = []
            for line in data_file:
                list_row.append(line)
                pic = form.image.data
                name = pic.filename
                if line[0] == shop.title():
                    new_name = name.replace(pic.filename, f'{line[0][0:5]}.jpg')
                    pic.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                          secure_filename(new_name)))
        flash("Successful!")
        return redirect(url_for('add_cafe'))
    return render_template('cafes.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
