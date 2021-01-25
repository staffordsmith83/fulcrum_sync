import requests

API_TOKEN = "2b6d6363d014e69d8eff078c093c0a06df71f68a45cd88123780386de4eced40e7a317c8ddc56e24"

def getAppsList(API_TOKEN):

    url = "https://api.fulcrumapp.com/api/v2/forms.json"

    querystring = {"schema":"true","page":"1","per_page":"20000"}

    headers = {
        "Accept": "application/json",
        "X-ApiToken": API_TOKEN
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    jsonResponse = response.json()

    appsList = []
    for form in jsonResponse['forms']:
        appsList.append(form['name'])

    return(appsList)


if __name__ == "__main__":
    print(getAppsList("2b6d6363d014e69d8eff078c093c0a06df71f68a45cd88123780386de4eced40e7a317c8ddc56e24"))
