from flask import render_template, request, redirect
from app import app
from app.utils import format_price
from enum import Enum

import requests
import json
import datetime

# get the API Key from the config file
apiKey = app.config["API_KEY"]

# http://www.davidadamojr.com/handling-cors-requests-in-flask-restful-apis/
@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
	return response



# ========== UPDATE BELOW THIS LINE ========== #



# This route loads the home screen.  Get all data necessary and pass it to the view.
@app.route('/')
@app.route('/index')
def index():
	accountsURL = "http://api.reimaginebanking.com/accounts?key={}".format(apiKey)
	accountsResponse = requests.get(accountsURL)
	# initialize transfers array
	transfersNoCards = []
	# check if accounts successfully retrieved
	if accountsResponse.status_code == 200:
		accounts = json.loads(accountsResponse.text)
		accountsNoCards = []
		for account in accounts:
			if account["type"] !=  "Credit Card":
				accountsNoCards.append(account)
				# only show payee transfers
				transfersURL = "http://api.reimaginebanking.com/accounts/{}/transfers/?type=payee&key={}".format(account["_id"], apiKey)
				transfersResponse = requests.get(transfersURL)
				transfers = json.loads(transfersResponse.text)
				for transfer in transfers:
					# get payer account
					payerURL = "http://api.reimaginebanking.com/accounts/{}?key={}".format(transfer["payer_id"], apiKey)
					payerResponse = requests.get(payerURL)
					payer = json.loads(payerResponse.text)
					# update transfer's payee_id and payer_id
					transfer["payee_id"] = account["nickname"]
					transfer["payer_id"] = payer["nickname"]
					transfersNoCards.append(transfer)

		return render_template("home.html", accounts=accountsNoCards, transfers=transfersNoCards, format_price=format_price)
	else:
		return render_template("notfound.html")

# This route should get the fields from the form and create a transfer POST request
@app.route('/transfer', methods=['POST'])
def postTransfer():
	fromAccount = request.form["fromAccount"]
	if fromAccount == "":
		return redirect("/index", code=302)
	toAccount = request.form["toAccount"]
	if toAccount == "":
		return redirect("/index", code=302)

	try:
		amount = float(request.form["amount"])
	except ValueError:
		amount = ""

	description = request.form["description"]

	medium = "balance"
	dateObject = datetime.date.today()
	# formatting date
	dateString = dateObject.strftime('%Y-%m-%d')

	body = {
	    'medium': medium,
		'payee_id': toAccount,
		'amount': amount,
		'transaction_date': dateString,
		'description': description
	}
	print body
	transferUrl = "http://api.reimaginebanking.com/accounts/{}/transfers?key={}".format(fromAccount, apiKey)

	response = requests.post(
		transferUrl,
		data=json.dumps(body),
		headers={'content-type':'application/json'})

	print response.text

	return redirect("/index", code=302)
