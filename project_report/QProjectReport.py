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
        max-width: 15em;
        border-top: 0.5px solid;
      }
      footer {
        font-size: x-small;
        padding-top: 1em;
        text-align: right;
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


def create_table(title, headers, data, single_row=False):
    """Creates an HTML table from a list of headers and a list of data rows.

    Parameters:
    title (str): a string for the title
    headers (list): a list of strings representing the table headers
    data (list): a list of lists representing the table rows, where each inner list contains the cells for a single row
    single_row (bool, optional): a flag indicating whether the data should be formatted in a single row (default: False)

    Returns:
    str: an HTML string representing the table
    """

    table_html = ["<thead><tr>"]

    for cell in headers:
        table_html.append("<th>{}</th>".format(cell))

    table_html.append("</tr></thead>")

    table_html.append("<tbody>")

    if single_row:
        table_html.append("<tr>")
        for cell in data:
            table_html.append("<td>{}</td>".format(cell))
        table_html.append("</tr>")
    else:
        for row in data:
            table_html.append("<tr>")
            for cell in row:
                table_html.append("<td>{}</td>".format(cell))
            table_html.append("</tr>")
    table_html.append("</tbody>")

    return "<div>{}<table>{}</table></div>".format(title, "\n".join(table_html))


def remove_outputfolders(main_directory):
    """Remove all files and subfolders within a given folder, then remove the folder itself.

    Parameters:
    main_directory (str): the path to the folder to be removed
    """
    try:
        for root, dirs, files in os.walk(main_directory, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
            os.rmdir(main_directory)
    except OSError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


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
        self.report_directory = os.path.join(self.folder, self.project_name) if self.project_name else os.path.join(
            self.folder, 'untitled_project')
        self.csv_directory = os.path.join(self.report_directory, 'csv')
        self.html_directory = os.path.join(self.report_directory, 'html')

        self.project_column_names = ['title',
                                     'file_name',
                                     'file_path',
                                     'crs_project',
                                     'layers_count',
                                     'creation_date',
                                     'last_save_date'
                                     ]
        self.project_file_path = os.path.split(self.qgsproject.fileName())[0]
        self.project_file_name = os.path.split(self.qgsproject.fileName())[1]
        self.project_data = [
            self.qgsproject.title(),
            self.project_file_name,
            self.project_file_path,
            f'{self.qgsproject.crs().authid()} {self.qgsproject.crs().description()}',
            self.qgsproject.count(),
            self.qgsproject.metadata().creationDateTime().date().toString("yyyy-MM-dd"),
            self.qgsproject.lastSaveDateTime().date().toString("yyyy-MM-dd")
        ]

        ## Relations

        self.project_relations_column_names = ['name',
                                               'referenced_layer',
                                               'referencing_layer',
                                               'field_pairs'
                                               ]
        self.project_relations_data = []

        self.relations = self.qgsproject.relationManager().relations()

        for k, v in self.relations.items():
            name = v.name() # Returns a human readable name for this relation.
            ## print(v.referencedFields()) # Returns a list of attributes used to form the referenced fields (most likely primary key) on the referenced (parent) layer.
            referencedLayer = v.referencedLayer().name() # Access the referenced (parent) layer
            ## print(v.referencingFields()) # Returns a list of attributes used to form the referencing fields (foreign key) on the referencing (child) layer.
            referencingLayer = v.referencingLayer().name() # Access the referencing (child) layer
            fieldPairs = v.fieldPairs()
            ## print(v.strength()) # Returns the relation strength as a string
            ## print(v.type()) # Returns the type of the relation

            self.project_relations_data.append([name, referencedLayer, referencingLayer, fieldPairs])

        # Layers
        self.layers = self.qgsproject.mapLayers().values()

        self.vector_layers_column_names = ['id',
                                           'name',
                                           'storage',
                                           # 'comment',
                                           'metadata_abstract',
                                           'path_url',
                                           'crs_layer',
                                           'encoding',
                                           'geometry_type',
                                           'features_count',
                                           'joins'
                                           ]

        self.vector_layers_data = []

        self.raster_layers_column_names = ['id',
                                           'name',
                                           'storage',
                                           # 'comment',
                                           'metadata_abstract',
                                           'path_url',
                                           'crs_layer',
                                           ]

        self.raster_layers_data = []

        # Fields
        self.layer_fields_column_names = ["id", "layer_id", "layer", "field_name", "display_name", "alias", "type_name",
                                          "type", "length"]
        self.layer_fields_data = []

        # Joins
        self.layer_joins_column_names = ["id", "layer_id", "layer", "join_layer", "join_field_name", "target_field_name"]
        self.layer_joins_data = []

        for index, layer in enumerate(self.layers, start=1):
            provider = layer.dataProvider()
            metadata = layer.metadata()

            layer_type = 1 if isinstance(layer, QgsVectorLayer) else 0
            layer_index = index
            layer_name = layer.name()
            crs = f'{layer.crs().authid()} {layer.crs().description()}'
            # path_url = layer.source() if layer_type == 1 else layer.source().split('url=')[1]
            # comment = provider.dataComment()
            abstract = metadata.abstract()
            path_url = get_url(layer)
            layer_storage = layer.dataProvider().storageType() if layer_type == 1 else layer.providerType()
            encoding = layer.dataProvider().encoding() if layer_type == 1 else ''
            geometry = QgsWkbTypes.geometryDisplayString(layer.geometryType()) if layer_type == 1 else ''
            features = layer.featureCount() if layer_type == 1 else ''
            joins = len(layer.vectorJoins()) if layer_type == 1 else ''
            # creationDate = ''
            # lastSaveDate = ''

            if isinstance(layer, QgsVectorLayer):
                self.vector_layers_data.append(
                    [layer_index, layer_name, layer_storage, abstract, path_url, crs, encoding, geometry,
                     features, joins]) # comment

                for index_field, field in enumerate(layer.fields(), start=1):
                    field_name = field.name()
                    display_name = field.displayName()
                    alias = field.alias()
                    # comment = field.comment(),
                    type_name = field.typeName()
                    field_type = field.type()
                    length = field.length()
                    # precision = field.precision(),

                    self.layer_fields_data.append(
                        [index_field, layer_index, layer_name, field_name, display_name, alias, type_name,
                         field_type, length])

                ## Joins

                if joins > 0:
                    vector_joins = layer.vectorJoins()
                    for index_join, join in enumerate(vector_joins, start=1):
                        join_layer = vector_joins[index_join - 1].joinLayer().name()
                        join_fieeld_name = vector_joins[index_join - 1].joinFieldName()
                        target_field_name = vector_joins[index_join - 1].targetFieldName()

                        self.layer_joins_data.append([index_join, layer_index, layer_name, join_layer,
                                                      join_fieeld_name, target_field_name])




            else:
                self.raster_layers_data.append(
                    [index, layer_name, layer_storage, abstract, path_url, crs]) # comment

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
        self.check_vector_layers = False
        self.check_raster_layers = False
        self.check_layouts = False
        self.check_fields = False
        self.check_joins = False
        self.check_relations = False

    def scaffolding(self):
        """"Making folders structure"""

        if not os.path.exists(self.report_directory):
            os.mkdir(self.report_directory)
            os.mkdir(self.csv_directory)
            os.mkdir(self.html_directory)
            # print("Directory '% s' created" % self.report_directory)
        else:
            remove_outputfolders(self.csv_directory)
            remove_outputfolders(self.html_directory)
            os.mkdir(self.csv_directory)
            os.mkdir(self.html_directory)
            # print("Directory '% s' already exists" % self.report_directory)

    def create_csv_file(self, file_name, column_names, data, single_row=False):
        """
        Creates a CSV file with the given file name, column names, and data.

        Parameters:
            - file_name (str): The name of the file to be created, without the file extension.
            - column_names (list): A list of strings representing the names of the columns in the CSV file.
            - data (list): A list of data to be written to the file.
            - single_row (bool): A boolean value indicating whether the data should be written as a single row
            or multiple rows. Default is False.

        Returns:
            None
        """

        csv_file = os.path.join(self.report_directory, self.csv_directory, file_name + '.csv')

        with open(csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(column_names)
            if single_row:
                writer.writerow(data)
            else:
                writer.writerows(data)

    def create_html(self, check_objets):
        """Create HTML report file"""

        self.check_project = check_objets[0]
        self.check_vector_layers = check_objets[1]
        self.check_raster_layers = check_objets[2]
        self.check_fields = check_objets[3]
        self.check_layouts = check_objets[4]
        self.check_joins = check_objets[5]
        self.check_relations = check_objets[6]

        html_file = os.path.join(self.report_directory, self.html_directory, 'project_report.html')
        html_title = self.project_data[0]
        html_string = """<html>
                        <head>{}</head>
                        <body>
                        <h1>QGIS Project Report <i>"{}"</i></h1>""".format(CSS, html_title)

        if self.check_project:
            html_string += create_table('<h2>Project</h2>', self.project_column_names, self.project_data, True)

        if self.check_raster_layers:
            html_string += create_table('<h2>Raster layers</h2>', self.raster_layers_column_names, self.raster_layers_data)

        if self.check_vector_layers:
            html_string += create_table('<h2>Vector layers</h2>', self.vector_layers_column_names, self.vector_layers_data)

        if self.check_relations:
            html_string += create_table('<h2>Relations</h2>', self.project_relations_column_names, self.project_relations_data)

        if self.check_joins:
            html_string += """<h2>Vector layers joins</h2>"""
            for vector_layer in self.vector_layers_data:
                n_joins = vector_layer[9]
                if n_joins > 0:
                    layer_id = vector_layer[0]
                    layer_name = vector_layer[1]
                    layer_joins_data_filtered = filter(lambda c: c[1] == layer_id, self.layer_joins_data)
                    html_string += create_table('<h3><i>Layer: {}</i></h3>'.format(layer_name), self.layer_joins_column_names,
                                                layer_joins_data_filtered)

        if self.check_fields:
            html_string += """<h2>Vector layers fields</h2>"""
            for vector_layer in self.vector_layers_data:
                layer_id = vector_layer[0]
                layer_name = vector_layer[1]
                layer_fields_data_filtered = filter(lambda c: c[1] == layer_id, self.layer_fields_data)
                html_string += create_table('<h3><i>Layer: {}</i><h3>'.format(layer_name), self.layer_fields_column_names,
                                            layer_fields_data_filtered)

        if self.check_layouts:
            html_string += create_table('<h2>Layouts</h2>', self.layouts_column_names, self.layouts_data)

        html_string += """<footer> <p>Generated with "Project Reports" QGIS plugin by Patricio Soriano <a 
        href="https://sigdeletras.com/">@SIGdeletras</a></p> </footer> """

        html_string += "</body></html>"

        with open(html_file, 'w') as html_file:
            html_file.write(html_string)
