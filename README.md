# Project reports

QGIS plugin to generate reports (CSV and HTML) of properties and metadata about layers, fields and layouts of QGIS projects.

## Description

This plugin collects information and properties from different PyQGIS objects, such as layers, fields or layouts accessible from the project and generates open data files (CSV and HTML) with this information. The main objective is to have a tool to generate final reports on work done with QGIS.

## Install

Project reports QGIS Plugin is available in QGIS Official Plugin Repository. For install just open QGIS, select Plugins -> Manage and Install Plugins and search for the plugin.

![image](https://user-images.githubusercontent.com/4746157/211209142-df602460-01be-42df-98e4-b0bb9211df73.png)


In case of manual installation, you can clone this repository latest release, unzip it into zip directory and enable plugin under QGIS Installed Plugins.

## Usage

After installing the plugin it will be accessible from the Plugin menu and in the toolbar via a shortcut.

When clicking on the tool, a side panel will appear with the different options of the plugin:

- Output directory
- Objects.
- Output formats (CSV and HTML)

![image](https://user-images.githubusercontent.com/4746157/211208664-d3b716d4-957d-42e4-8666-7b08f23b88b8.png)

After clicking on the Create Reports button the generated files will be available in the indicated directory.

## Outputs

- CVS
- HMTL (with CSS)

It is possible to customize the CSS style sheet of the HTML by editing the existing CSS variable in the class file (QProjectReport.py)

![image](https://user-images.githubusercontent.com/4746157/211209086-a60984cf-5bb9-4415-9977-aa919f83f567.png)

## Information about QGIS objects

### Project

Main PyQGIS class [QgsProject](https://qgis.org/pyqgis/master/core/QgsProject.html#module-QgsProject)

- **title**: The project's title
- **fileName**: The project's file name.
- **homePath**: The project's home path
- **crs**: Project's native coordinate reference system.
- **layers_count**: The number of registered layers
- **creationDate**: The date when the project was created
- **lastSaveDate**: The date when the project was last saved

### Layers

Main PyQGIS class [QgsVectorLayer]([https://qgis.org/pyqgis/master/core/QgsProject.html#module-QgsProject](https://qgis.org/pyqgis/master/core/QgsVectorLayer.html#module-QgsVectorLayer)) and [QgsRasterLayer](https://qgis.org/pyqgis/master/core/QgsRasterLayer.html#module-QgsRasterLayer))

- **name**: The display name of the layer
- **crs**: Layer's spatial reference system.
- **path_url**: URL from the datastorage
- **storage**: The permanent storage type for this layer as a friendly name.
- **encoding**: The character encoding of the data in the resource. 
- **geometry_type**: Returns point, line or polygon
- **features_count**: Number of features rendered with specified legend key.
- 
### Fields

Main PyQGIS class [QgsProject](https://qgis.org/pyqgis/master/core/QgsFields.html#module-QgsFields)

- **layer**: Layer name.
- **field_name**: Field name
- **display_name**: The name to use when displaying this field
- **alias**: The alias for the field (the friendly displayed name of the field ), or an empty string if there is no alias.
- **type_name**: Field variant type
- **type**: Field type (e.g., char, varchar, text, int, serial, double).
- **length**: Field length

### Layouts

Main PyQGIS class [QgsLayoutManager](https://qgis.org/pyqgis/master/core/QgsLayoutManager.html#qgis.core.QgsLayoutManager.layouts)

- **layout_name**: Layout name.
- **layout_type**: Master layout type (PrintLayout or Report)
- **atlas**: Is an Atlas? (True/False)
- **atlas_coverageLayer_name**: Coverage layer name used for the atlas features.

### Contributing

For collaborations and contributions, you can follow this [good practice guide](https://github.com/firstcontributions/first-contributions)


