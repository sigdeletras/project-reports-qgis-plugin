# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProjectReport
                                 A QGIS plugin
 Genereate reports about project, layers, fields and layout
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2023-01-05
        copyright            : (C) 2023 by Patricio Soriano. Geoinnova
        email                : info@geoinnova.org
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
    """Load ProjectReport class from file ProjectReport.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .project_report import ProjectReport
    return ProjectReport(iface)