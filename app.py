# https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
# https://github.com/nithinmurali/pygsheets

from flask import Flask, abort, request, jsonify, g, url_for, render_template, redirect, send_from_directory, Response, request
from forms import RegistrationForm
import requests
import stripe
import pygsheets

app = Flask(__name__)
app.secret_key = "sekret"


stripe.api_key = "sk_test_4RfmxtTrHP0R0mebD2aCtlmj"
gc = pygsheets.authorize(service_file='client_secret.json')
sh = gc.open('Paid Signups')
wks = sh[0]




@app.route("/",methods=['GET', 'POST'])
def main():
	form = RegistrationForm()

	if request.method == 'GET':

		return render_template("index.html", form=form)
	if request.method == 'POST':

		return redirect(url_for('groups'))

	return render_template("index.html", form=form)

@app.route("/step1", methods=['GET', 'POST'])
def step1():
	form = RegistrationForm()
	if request.method == 'GET':
		return render_template("step1.html",form=form)
	if request.method == 'POST':
		# values_list = ["1","2<","3<","4","5"]
		# wks.insert_rows(row=1, number=1, values=values_list)

		return redirect(url_for('step2'))
	return render_template("step1.html", form=form)

@app.route("/step2", methods=['GET','POST'])
def step2():
	if request.method == 'GET':
		return render_template("step2.html")
	if request.method == 'POST':

		# token = request.form['stripeToken'] # Using Flask

		# # Charge the user's card:
		# charge = stripe.Charge.create(
		#   amount=999,
		#   currency="usd",
		#   description="Example charge",
		#   source=token,
		# )

		return redirect(url_for('success'))


@app.route("/success",methods=['GET'])
def success():
	render_template("success.html")


if __name__ == '__main__' :

	app.run(debug=True,host='0.0.0.0')