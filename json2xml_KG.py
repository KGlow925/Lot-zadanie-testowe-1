import argparse
import json
import os
import sys


def dicttoxml(data, outfile, tabs=""):
    if type(data) is list:
        for item in data:
            dicttoxml(item, outfile, tabs=tabs)
    elif type(data) is dict:
        for key in data.keys():
            outfile.write(tabs + '<' + key + '>' + '\n')
            dicttoxml(data[key], outfile, tabs=tabs + '\t')
            outfile.write(tabs + '</' + key + '>' + '\n')
    else:
        outfile.write(tabs + str(data) + '\n')


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--folder", required=True, help="Name of folder with JSONs")
parser.add_argument("-d", "--destination", required=True, help="Name of destination folder")

args = parser.parse_args()
json_folder = args.folder
destination = args.destination

if not os.path.isdir(json_folder):
    raise Exception("Incorrect folder path")

# If destination folder doesn't exist then I create it
if not os.path.exists(destination):
    os.makedirs(destination)

for filename in os.listdir(json_folder):
    is_json = True
    name = os.path.splitext(filename)[0]

    # Loading json file into dictionary
    with open(json_folder + '/' + filename, 'r', encoding='utf-8') as f:
        try:
            json_data = json.load(f)
        except Exception as e:
            print("WARNING: " + filename + " is not a json file", file=sys.stderr)
            is_json = False

    if is_json:
        # Converting dictionary into xml and writing it into out_file
        with open(destination + '/' + name + '.xml', 'w', encoding='utf-8') as f:
            dicttoxml(json_data, f)
