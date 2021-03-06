# -*- coding: utf-8 -*-
#  TODO: Allow user configurable API Key
#  TODO: move apps list population to only happen once Get Apps List 'pushButton' is pressed
#  TODO: deal with possibly unbound geotype variable, line 261
#   TODO: BUGFIX - if plugin is opened a second time, it will load two copies of the selected layer...
#               this is regardless of whether that layer has been connected before. So the load point method is being called twice.
# TODO: when storing or reading apiKey, should the s=QgsSettings variable be a global class variable instead of scoped to the indiv functions?

"""
/***************************************************************************
 FulcrumSync
                                 A QGIS plugin
 Link Fulcrum to QGIS throught the REST API
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-01-21
        git sha              : $Format:%H$
        copyright            : (C) 2021 by NGIS
        email                : stafford.smith@ngis.com.au
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import QgsProject, QgsVectorLayer, QgsJsonUtils, QgsWkbTypes, QgsField, QgsFields, edit, QgsSettings
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.gui import QgsMessageBar
from qgis.utils import iface

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .fulcrum_sync_dialog import FulcrumSyncDialog
import os.path
import requests
import json


class FulcrumSync:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'FulcrumSync_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Fulcrum Sync')

        # Some custom declarations
        self.selectedLayer = ''

        ###########################################################################
        # DEFAULT API KEY HERE - set to empty '' after testing
        ###########################################################################
        # self.API_TOKEN = '86525570d371b23fb3085277dba6e2f8a2fc0fd68256d14007329604948175e2656a7bb35bc81db1'
        self.API_TOKEN = ''

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('FulcrumSync', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/fulcrum_sync/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Fulcrum Sync'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Fulcrum Sync'),
                action)
            self.iface.removeToolBarIcon(action)

    def getSelectedLayer(self):
        self.selectedLayer = self.dlg.listWidget.selectedItems()[0].text()

        # Enable the load points button, now that we have a layer
        self.dlg.loadPointsButton.setEnabled(True)

    def getGeoJsonFromSelectedLayer(self):

        if self.selectedLayer:
            url = "https://api.fulcrumapp.com/api/v2/query"

            tableSelector = f"SELECT * FROM \"{self.selectedLayer}\""
            querystring = {"q": tableSelector, "format": "geojson", "headers": "false",
                           "metadata": "false", "arrays": "false", "page": "1", "per_page": "20000"}

            headers = {
                "Accept": "application/json",
                "X-ApiToken": self.API_TOKEN
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring)

            # For Debugging:
            iface.messageBar().pushMessage(response.text)
            
            self.createLayerFromGeojson(response.text)

        else:
            iface.messageBar().pushMessage("No Layer Selected")

    def createLayerFromGeojson(self, geoj):
        # if there are features in the list
        if len(geoj) > 0:

            # add the layer to the list of layers
            vlayer = QgsVectorLayer(geoj, self.selectedLayer, 'ogr')

            # Now handle any integerList type fields, as some versions of QGIS have a problem with this:
            self.handleIntegerLists(vlayer)
            QgsProject.instance().addMapLayer(vlayer)
            iface.messageBar().pushMessage("Handled Integer List Fields to prevent QGIS errors")

        else:
            iface.messageBar().pushMessage("No features found in the geoJSON")

    
    def handleIntegerLists(self, geoj_layer):
        # QGIS does not import geojson with IntegerList type fields correctly.
        # For now, we will remove these fields, but a better solution is needed.
        # Some users may have integerList fields that are important in their data.

        ###############################
        # TODO: l.deleteAttribute(idx) method fails because our layer is not editable.
        # In the data provider, the uri is actually the raw string object in memory from our code.
        # perhaps we need to write this out to a temporary location.
        # Should this be in a local database maybe?
        # Can the Fulcrum API return a different format than geojson?
        
        l = geoj_layer
        for f in l.fields():
            if f.typeName() == "IntegerList":
                idx= l.fields().indexFromName(f.name())
                l.deleteAttribute(idx)
                iface.messageBar().pushMessage('field deleted: ' + f.name())


    def getAppsList(self):

        url = "https://api.fulcrumapp.com/api/v2/forms.json"
        querystring = {"schema": "true", "page": "1", "per_page": "20000"}
        headers = {
            "Accept": "application/json",
            "X-ApiToken": self.API_TOKEN
        }

        try:
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            jsonResponse = response.json()

            appsList = []
            for form in jsonResponse['forms']:
                appsList.append(form['name'])

            self.dlg.listWidget.clear()
            self.dlg.listWidget.addItems(appsList)

        except:
            self.dlg.apiInput.setPlainText(f'API Key Invalid')

    def registerApiKey(self):
        # First get the value of the API Key QDialog box and store in local variable
        apiKey = self.dlg.apiInput.toPlainText()

        if self.testApiKey(apiKey):
            self.storeApiKey(apiKey)
            self.recallApiKey()

        else:
            iface.messageBar().pushMessage("Could not register API Key")

    def testApiKey(self, apiKey):
        # Setup the request
        url = "https://api.fulcrumapp.com/api/v2/users.json"
        querystring = {"page": "1", "per_page": "20000"}
        headers = {
            "Accept": "application/json",
            "X-ApiToken": apiKey
        }

        try:
            # Make the GET request
            response = requests.request(
                "GET", url, headers=headers, params=querystring)

            responseDict = json.loads(response.text)
            userName = (responseDict["user"]["first_name"] +
                        " " + responseDict["user"]["last_name"])

            self.dlg.apiInput.setPlainText(
                f'API succesfully validated: Registered username is {userName}')

            # Disable the register button
            self.dlg.registerButton.setEnabled(False)

            result = True

        except:
            iface.messageBar().pushMessage("API Key failed test")
            self.forgetApiKey()
            result = False

        return result

    def forgetApiKey(self):
        s = QgsSettings()
        s.remove("ApiKey")
        self.dlg.apiInput.setPlainText(
            'Please paste a Fulcrum API Key here and click REGISTER')

        # Enable the register button. TODO: Is this the best time to do it?
        self.dlg.registerButton.setEnabled(True)

    def storeApiKey(self, apiKey):
        s = QgsSettings()
        s.setValue("ApiKey", apiKey)

    def recallApiKey(self):
        try:
            s = QgsSettings()
            apiKey = s.value("ApiKey")

            self.API_TOKEN = apiKey

        except:
            self.dlg.apiInput.setPlainText(
                'Please paste a Fulcrum API Key here and click REGISTER')
            iface.messageBar().pushMessage("Could Not Recall API Key")

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = FulcrumSyncDialog()

        else:
            #  Disconnect button so it doesnt try to call the methods twice if we reload
            try:
                self.dlg.loadPointsButton.clicked.disconnect()
            except:
                pass

        # Attempt to read in a saved API Key from global QGIS storage
        self.recallApiKey()
        self.testApiKey(self.API_TOKEN)

        ############################################
        # Set up the connections between the dialog clicks and the methods

        # For the API Key
        self.dlg.registerButton.clicked.connect(lambda: self.registerApiKey())
        self.dlg.forgetButton.clicked.connect(lambda: self.forgetApiKey())

        # For the APps List
        self.dlg.getAppsButton.clicked.connect(lambda: self.getAppsList())

        # For the Layer Select
        self.dlg.listWidget.itemClicked.connect(self.getSelectedLayer)
        self.dlg.loadPointsButton.clicked.connect(
            lambda: self.getGeoJsonFromSelectedLayer())

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            pass
