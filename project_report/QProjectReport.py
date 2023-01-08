import csv
import os

from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsRasterLayer

CSS = """
    <style>
html,body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe WPC", "Segoe UI",
          system-ui, "Ubuntu", "Droid Sans", sans-serif;
        font-size: 14px;
        line-height: 1.6;
        padding: 0 26px;
        word-wrap: break-word;
      }

      body {
        padding-top: 1em;
        padding-bottom: 2em;
      }

      h2,h3,h4,h5,h6 {
        font-weight: normal;
        margin-bottom: 0.2em;
      }

      h1 {
        padding-bottom: 0.3em;
        line-height: 1.2;
        border-bottom-width: 2px;
        border-bottom-style: solid;
        font-weight: normal;
      }

      p {
        margin-bottom: 0.7em;
      }

      table {
        border-collapse: collapse;
        margin-bottom: 0.7em;
        
      }

      th {
        text-align: left;
        border-bottom: 1.5px solid;
      }

      th,td {
        padding: 1px 10px;
      }
      td {
        word-break: break-word;
        max-width: 30em;
        border-top: 0.5px solid;
      }
    </style>"""


def get_url(layer_object):
    """Returns the URL of a layer object.

       Parameters:
       layer_object (QgsVectorLayer or QgsRasterLayer): The layer object to get the URL of.

       Returns:
       str: The URL of the layer object.
       """

    if isinstance(layer_object, QgsVectorLayer):
        path_url = layer_object.source()
    elif isinstance(layer_object, QgsRasterLayer) and layer_object.providerType() == 'gdal':
        path_url = layer_object.source()
    else:
        path_url = layer_object.source().split('url=')[1]
    return path_url


def create_table(title, headers, data):
    """Creates an HTML table from a list of headers and a list of data rows.

    Parameters:
    title (str): a string for the title
    headers (list): a list of strings representing the table headers
    data (list): a list of lists representing the table rows, where each inner list contains the cells for a single row

    Returns:
    str: an HTML string representing the table
    """

    table_html = ["<thead><tr>"]

    for cell in headers:
        table_html.append("<th>{}</th>".format(cell))

    table_html.append("</tr></thead>")

    table_html.append("<tbody>")

    for row in data:
        table_html.append("<tr>")
        for cell in row:
            table_html.append("<td>{}</td>".format(cell))
        table_html.append("</tr>")
    table_html.append("</tbody>")

    return "<div><h2>{}</h2><table>{}</table></div>".format(title, "\n".join(table_html))


class QProjectReport:
    """ Class with information and properties of QGIS projects and their objects (layers, fields and layouts)
    and generation of output files."""

    def __init__(self, qgsproject, output_directory):
        """Class Constructor. Generates the attributes relative to the QGIS project.

        :param qgsproject: QGIS project
        :type qgsproject: QgsProject object

        :param output_directory: Directory for creating folders and property files
        :type output_directory: str
        """

        # Project
        self.qgsproject = qgsproject
        self.folder = output_directory
        self.project_name = (self.qgsproject.fileName().split('/')[-1]).split('.')[0]
        self.report_directory = os.path.join(self.folder, self.project_name)
        self.csv_directory = os.path.join(self.report_directory, 'csv')
        self.html_directory = os.path.join(self.report_directory, 'html')

        self.project_column_names = ['title',
                                     'fileName',
                                     'filePath',
                                     'crs',
                                     'layers_count',
                                     'creationDate',
                                     'lastSaveDate'
                                     ]
        self.project_file_path = os.path.split(self.qgsproject.fileName())[0]
        self.project_file_name = os.path.split(self.qgsproject.fileName())[1]
        self.project_data = [[
            self.qgsproject.title(),
            self.project_file_name,
            self.project_file_path,
            self.qgsproject.crs().authid(),
            self.qgsproject.count(),
            self.qgsproject.metadata().creationDateTime().date().toString("yyyy-MM-dd"),
            self.qgsproject.lastSaveDateTime().date().toString("yyyy-MM-dd")
        ]]

        # Layers
        self.layers = self.qgsproject.mapLayers().values()

        self.layers_column_names = ['id',
                                    'name',
                                    'storage',
                                    'path_url',
                                    'crs',
                                    'encoding',
                                    'geometry_type',
                                    'features_count',
                                    ]

        self.layers_data = []

        # Fields
        self.layer_fields_column_names = ["id", "layer", "field_name", "display_name", "alias", "type_name",
                                          "type", "length"]
        self.layer_fields_data = []

        for index, layer in enumerate(self.layers, start=1):

            layer_type = 1 if isinstance(layer, QgsVectorLayer) else 0
            layer_name = layer.name()
            crs = layer.crs().authid()
            # path_url = layer.source() if layer_type == 1 else layer.source().split('url=')[1]
            path_url = get_url(layer)
            layer_storage = layer.dataProvider().storageType() if layer_type == 1 else layer.providerType()
            encoding = layer.dataProvider().encoding() if layer_type == 1 else ''
            geometry = QgsWkbTypes.geometryDisplayString(layer.geometryType()) if layer_type == 1 else ''
            features = layer.featureCount() if layer_type == 1 else ''
            # creationDate = ''
            # lastSaveDate = ''

            self.layers_data.append([index, layer_name, layer_storage,  path_url, crs, encoding, geometry, features])

            if isinstance(layer, QgsVectorLayer):
                for index, field in enumerate(layer.fields(), start=1):
                    field_name = field.name()
                    display_name = field.displayName()
                    alias = field.alias()
                    # comment = field.comment(),
                    type_name = field.typeName()
                    field_type = field.type()
                    length = field.length()
                    # precision = field.precision(),

                    self.layer_fields_data.append([index, layer_name, field_name, display_name, alias, type_name,
                                                   field_type, length])

        # Layouts
        self.layouts = self.qgsproject.layoutManager().layouts()

        self.layouts_column_names = ['id', 'layout_name', 'layout_type', 'atlas', 'atlas_coverageLayer_name']
        self.layouts_data = []

        dict_type_layouts = {0: "PrintLayout", 1: "Report", }

        for index, layout in enumerate(self.layouts, start=1):
            layout_name = layout.name()
            # project = layout.customProperties()
            layout_type = dict_type_layouts[layout.layoutType()]
            atlas = True if layout.layoutType() == 0 and layout.atlas().coverageLayer() is not None else False
            # atlas_count = layout.atlas().count() if  layout.layoutType() == 0 else ''
            atlas_coverageLayer_name = layout.atlas().coverageLayer().name() if layout.layoutType() == 0 and atlas else ''

            self.layouts_data.append([index, layout_name, layout_type, atlas, atlas_coverageLayer_name])

        # Check
        self.check_project = False
        self.check_layers = False
        self.check_layouts = False
        self.check_fields = False

    def scaffolding(self):
        """"Making folders structure"""

        if not os.path.exists(self.report_directory):
            os.mkdir(self.report_directory)
            os.mkdir(self.csv_directory)
            os.mkdir(self.html_directory)
            print("Directory '% s' created" % self.report_directory)
        else:
            print("Directory '% s' already exists" % self.report_directory)

    def createCSVProject(self):
        """Creating CSV file with properties and info about the QGIS project"""

        csv_file = os.path.join(self.report_directory, self.csv_directory, '01_project.csv')

        with open(csv_file, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.project_column_names)
            writer.writerow(self.project_data)
            print("CSV project file  created")

    def createCSVLayers(self):
        """Create CSV file with properties and info about the QGIS project's layers"""

        csv_file = os.path.join(self.report_directory, self.csv_directory, '02_layers.csv')

        with open(csv_file, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.layers_column_names)
            writer.writerows(self.layers_data)
            print("CSV QGIS project's layers  created")

    def createCSVLayerFields(self):
        """Create CSV file with properties about the vector layers fields"""

        csv_file = os.path.join(self.report_directory, self.csv_directory, '03_fields.csv')

        with open(csv_file, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.layer_fields_column_names)
            writer.writerows(self.layer_fields_data)
            print("CSV vector layers fields created")

    def createCSVLayouts(self):
        """Create CSV file with properties about the layouts"""

        csv_file = os.path.join(self.report_directory, self.csv_directory, '04_layouts.csv')

        with open(csv_file, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.layouts_column_names)
            writer.writerows(self.layouts_data)
            print("CSV layouts created")

    def create_html(self, check_objets):
        """Create HTML report file"""

        self.check_project = check_objets[0]
        self.check_layers = check_objets[1]
        self.check_fields = check_objets[2]
        self.check_layouts = check_objets[3]

        html_file = os.path.join(self.report_directory, self.html_directory, 'project_report.html')
        html_title = self.project_data[0][0]
        html_string = """<html>
                        <head>{}</head>
                        <body>
                        <h1>QGIS Project Report <i>"{}"</i></h1>""".format(CSS, html_title)

        if self.check_project:
            html_string += create_table('Project', self.project_column_names, self.project_data)

        if self.check_layers:
            html_string += create_table('Layers', self.layers_column_names, self.layers_data)

        if self.check_fields:
            html_string += create_table('Fields', self.layer_fields_column_names, self.layer_fields_data)

        if self.check_layouts:
            html_string += create_table('Layouts', self.layouts_column_names, self.layouts_data)

        html_string += "</body></html>"

        with open(html_file, 'w') as html_file:
            html_file.write(html_string)
