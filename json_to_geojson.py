#!/usr/bin/env python3

from sys import exit
from json import load, dump

def read_file():
    try:
        inputfile = input("Filename: ").strip(' ')
        if not inputfile:
            raise ValueError('Error: Missing input file')
        if inputfile[-5:] != '.json':
            raise ValueError('Error: Input file is not JSON file')

        proppath = input("If the object holding the properties data in the JSON file is nested, input the path with dot separated each key (example: data.stations.0). If not, just press enter: ").strip(' ').split(".")

        propkey = input("Input the property keys in the JSON file that you want inside the geojson's properties object, with comma separated each key (example: name, age, height): ").strip(' ').split(",")
        if not propkey: raise ValueError('Error: Property keys are required.')

        longkey = input("JSON file's property key for longitude: ").strip(' ')
        if not longkey: raise ValueError('Error: Empty longitude input')
        latkey = input("JSON file's property key for latitude: ")
        if not latkey: raise ValueError('Error: Empty latitude input').strip(' ')

        fp = open(inputfile, 'r')
        jsonfile = load(fp)
        fp.close()

        propobj = get_properties_obj(jsonfile, proppath)
        return propobj, propkey, longkey, latkey

    except IOError:
        print('Could not read file: ', inputfile)
        exit()

    except Exception as e:
        print(e)
        exit()


def get_properties_obj(file, path):
    if path and path[0] != '':
        for p in path:
            if p.isdigit():
                p = int(p)
            file = file[p]
        return file

    return file


def create_geojson(propobj, propkey, longkey, latkey):
    geojson = {}
    geojson['type'] = 'FeatureCollection'

    features = []
    for prop in propobj:
        feature = {}
        feature['type'] = 'Feature'
        feature['geometry'] = {
            'type':'Point',
            'coordinates':[ prop[longkey], prop[latkey] ]
        }

        properties = {}
        for key in propkey:
            properties[key] = prop[key]

        feature['properties'] = properties
        features.append(feature)

    geojson['features'] = features
    return geojson


def main():
    propobj, propkey, longkey, latkey = read_file()
    geojson = create_geojson(propobj, propkey, longkey, latkey)

    with open('convert.geojson', 'w') as f:
        dump(geojson, f, indent=2)
    f.close()

    print("File conversion successful. You new GeoJSON is now available as convert.geojson.")


if __name__ == '__main__':
    main()