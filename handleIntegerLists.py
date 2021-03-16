geoj_layer = QgsVectorLayer(geoj, '', 'ogr')
refactor = []
field_error = []
for field in geoj_layer.fields(): # creation of a list with the field and field type of the layer.
    refactor_field = {}
    refactor_field['expression']=str("\"")+field.name()+str("\"")
    refactor_field['name']=field.name()
    refactor_field['precision']=field.precision()
    if field.typeName() == "IntegerList": # if the field as a not well handled type
        field_error.append(field.name()[:10])
        refactor_field['length']=0
        refactor_field['type']=10
    else :
        refactor_field['type']=field.type()
    refactor.append(refactor_field)

output_path = path + 'new_layer.shp'
# I'm using refactorfield algorithm from Qgis to create a new layer with some modification on specified fields.
processing.run("qgis:refactorfields", {'INPUT':geoj,'FIELDS_MAPPING':refactor,'OUTPUT':output_path})
iface.addVectorLayer(output_path,'', 'ogr')

# Modification of the value for a better value
geoj_layer = QgsVectorLayer(output_path, '', 'ogr')
for field_name in field_error:
    for f in geoj_layer.getFeatures() :
        attrs= f.attributes()
        value = attrs[geoj_layer.fields().indexFromName(field_name)]
        string = re.split(',|:|\)', value)
        new_value = ''
        for elem in string[1:-1] :
            if elem == string[1:-1][-1] :
                new_value = new_value +str(elem)
            else :
                new_value = new_value +str(elem) + ", "
        geoj_layer.startEditing()
        geoj_layer.changeAttributeValue(f.id(), geoj_layer.fields().indexFromName(field_name), new_value )
        geoj_layer.commitChanges()
        geoj_layer.triggerRepaint()