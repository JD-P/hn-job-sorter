#Tool to create a labelled training set from a HN hiring thread

from urllib.request import urlopen
from urllib.error import URLError
from os.path import isfile
import argparse
import json


def open_hn_item(id_):
    try:
        opened = urlopen("https://hacker-news.firebaseio.com/v0/item/" 
                         + str(id_) + ".json")
    except URLError:
        print("Unable to open item ID: API is down or your item ID is invalid.")
    text = opened.read()
    return json.loads(text.decode())

parser = argparse.ArgumentParser()
parser.add_argument("ID", help="The ID of the HN API item to tag.")
parser.add_argument("outfile", help="The filepath to write output to.")
arguments = parser.parse_args()

thread = open_hn_item(arguments.ID)
if isfile(arguments.outfile):
    with open(arguments.outfile) as infile:
        labels = json.load(infile)
else:
    labels = []

labelled = 0
for descendant in thread["kids"]:
    post = open_hn_item(descendant)
    try:
        first_line = post["text"].split("<p>")[0]
    except KeyError:
        continue
    print(labelled, "of", len(thread["kids"]))
    print("FIRST LINE:\n", " " * len("FIRST LINE:"), first_line)
    label = input("Is this a well formed first line?\n>>>")
    while label != "0" and label != "1":
        label = input("Label must be 1 or 0.\n>>>")
    labels.append([first_line.replace("\t", " " * 4), int(label)])
    labelled += 1

outfile = open(arguments.outfile, "w")
json.dump(labels, outfile)
