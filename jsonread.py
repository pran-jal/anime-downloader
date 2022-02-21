import json
import JsonWrite

def url():
    f = open('data.json')
    
    try :
        return json.load(f)['@graph'][0]['video']['embedUrl']

    except Exception as e:
        print(" ERROR : ", e)
    
    finally :
        f.close()

