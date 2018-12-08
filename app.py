import json
import requests
from flask import (Flask, render_template, redirect, 
                    url_for, request, make_response, jsonify)

app = Flask(__name__)

def get_submit_data():
    try:
        data = json.loads(request.cookies.get('character'))
    except TypeError:
        data = {}
    return data

def get_hs_cookie():
    try:
        hs_cookie = request.cookies.get('hubspotutk')
    except TypeError:
        hs_cookie = ""
    return  hs_cookie

def format_post_data(data, hs_cookie):
    # form field values
    firstname = data.get('firstname', '')
    lastname = data.get('lastname', '')
    email = data.get('email', '')
    position = data.get('applying_for_position', '')
    description = data.get('role_interest_description', '')

    values_dict = {
        "firstname" : firstname,
        "lastname" : lastname,
        "email" : email,
        "position" : position,
        "description" : description
    }
    
    # form variables
    portalId = 5222232
    formGUID = "ccc375a5-c81c-457d-a5ea-05aadf92bfbe"
    
    # tracking code variables
    hutk = hs_cookie
    ipAddress = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    # page variables
    pageTitle = "Advocate Form"
    pageUrl = request.path

    strError = "No Error"

    post_data = post_to_hubspot_formsAPI(portalId, formGUID, values_dict, hutk, ipAddress, pageTitle, pageUrl, strError)
    var_list = [portalId, formGUID, values_dict, hutk, ipAddress, pageTitle, pageUrl, strError, post_data ]
    return var_list


def post_to_hubspot_formsAPI(portalId, formGUID, values_dict, hutk, ipAddress, pageTitle, pageUrl, strMessage):
    api_key = get_api_key()
    endPointUrl = "https://forms.hubspot.com/uploads/form/v2/{}/{}".format(portalId, formGUID)
    hsContext = {
        "hutk" : hutk,
        "ipAddress" : ipAddress,
        "pageUrl" : pageUrl,
        "pageName" : pageTitle
    }

    hsContextJSON = json.dumps(hsContext)

    postData = ""

    for key, value in values_dict.items():
        postData += key + "=" + value + "&"

    postData += "hs_context=" + hsContextJSON

    return postData

def get_api_key():
    api_key = "242d0749-2269-4dbb-a27d-f4024de96dab"
    return api_key

@app.route('/')
def index():
    data = get_submit_data()
    hs_cookie = get_hs_cookie()
    return render_template('index.html', info=data, hs_cookie=hs_cookie)

@app.route('/submit', methods=['POST'])
def submit():
    response = make_response(redirect(url_for('info')))
    data = get_submit_data()
    hs_cookie = get_hs_cookie()
    data.update(dict(request.form.items()))
    response.set_cookie('character', json.dumps(data))
    format_post_data(data, hs_cookie)
    return response

@app.route('/info')
def info():
    info = get_submit_data()
    hs_cookie = get_hs_cookie()
    data = format_post_data(info, hs_cookie)
    return render_template('info.html', info=info, hs_cookie=hs_cookie, data=data)

app.run(debug=True, port=8000, host="0.0.0.0")