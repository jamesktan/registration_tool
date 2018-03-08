# https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
# https://github.com/nithinmurali/pygsheets

from flask import Flask, abort, request, jsonify, g, url_for, render_template, redirect, send_from_directory, Response, request
from forms import RegistrationForm
import requests
import stripe
import pygsheets
import datetime
import uuid

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
	if request.method == 'POST' and form.validate_on_submit():
		print("post")

		values_list = []
		time = datetime.datetime.now()
		values_list.append(str(time))

		token = uuid.uuid1()
		values_list.append(str(token))

		name = form.name.data
		if name != None: values_list.append(name)
		email = form.email.data
		if email != None: values_list.append(email)
		phone = form.phone.data
		if phone != None: values_list.append(phone)
		community = form.community.data
		if community != None: values_list.append(community)
		days = ",".join(form.days.data)
		values_list.append(days)
		dietary = ",".join(form.dietary.data)
		values_list.append(dietary)
		dietary_other = form.dietary_other.data
		values_list.append(dietary_other)
		food_allergies = form.food_allergies.data
		values_list.append(food_allergies)
		number_family = form.number_of_family.data
		values_list.append(number_family)
		family_details = form.family_details.data
		values_list.append(family_details)

		wks.insert_rows(row=1, number=1, values=values_list)

		return redirect(url_for('step2',number_family=number_family, token=token))
	return render_template("step1.html", form=form)

@app.route("/step2/<number_family>/<token>", methods=['GET','POST'])
def step2(number_family,token):
	if request.method == 'GET':
		count = int(number_family)
		return render_template("step2.html", count=count, token=token)
	if request.method == 'POST':

		user_token = request.form.get('user_token')
		user_count = int(request.form.get('user_count'))

		token = request.form['stripeToken'] # Using Flask

		# # Charge the user's card:
		charge = stripe.Charge.create(
			amount=167*100*user_count,
			currency="usd",
			description=user_token + "Charged",
			source=token,
		)

		# Updarte the spreadsheet with the charge token and amount
		amount = 167.0*100*user_count

		cell = wks.find(user_token)[0]
		row = cell.row
		cell_amount_id = "M" + str(row)
		cell_token_id = "N" + str(row)
		# wks.update_cell(cell_amount_id,amount)
		# print(charge)
		# wks.update_cell(cell_token_id,charge)


		return redirect(url_for('success'))


@app.route("/success",methods=['GET'])
def success():

	return render_template("success.html")


if __name__ == '__main__' :

	app.run(debug=True,host='0.0.0.0')