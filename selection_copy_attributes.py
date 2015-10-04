#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import qgis.utils
import json
import os


ICON = QIcon(os.path.join(os.path.dirname(__file__), os.path.sep.join(['images','icon.png'])))


class SelectionCopyAttributes:
    
    def __init__(self, iface):
        self.iface = iface
    
    def initGui(self):
        self.action = QAction(ICON, "Selection copy attributes", self.iface.mainWindow())
        QObject.connect(self.action, SIGNAL("triggered(bool)"), self.sel_copy_attrs)
        editMenu = self.iface.attributesToolBar()
        editMenu.addAction(self.action)
        editMenu.update()
    
    def sel_copy_attrs(self, checked):
        # find the active layer which is the source of the attributes
        srclyr = qgis.utils.iface.activeLayer()
        if not srclyr: return           # no source layer found
        # find the editable layer which is the destination of the attributes
        destlyr = [l for l in qgis.utils.iface.legendInterface().layers() if l.isEditable()]
        if len(destlyr) < 1: return     # no destlyr found
        destlyr = destlyr[0]    # we should only have one editable layer
        # get name of srclyr and limit max length to 10 characters
        srcname = srclyr.name()[:10]
        destidx = destlyr.fieldNameIndex(srcname)
        if destidx < 0: return    # we did not find an appropriate destination attribute
        # get the selected source feature attributes
        srcattrs = [f.name() for f in srclyr.pendingFields()]
        destval = []
        destval.append(srcattrs)
        srcfeats = srclyr.selectedFeatures()
        for f in srcfeats:
            # we need to replace NULL instances by None in order to serialize them to JSON values
            attrs = [None if isinstance(a, QPyNullVariant) else a for a in f.attributes()]
            destval.append(attrs)
        destval_json = json.dumps(destval)
        destfeats = destlyr.selectedFeatures()
        for f in destfeats:
            destlyr.changeAttributeValue(f.id(), destidx, destval_json)
        print 'attributes copied from %s to %s' % (srclyr.name(), destlyr.name())
    
    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        editMenu = self.iface.attributesToolBar()
        editMenu.removeAction(self.action)
        editMenu.update()
        QObject.disconnect(self.action, SIGNAL("triggered(bool)"), self.sel_copy_attrs)

