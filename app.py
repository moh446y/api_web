import requests
import hashlib
import base64
from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def index():
	number = request.args.get('n')
	password = request.args.get('p')
	email = request.args.get('e')
	
	if "011" in number:
		num = number[+1:]
	else:
		num = number

	code = email + ":" + password
	ccode = code.encode("ascii")
	base64_bytes = base64.b64encode(ccode)
	auth = base64_bytes.decode("ascii")
	xauth = "Basic " + auth
	
	urllog = "https://mab.etisalat.com.eg:11003/Saytar/rest/authentication/loginWithPlan"

	headerslog = {
		"applicationVersion": "2",
		"applicationName": "MAB",
		"Accept": "text/xml",
		"Authorization": xauth,
		"APP-BuildNumber": "964",
		"APP-Version": "27.0.0",
		"OS-Type": "Android",
		"OS-Version": "12",
		"APP-STORE": "GOOGLE",
		"Is-Corporate": "false",
		"Content-Type": "text/xml; charset=UTF-8",
		"Content-Length": "1375",
		"Host": "mab.etisalat.com.eg:11003",
		"Connection": "Keep-Alive",
		"Accept-Encoding": "gzip",
		"User-Agent": "okhttp/5.0.0-alpha.11",
		"ADRUM_1": "isMobile:true",
		"ADRUM": "isAjax:true"
	}
	
	datalog = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><loginRequest><deviceId></deviceId><firstLoginAttempt>true</firstLoginAttempt><modelType></modelType><osVersion></osVersion><platform>Android</platform><udid></udid></loginRequest>"
	
	log = requests.post(urllog, headers=headerslog, data=datalog)

	if "true" in log.text:
		st = log.headers["Set-Cookie"]
		ck = st.split(";")[0]
		br = log.headers["auth"]

		url = "https://mab.etisalat.com.eg:11003/Saytar/rest/zero11/offersV3?req=<dialAndLanguageRequest><subscriberNumber>%s</subscriberNumber><language>1</language></dialAndLanguageRequest>" % (num)

		headers = {
			'applicationVersion': "2",
			'Content-Type': "text/xml",
			'applicationName': "MAB",
			'Accept': "text/xml",
			'Language': "ar",
			'APP-BuildNumber': "10459",
			'APP-Version': "29.9.0",
			'OS-Type': "Android",
			'OS-Version': "11",
			'APP-STORE': "GOOGLE",
			'auth': "Bearer " + br,
			'Host': "mab.etisalat.com.eg:11003",
			'Is-Corporate': "false",
			'Connection': "Keep-Alive",
			'Accept-Encoding': "gzip",
			'User-Agent': "okhttp/5.0.0-alpha.11",
			'Cookie': ck
		}

		response = requests.get(url, headers=headers)

		if response.status_code == 200:
			root = ET.fromstring(response.text)
			offer_id = None
			for category in root.findall('.//mabCategory'):
				for product in category.findall('.//mabProduct'):
					for parameter in product.findall('.//fulfilmentParameter'):
						if parameter.find('name').text == 'Offer_ID':
							offer_id = parameter.find('value').text
							break
					if offer_id:
						break
				if offer_id:
					break
		else:
			return jsonify({"result": "Try again tomorrow"})
	else:
		return jsonify({"result":"The number or password is incorrect"})
		

	if "true" in log.text:
		st = log.headers["Set-Cookie"]
		ck = st.split(";")[0]
		br = log.headers["auth"]

		urlsub = "https://mab.etisalat.com.eg:11003/Saytar/rest/zero11/submitOrder"

		headerssub = {
			"applicationVersion": "2",
			"applicationName": "MAB",
			"Accept": "text/xml",
			"Cookie": ck,
			"Language": "ar",
			"APP-BuildNumber": "964",
			"APP-Version": "27.0.0",
			"OS-Type": "Android",
			"OS-Version": "12",
			"APP-STORE": "GOOGLE",
			"auth": "Bearer " + br,
			"Is-Corporate": "false",
			"Content-Type": "text/xml; charset=UTF-8",
			"Content-Length": "1375",
			"Host": "mab.etisalat.com.eg:11003",
			"Connection": "Keep-Alive",
			"User-Agent": "okhttp/5.0.0-alpha.11"
		}

		datasub = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><submitOrderRequest><mabOperation></mabOperation><msisdn>%s</msisdn><operation>ACTIVATE</operation><parameters><parameter><name>GIFT_FULLFILMENT_PARAMETERS</name><value>Offer_ID:%s;ACTIVATE:True;isRTIM:Y</value></parameter></parameters><productName>FAN_ZONE_HOURLY_BUNDLE</productName></submitOrderRequest>" % (num, offer_id)

		subs = requests.post(urlsub, headers=headerssub, data=datasub).text

		if "true" in subs:
			return jsonify({'result': 'Two hours'})
		else:
			return jsonify({"result":"Check Your Data"})
	else:
		return jsonify({"result":"Check Your Input"})
@app.route('/orange')
def Orange():
	none = "5"
	number = request.args.get('n')
	password = request.args.get('p')
	
	with requests.Session() as req:
		if none=="5":
			urlog = "https://services.orange.eg/GetToken.svc/GenerateToken"
			headerlog = {
			   
		                "Content-Type": "application/json; charset=UTF-8",
		                "User-Agent":"okhttp/3.14.9"
		            
			}
			datalog = '{"channel":{"ChannelName":"MobinilAndMe","Password":"ig3yh*mk5l42@oj7QAR8yF"}}'
			
			ctv = req.post(urlog, headers=headerlog, data=datalog).json()["GenerateTokenResult"]["Token"]
			
			htv = hashlib.sha256((ctv + ',{.c][o^uecnlkijh*.iomv:QzCFRcd;drof/zx}w;ls.e85T^#ASwa?=(lk').encode()).hexdigest().upper()
			
			
			url = "https://services.orange.eg/SignIn.svc/SignInUser"
			
			headers = {
			    "_ctv": ctv,
			    "_htv": htv,
			    "Content-Type": "application/json; charset=UTF-8",
			    "Content-Length": "168",
			    "Host": "services.orange.eg",
			    "Connection": "Keep-Alive",
			    "Accept-Encoding": "gzip",
			    "User-Agent": "okhttp/3.14.9"
			}
			
			data = '{"appVersion": "6.0.1","channel":{"ChannelName":"MobinilAndMe", "Password": "ig3yh*mk5l42@oj7QAR8yF"},"dialNumber":"' + number + '","isAndroid": "true","password":"' + password + '"}'
			
			slow = req.post(url, headers=headers, data=data)
			userid = slow.json()["SignInUserResult"]["UserData"]["UserID"]
			
			urlx = "https://services.orange.eg/APIs/Promotions/api/CAF/Redeem"
			
			headersx = {
			    "_ctv": ctv,
			    "_htv": htv,
			    'UserId': userid,
			    "Content-Type": "application/json; charset=UTF-8",
			    "Host": "services.orange.eg",
			    "Connection": "Keep-Alive",
			    "User-Agent": "okhttp/3.12.9"
			}
			
			json_data = {
			    "Language": "ar",
			    "OSVersion": "Android7.0",
			    "PromoCode": "رمضان كريم",
			    "dial": number,
			    "password": password,
			    "Channelname": "MobinilAndMe",
			    "ChannelPassword": "ig3yh*mk5l42@oj7QAR8yF"
			}
			MEGA = req.post(urlx, headers=headersx, json=json_data).text
			
			if "Success" in MEGA:
			    return jsonify({"result":"Success"})
			
			if "انت استخدمت البرومو كود النهاردة" in MEGA:
			    return jsonify({"result":"Try again"})

app.run(host='0.0.0.0', port=5000)