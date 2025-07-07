# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickFieldEditor
                                 A QGIS plugin
 Quick Field Editor is a QGIS plugin that simplifies attribute table updates with tools for serial numbers, geometry calculations (area, length, perimeter), coordinates, date, time, text replacement, and field concatenation
                             -------------------
        begin                : 2025-07-06
        copyright            : (C) 2025 by Anustup Jana
        email                : anustupjana21@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load QuickFieldEditor class from file QuickFieldEditor.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .quick_field_editor import QuickFieldEditor
    return QuickFieldEditor(iface)