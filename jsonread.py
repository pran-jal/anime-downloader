
import json

def url() :
    f = open("data.json")
    a = json.load(f)
    return a["@graph"][0]["video"]["embedUrl"]
