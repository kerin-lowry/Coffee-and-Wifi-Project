from flask import Flask, render_template, redirect, request
from flask.helpers import url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.wrappers import request
from wtforms import StringField, SubmitField
from wtforms import validators
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

coffee_options = ["☕️", "☕️☕️", "☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️☕️☕️"]
wifi_options = ["〰️","💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"]
power_options = ["〰️","🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"]

class CafeForm(FlaskForm):
    cafe = StringField(label="Cafe Name", validators=[DataRequired()])
    location = StringField(label="Cafe Location on Google Maps (URL)", validators=[DataRequired(), validators.URL()])
    opening = StringField(label="Opening Time (e.g. 8AM)", validators=[DataRequired()])
    closing = StringField(label="Closing Time (e.g. 5:30PM)", validators=[DataRequired()])
    coffee = SelectField(label="Coffee", choices=[(coffee, coffee) for coffee in coffee_options], validators=[DataRequired()])
    wifi = SelectField(label="Wifi", choices=[(wifi, wifi) for wifi in wifi_options], validators=[DataRequired()])
    power = SelectField(label="Power", choices=[(power, power) for power in power_options], validators=[DataRequired()])
    submit = SubmitField("Submit")


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", "a", newline='', encoding="utf8") as csv_file:
            csv_file.write(f"\n{form.cafe.data}, {form.location.data}, {form.opening.data}, {form.closing.data}, {form.coffee.data}, {form.wifi.data}, {form.power.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open("cafe-data.csv", newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        length = len(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows, length=length)


if __name__ == '__main__':
    app.run(debug=True)
