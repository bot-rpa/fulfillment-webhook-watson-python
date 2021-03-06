
from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "welcome":
    #if req.get("result").get("action") == "input.usage":
        result = req.get("result")
        parameters = result.get("parameters")
        duration = parameters.get("duration") 
        duration = duration.replace("2018", "2017")
        servicetype = parameters.get("servicetype") 
        data = ""
        res = makeWebhookResult(duration,servicetype)
    else :
        result = req.get("result")
        parameters = result.get("parameters")
        userid = parameters.get("userid")
        password = parameters.get("password")
        res = makeWebhookResult2(userid, password)
    return res

def makeWebhookResult3():
        output_speech = "Please enter userid121"
        return {
            "speech": output_speech,
            "displayText": output_speech,
            "source": "apiai-weather-webhook-sample",
            #"speech":"This is a simple response with suggestion chips",
            "data": {
                "google":
                {
                    "richResponse":
                    {
                        "items":
                        [
                            {
                                "simpleResponse":
                                {
                                    "textToSpeech":"This is a simple response for with suggestion chips"
                                }
                            }
                        ],                                
                        "suggestions":
                        [
                            {
                                "title":"Please enter your userid"
                            }
                        ]
                    }
                }
            }
        }
    
def makeWebhookResult2(userid, password):
    if (userid == "9" and password == "password"):     
        username = "Arvind"
        output_speech = " Welcome " + username + ". \n How may I help you."
        return {
            "speech": output_speech,
            "displayText": output_speech,
            "source": "apiai-weather-webhook-sample",
            #"speech":"This is a simple response with suggestion chips",
            "data": {
                "google":
                {
                    "richResponse":
                    {
                        "items":
                        [
                            {
                                "simpleResponse":
                                {
                                    "textToSpeech": output_speech
                                }
                            }
                        ],
                        "suggestions":
                        [
                            {
                                "title":"Usage"
                            },
                            {
                                "title":"Complaint"
                            },                           
                            {
                                "title":"Notification"
                            },
                            {
                                "title":"Offer"
                            },
                            {
                                "title":"Outage Details"
                            }
                        ]
                    }
                }
            }
        }
    elif (userid == "8" and password == "password"):     
        username = "Sree" 
        output_speech = "You have entered correct details . Welcome " + username
        return {
            "speech": output_speech,
            "displayText": output_speech,
            "source": "apiai-weather-webhook-sample",
            "data": {
                "google":
                {
                    "richResponse":
                    {
                        "items":
                        [
                            {
                                "simpleResponse":
                                {
                                    "textToSpeech": output_speech
                                }
                            }
                        ],
                        "suggestions":
                        [
                            {
                                "title":"Usage"
                            },
                            {
                                "title":"Complaint"
                            },                           
                            {
                                "title":"Notification"
                            },
                            {
                                "title":"Offer"
                            },
                            {
                                "title":"Outage Details"
                            }
                        ]
                    }
                }
            }
        }
    else:
        output_speech = "You haven't entered correct details. Please re-enter the credentials"
        return {
            "speech": output_speech,
            "displayText": output_speech,
            "source": "apiai-weather-webhook-sample",
            "followupEvent": {
                    "name": "event-incorrectdetails",
                    "data": {
                        "welcome":"welcome"
                    }
            }
        }


def makeWebhookResult(duration,servicetype):
    if (duration == "2017-08-01/2017-08-31"):
        usage = "100"
    elif (duration == "2017-09-01/2017-09-30"):
        usage = "245"
    elif (duration == "2017-07-01/2017-07-31"):
        usage = "110"
    elif (duration == "2017-06-01/2017-06-30"):
        usage = "120"
    elif (duration == "2018-05-01/2018-05-31"):
        usage = "150"
    elif (duration == "2018-04-01/2018-04-30"):
        usage = "145"
    elif (duration == "2018-03-01/2018-03-31"):
        usage = "169"
    elif (duration == "2018-02-01/2018-02-28"):
        usage = "140"
    elif (duration == "2018-01-01/2018-01-31"):
        usage = "130"
    elif (duration == "2018-01-01/2018-12-31"):
        usage = "1350"
    elif (duration == "2017-09-18/2017-09-24"):
        usage = "30"
    elif (duration == "2018-06-18/2018-06-24"):
        usage = "20"
    else:
        usage = "210"
    
    output_speech = "Your " + servicetype + " usage for the duration " + duration + " is " + usage + " units which costs " + str(float(usage) * 0.45) + " pounds. Any thing else I can do for you."
    return {
        "speech": output_speech,
        "displayText": output_speech,
        "source": "apiai-weather-webhook-sample",
        "data": {
            "google":
            {
                "richResponse":
                {
                    "items":
                    [
                        {
                            "simpleResponse":
                            {
                                "textToSpeech":output_speech
                            }
                        }
                    ],
                    "suggestions":
                    [
                        {
                            "title":"Usage"
                        },
                        {
                           "title":"Complaint" 
                        },
                        {
                            "title":"Notification"
                        },
                        {
                            "title":"Offer"
                        },
                        {
                            "title":"End Call"
                        }
                    ]
                }
            }
        }
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
