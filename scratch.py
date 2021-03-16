def getGeoJsonFromSelectedLayer():

import requests

plug = qgis.utils.plugins['fulcrum_sync']

url = "https://api.fulcrumapp.com/api/v2/query"

tableSelector = f"SELECT * FROM \"THIS ONE: Invasive Species Form\""
querystring = {"q": tableSelector, "format": "geojson", "headers": "false",
                "metadata": "false", "arrays": "false", "page": "1", "per_page": "20000"}

headers = {
    "Accept": "application/json",
    "X-ApiToken": '86525570d371b23fb3085277dba6e2f8a2fc0fd68256d14007329604948175e2656a7bb35bc81db1'
}

response = requests.request(
    "GET", url, headers=headers, params=querystring)

