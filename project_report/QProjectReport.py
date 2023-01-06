import csv
import os

from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsRasterLayer


def getURL(layer_object):
    """Static function to get the url from layer source

    :param layer_object: QGIS layer
    :type layer_object: QgsMapLayer
    """

    if isinstance(layer_object, QgsVectorLayer):
        path_url = layer_object.source()
    elif isinstance(layer_object, QgsRasterLayer) and layer_object.providerType() == 'gdal':
        path_url = layer_object.source()
    else:
        path_url = layer_object.source().split('url=')[1]
    return path_url


class QProjectReport:
    """ Class with information and properties of QGIS projects and their objects (layers, fields and layouts)
    and generation of output files."""

    def __init__(self, qgsproject, folder):
        """Class Constructor. Generates the attributes relative to the QGIS project.

        :param qgsproject: QGIS project
        :type qgsproject: QgsProject object

        :param folder: Directory for creating folders and property files
        :type folder: str
        """

        # Project
        self.qgsproject = qgsproject
        self.folder = folder
        self.project_name = (self.qgsproject.fileName().split('/')[-1]).split('.')[0]
        self.report_directory = os.path.join(self.folder, self.project_name)
        self.csv_directory = os.path.join(self.report_directory, 'csv')

        self.project_column_names = ['title',
                                     'fileName',
                                     'homePath',
                                     'crs',
                                     'layers_count',
                                     'creationDate',
                                     'lastSaveDate'
                                     ]
        self.project_data = [
            self.qgsproject.title(),
            self.qgsproject.fileName(),
            self.qgsproject.homePath(),
            self.qgsproject.crs().authid(),
            self.qgsproject.count(),
            self.qgsproject.metadata().creationDateTime().date().toString("yyyy-MM-dd"),
            self.qgsproject.lastSaveDateTime().date().toString("yyyy-MM-dd")
        ]

        # Layers
        self.layers = self.qgsproject.mapLayers().values()

        self.layers_column_names = ['name',
                                    'crs',
                                    'path_url',
                                    'storage',
                                    'encoding',
                                    'geometry_type',
                                    'features_count',
                                    ]

        self.layers_data = []

        # Fields
        self.layer_fields_column_names = ["layer", "field_name", "display_name", "alias", "comment", "type_name",
                                          "type",
                                          "length", "precision"]
        self.layer_fields_data = []

        for layer in self.layers:

            layer_type = 1 if isinstance(layer, QgsVectorLayer) else 0

            layer_name = layer.name()
            crs = layer.crs().authid()
            # path_url = layer.source() if layer_type == 1 else layer.source().split('url=')[1]
            path_url = getURL(layer)
            layer_storage = layer.dataProvider().storageType() if layer_type == 1 else layer.providerType()
            encoding = layer.dataProvider().encoding() if layer_type == 1 else ''
            geometry = QgsWkbTypes.geometryDisplayString(layer.geometryType()) if layer_type == 1 else ''
            features = layer.featureCount() if layer_type == 1 else ''
            # creationDate = ''
            # lastSaveDate = ''

            self.layers_data.append([layer_name, crs, path_url, layer_storage, encoding, geometry, features])

            if isinstance(layer, QgsVectorLayer):
                for field in layer.fields():
                    field_name = field.name()
                    display_name = field.displayName()
                    alias = field.alias()
                    comment = field.comment(),

                    type_name = field.typeName()
                    field_type = field.type()
                    length = field.length()
                    precision = field.precision(),

                    self.layer_fields_data.append([layer_name, field_name, display_name, alias, comment, type_name,
                                                   field_type, length, precision])

        # Layouts
        self.layouts = self.qgsproject.layoutManager().layouts()

        self.layouts_column_names = ['layout_name', 'layout_type', 'atlas', 'atlas_coverageLayer_name']
        self.layouts_data = []

        dict_type_layouts = {0: "PrintLayout", 1: "Report", }

        for layout in self.layouts:
            layout_name = layout.name()
            # project = layout.customProperties()
            layout_type = dict_type_layouts[layout.layoutType()]
            atlas = True if layout.layoutType() == 0 and layout.atlas().coverageLayer() is not None else False
            # atlas_count = layout.atlas().count() if  layout.layoutType() == 0 else ''
            atlas_coverageLayer_name = layout.atlas().coverageLayer().name() if layout.layoutType() == 0 and atlas else ''

            self.layouts_data.append([layout_name, layout_type, atlas, atlas_coverageLayer_name])

    def scaffolding(self):
        """"Making folders structure"""

        if not os.path.exists(self.report_directory):
            os.mkdir(self.report_directory)
            os.mkdir(self.csv_directory)
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
