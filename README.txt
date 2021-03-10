TODO List:

Errors to Handle:

Error when doing TEST API whne no API key specified
2021-03-10T12:20:02     WARNING    Traceback (most recent call last):
              File "C:/Users/staff/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\fulcrum_sync\fulcrum_sync.py", line 311, in 
              self.dlg.apiButton.clicked.connect(lambda: self.testApiKey())
              File "C:/Users/staff/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\fulcrum_sync\fulcrum_sync.py", line 275, in testApiKey
              responseDict = json.loads(response.text)
              File "C:\OSGEO4~1\apps\Python37\lib\json\__init__.py", line 348, in loads
              return _default_decoder.decode(s)
              File "C:\OSGEO4~1\apps\Python37\lib\json\decoder.py", line 337, in decode
              obj, end = self.raw_decode(s, idx=_w(s, 0).end())
              File "C:\OSGEO4~1\apps\Python37\lib\json\decoder.py", line 355, in raw_decode
              raise JSONDecodeError("Expecting value", s, err.value) from None
             json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
             


Error when clicking Get Apps List:
2021-03-10T13:42:40     WARNING    Traceback (most recent call last):
              File "C:/Users/staff/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\fulcrum_sync\fulcrum_sync.py", line 336, in 
              self.dlg.getAppsButton.clicked.connect(lambda: self.getAppsList())
              File "C:/Users/staff/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\fulcrum_sync\fulcrum_sync.py", line 252, in getAppsList
              jsonResponse = response.json()
              File "C:\OSGEO4~1\apps\Python37\lib\site-packages\requests\models.py", line 898, in json
              return complexjson.loads(self.text, **kwargs)
              File "C:\OSGEO4~1\apps\Python37\lib\site-packages\simplejson\__init__.py", line 518, in loads
              return _default_decoder.decode(s)
              File "C:\OSGEO4~1\apps\Python37\lib\site-packages\simplejson\decoder.py", line 370, in decode
              obj, end = self.raw_decode(s)
              File "C:\OSGEO4~1\apps\Python37\lib\site-packages\simplejson\decoder.py", line 400, in raw_decode
              return self.scan_once(s, idx=_w(s, idx).end())
             simplejson.errors.JSONDecodeError: Expecting value: line 1 column 1 (char 0)


Not loading API Key or any message on first load

