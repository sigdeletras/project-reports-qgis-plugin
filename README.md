# Project reports (v.1.2)

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

- CVS (semicolon delimited)
- HMTL (with CSS)

It is possible to customize the CSS style sheet of the HTML by editing the existing CSS variable in the class file (QProjectReport.py)

![image](https://user-images.githubusercontent.com/4746157/211212255-86c0924b-4eda-4f64-bdb1-07c8438db6a7.png)

![image](https://user-images.githubusercontent.com/4746157/211209086-a60984cf-5bb9-4415-9977-aa919f83f567.png)

## Information about QGIS objects

### Project

Main PyQGIS class [QgsProject](https://qgis.org/pyqgis/master/core/QgsProject.html#module-QgsProject)

- **title**: The project's title
- **file_name**: The project's file name.
- **file_path**: The project's home path
- **crs_project**: Project's native coordinate reference system.
- **layers_count**: The number of registered layers
- **creation_date**: The date when the project was created
- **last_save_date**: The date when the project was last saved

### Relations

Main PyQGIS class [QgsRelationManager](https://qgis.org/pyqgis/master/core/QgsRelationManager.html)

- **name**: The human readable name for this relation.
- **referenced_layer**: The referenced (parent) layer.
- **referencing_layer**: The referencing (child) layer This is the layer which has the field(s) which point to another layer.
- **field_pairs**: Returns the field pairs which form this relation.

### Layers

Main PyQGIS class [QgsVectorLayer](https://qgis.org/pyqgis/master/core/QgsVectorLayer.html#module-QgsVectorLayer)) and [QgsRasterLayer](https://qgis.org/pyqgis/master/core/QgsRasterLayer.html#module-QgsRasterLayer))

- **id**: Identification number in the report.
- **name**: The display name of the layer
- **storage**: The permanent storage type for this layer as a friendly name.
- **metadata_abstract**: The metadata summary of the layer (if added in the project).
- **path_url**: URL from the datastorage
- **crs_layer**: Layer's spatial reference system.

For the vector layers only:

- **encoding**: The character encoding of the data in the resource. 
- **geometry_type**: Returns point, line or polygon
- **features_count**: Number of features rendered with specified legend key.
- **joins**: Number of layer joints
### Fields

Main PyQGIS class [QgsFields](https://qgis.org/pyqgis/master/core/QgsFields.html#module-QgsFields)

- **id**: Identification number in the report.
- **layer_id**: Layer identification number in the report.
- **layer**: Layer name.
- **field_name**: Field name
- **display_name**: The name to use when displaying this field
- **alias**: The alias for the field (the friendly displayed name of the field ), or an empty string if there is no alias.
- **type_name**: Field variant type
- **type**: Field type (e.g., char, varchar, text, int, serial, double).
- **length**: Field length

### Joins

Main PyQGIS class [QgsVectorLayerJoinInfo](https://qgis.org/pyqgis/master/core/QgsVectorLayerJoinInfo.html#qgis.core.QgsVectorLayerJoinInfo)

- **id**: Identification number in the report.
- **layer_id**: Layer identification number in the report.
- **layer**: Layer name.
- **join_layer**: The Joined layer name
- **join_field_name**: The name of the field of joined layer that will be used for join
- **target_field_name**: The name of the field of our layer that will be used for join.
### Layouts

Main PyQGIS class [QgsLayoutManager](https://qgis.org/pyqgis/master/core/QgsLayoutManager.html#qgis.core.QgsLayoutManager.layouts)

- **layout_name**: Layout name.
- **layout_type**: Master layout type (PrintLayout or Report)
- **atlas**: Is an Atlas? (True/False)
- **atlas_coverageLayer_name**: Coverage layer name used for the atlas features.

### Changelog
- 2023/01/19 1.2 Added layer metadata abstract. Link to out_folder in message. Added CRS Description. Splitted  fields table's html by layers. Joins' information implemented. Changes in HTML headings for subtables. Relations' information implemented
- 2023/01/12 1.1 Fixing error in project csv file. Added More warnings about if the destination folder exists. The HTML and CSV subfolders are only deleted if the parent folder already exists.  Improved  class methods. Added 'comment' information about layer.
- 2023/01/08 1.0 HTML output option. Check the options selected in the GUI and update the state of the "Create Report" button.
- 2023/01/06 0.1 Initial release

### Contributing

For collaborations and contributions, you can follow this [good practice guide](https://github.com/firstcontributions/first-contributions)


