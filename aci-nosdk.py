#!/usr/bin/env python
###################################################################################
#                           Written by Wei, Hang                                  #
#                          weihang_hank@gmail.com                                 #
###################################################################################
"""
ACI programmability without Cobra
"""

import requests

requests.packages.urllib3.disable_warnings()
url = "http://10.75.53.131"
payload = '''
{
   "aaaUser": {
       "attributes": {
           "name": "hangwe",
           "pwd": "cisco.123"
       }
   }
}
'''
headers = {
    'Content-Type': 'text/plain'
}
response = requests.request("POST", url + "/api/aaaLogin.json", headers=headers, data=payload).json()
token = response["imdata"][0]["aaaLogin"]["attributes"]["token"]
payload = '''
{
    "fvTenant": {
        "attributes": {
            "dn": "uni/tn-hangwe-rogue2",
            "name": "hangwe-rogue2",
            "rn": "tn-hangwe-rogue2",
            "status": "created"
        },
        "children": [
            {
                "fvCtx": {
                    "attributes": {
                        "dn": "uni/tn-hangwe-rogue2/ctx-hangwe-rogue2-ctx",
                        "name": "hangwe-rogue2-ctx",
                        "rn": "ctx-hangwe-rogue2-ctx",
                        "status": "created"
                    },
                    "children": []
                }
            }
        ]
    }
}
'''
headers = {
    'Content-Type': 'application/json',
    'Cookie': 'APIC-cookie=' + token
}
requests.request("POST", url + '/api/node/mo/uni/tn-hangwe-rogue2.json', headers=headers, data=payload)
response = requests.request("GET", url + '/api/node/class/fvTenant.json', headers=headers, data={})
print(response.text.encode('utf8'))
