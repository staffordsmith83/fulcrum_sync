import requests

url = "https://api.fulcrumapp.com/api/v2/query"

querystring = {"q":"SELECT * FROM \"Winyama Wetland Survey\"","format":"geojson","headers":"false","metadata":"false","arrays":"false","page":"1","per_page":"20000"}

headers = {
    "Accept": "application/json",
    "X-ApiToken": "2b6d6363d014e69d8eff078c093c0a06df71f68a45cd88123780386de4eced40e7a317c8ddc56e24"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)