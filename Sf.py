import shapefile
from pyproj import Transformer


class Sf:
    def __init__(self, namePath: str):
        self.namePath = namePath
        self.inputCordSystem = ""
        self.outputCordSystem = ""
        self.shapeFiles = shapefile.Reader(f'shapefiles/{namePath}/{namePath}')

    def getGEOJson(self, inputCordSystem: str, outputCordSystem: str):
        self.inputCordSystem = inputCordSystem
        self.outputCordSystem = outputCordSystem
        shape_rec = self.shapeFiles.shapeRecords()
        t = shape_rec.__geo_interface__
        transformer = Transformer.from_crs(self.inputCordSystem, self.outputCordSystem, always_xy=True)
        t_geo_json = {'type': 'FeatureCollection', "name": self.namePath,
                      "crs": {
                          "type": "name",
                          "properties": {
                              "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                          }
                      }, 'features': []}

        for f in t['features']:
            cord_tmp = []
            for c in f['geometry']['coordinates']:
                t = transformer.transform(c[0], c[1])
                cord_tmp.append(t)
            t_geo_json['features'].append({'type': 'Feature',
                                           'properties': {
                                               'ID': f['properties']['ID'],
                                               'lunghezza': f['properties']['lunghezza']
                                           },
                                           'geometry': {
                                               'type': 'LineString',
                                               'coordinates': cord_tmp
                                           }
                                           })

        return t_geo_json
