"""For getting user details, use to test API Key"""

import requests
import json

url = "https://api.fulcrumapp.com/api/v2/users.json"

querystring = {"page":"1","per_page":"20000"}

headers = {
    "Accept": "application/json",
    "X-ApiToken": "2b6d6363d014e69d8eff078c093c0a06df71f68a45cd88123780386de4eced40e7a317c8ddc56e24"
}

response = requests.request("GET", url, headers=headers, params=querystring)

responseDict = json.loads(response.text)
userName = (responseDict["user"]["first_name"] + " " + responseDict["user"]["last_name"] )

return userName