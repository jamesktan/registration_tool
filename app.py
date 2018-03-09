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

max_users = 61

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


		number_adults = form.number_of_adults.data
		names_adults = form.names_of_adults.data

		number_jy = form.number_of_jy.data
		names_jy = form.names_of_jy.data

		number_toddler = form.number_of_children.data
		names_toddler = form.names_of_children.data

		values_list.append(number_adults)
		values_list.append(names_adults)
		values_list.append(number_jy)
		values_list.append(names_jy)
		values_list.append(number_toddler)
		values_list.append(names_toddler)

		if len(wks.get_all_values()) > max_users :
			values_list.append("waitlist")
		else:
			values_list.append("registered")

		wks.insert_rows(row=1, number=1, values=values_list)


		# Calculate Cost
		total = (148 * int(number_adults)) + (78 * int(number_jy)) + (48*int(number_toddler)) 
		total_cents = total * 100

		if len(wks.get_all_values()) > max_users :
			return redirect(url_for('waitlist'))
		else:
			return redirect(url_for('step2',total=total_cents, token=token))

	return render_template("step1.html", form=form)

@app.route("/step2/<total>/<token>", methods=['GET','POST'])
def step2(total,token):
	if request.method == 'GET':
		return render_template("step2.html", total=total, token=token)
	if request.method == 'POST':

		user_token = request.form.get('user_token')
		user_total = int(request.form.get('user_total'))

		token = request.form['stripeToken'] # Using Flask

		# # Charge the user's card:
		charge = stripe.Charge.create(
			amount=user_total,
			currency="usd",
			description=user_token + " Charged",
			source=token,
		)

		# Update the spreadsheet with the charge token and amount
		cell = wks.find(user_token)[0]
		row = cell.row
		cell_amount_id = "R" + str(row)
		cell_token_id = "S" + str(row)
		wks.update_cell(cell_amount_id,user_total)
		print(charge.id)
		wks.update_cell(cell_token_id,charge.id)


		return redirect(url_for('success'))


@app.route("/success",methods=['GET'])
def success():
	return render_template("success.html")

@app.route("/waitlist", methods=['GET'])
def waitlist():
	return render_template("waitlist.html")

if __name__ == '__main__' :

	app.run(debug=True)