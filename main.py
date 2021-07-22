import json
from Sf import Sf


def elaborateGEOJson(shapeName):
    shapeFile = Sf(shapeName)
    GEOJson = shapeFile.getGEOJson("EPSG:3044", "EPSG:4326")
    json_object = json.dumps(GEOJson, indent=4)
    with open(f'GEOJson/{shapeName}.json', "w") as outfile:
        outfile.write(json_object)


if __name__ == '__main__':
    elaborateGEOJson('ABI4TERAMO000000')
