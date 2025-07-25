# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickFieldEditor
                                 A QGIS plugin
 Quick Field Editor is a QGIS plugin that simplifies attribute table updates with tools for serial numbers, geometry calculations (area, length, perimeter), coordinates, date, time, text replacement, and field concatenation
                              -------------------
        begin                : 2025-07-06
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Anustup Jana
        email                : anustupjana21@gmail.com
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from .quick_field_editor_dialog import QuickFieldEditorDialog
import os.path

class QuickFieldEditor:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'QuickFieldEditor_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.actions = []
        self.menu = self.tr(u'&Quick Field Editor')
        self.first_start = None

    def tr(self, message):
        """Get the translation for a string using Qt translation API."""
        return QCoreApplication.translate('QuickFieldEditor', message)

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
        """Add a toolbar icon to the toolbar."""
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)
        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.add_action(
            icon_path,
            text=self.tr(u'Quick Field Editor'),
            callback=self.run,
            parent=self.iface.mainWindow(),
            status_tip=self.tr(u'Update attribute fields with calculations and text operations'),
            whats_this=self.tr(u'Quick Field Editor simplifies attribute table updates with tools for serial numbers, geometry calculations, coordinates, date, time, text replacement, and field concatenation')
        )
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Quick Field Editor'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work."""
        if self.first_start:
            self.first_start = False
            self.dlg = QuickFieldEditorDialog(parent=self.iface.mainWindow())

        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            pass