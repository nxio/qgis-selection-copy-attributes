"""
SelectionCopyAttributes
-----------------------

QGIS plugin to copy attributes of selected features from one layer to another layer.
"""
def name():
    return "SelectionCopyAttributes"
def description():
    return "QGIS plugin to copy attributes of selected features from one layer to another layer."
def version():
    return "Version 0.0.1"
def icon():
    return "icon.png"
def author():
    return "Christian Kaiser"
def email():
    return "ck@naxio.ch"
def category():
  return "Vector"
def qgisMinimumVersion():
    return "2.0"
def classFactory(iface):
    from selection_copy_attributes import SelectionCopyAttributes
    return SelectionCopyAttributes(iface)
