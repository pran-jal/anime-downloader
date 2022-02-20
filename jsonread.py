import json
import JsonWrite

def url() :
    try :
        f = open('data.json')
    #f = open('data.txt', 'r')
    #return json.loads(f.read())["@graph"][0]["video"]["embedUrl"]
    
    except :
        if Exception == FileNotFoundError :
            print( " JSON data file found ")
            ans = input( "Extract again ? (Y/n) ")
            if ans == 'Y' or ans == 'y' :
                JsonWrite.JsonWrite()
    finally :
        f = open('data.json')
        return json.load(f)["@graph"][0]["video"]["embedUrl"]