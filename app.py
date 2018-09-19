import urllib
import json
import os
from flask import flask
from flask import request
from flask import make_response


#   Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook',methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = makeWebhookResult(req)
    res = json.dumps(res, ident=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req):
    if req.get("result").get("action") != "interest":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    name = parameters.get("bank-name")
    bank = {'Federal Bank':'6.7%','Andhra Bank':'6.85%','Bandhan Bank':'7.00%'}
    speech = "The interest rate of" + name + " is " + str(bank[name])
    print("Response:")
    print(speech)
    return {
        "speech" : speech,
        "displayText" : speech,
        "source" : "BankInterestRates"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=True, port=port, host = '0.0.0.0')
