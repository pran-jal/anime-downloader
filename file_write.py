def fileWrite(html_doc) :

    try :
        f = open('data.json', 'a')
        f.write( html_doc )
        f.close()
        return None
        
    except Exception as e:
        return e