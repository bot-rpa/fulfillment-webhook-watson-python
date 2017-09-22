# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import string

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
    result = req.get("result")
    parameters = result.get("parameters")
    duration = parameters.get("duration") 
    #duration = string.replace(duration, "2018", "2017")
    servicetype = parameters.get("servicetype") 
    data = ""
    res = makeWebhookResult(duration,servicetype)
    return res

def makeWebhookResult(duration,servicetype):
    if (duration == "2017-08-01/2017-08-31"):
        usage = "100"
    elif (duration == "2017-07-01/2017-07-31"):
        usage = "110"
    elif (duration == "2017-06-01/2017-06-30"):
        usage = "120"
    elif (duration == "2017-05-01/2017-05-31"):
        usage = "150"
    elif (duration == "2017-04-01/2017-04-30"):
        usage = "145"
    elif (duration == "2017-03-01/2017-03-31"):
        usage = "169"
    elif (duration == "2017-02-01/2017-02-28"):
        usage = "140"
    elif (duration == "2017-01-01/2017-01-31"):
        usage = "130"
    elif (duration == "2016-01-01/2016-12-31"):
        usage = "1350"
    elif (duration == "2017-09-18/2017-09-24"):
        usage = "30"
    elif (duration == "2017-09-11/2017-09-17"):
        usage = "20"
    else:
        usage = "200"
    
    output_speech = "Your " + servicetype + " usage for the duration " + duration + " is " + usage + " units which costs 50 pounds. Any thing else I can do for you."
    return {
        "speech": output_speech,
        "displayText": output_speech,
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
