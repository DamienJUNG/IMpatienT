import os
import json


def load_onto():
    with open(os.path.join("data/ontology", "ontology.json.demo"), "r") as fp:
        onto_tree = json.load(fp)
    onto_tree_imgannot = [i for i in onto_tree if i["data"]["image_annotation"] == True]
    return onto_tree_imgannot
