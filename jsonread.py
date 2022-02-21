import json
import JsonWrite

def url() :
    try :
        f = open('data.json')
        #return json.loads(open('data.txt', 'r').read())["@graph"][0]["video"]["embedUrl"]
    except FileNotFoundError as e :
        if e.__class__.__name__ == 'FileNotFoundError' :
            print( " JSON data file found ")
            ans = input( "Extract again ? (Y/n) ")
            if ans == 'Y' or ans == 'y' :
                JsonWrite.JsonWrite()
            
    finally :
        f = open('data.json')
        
        print(json.load(f)["@graph"][0]["video"]["embedUrl"] )
        f.close()

url()