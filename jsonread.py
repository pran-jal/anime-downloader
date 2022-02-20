import json

def url() :
    f = open("data.txt", 'r')
    string = f.read()
    a = json.loads(string)
    return a["@graph"][0]["video"]["embedUrl"]
