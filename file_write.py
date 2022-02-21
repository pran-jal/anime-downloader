def fileWrite(html_doc) :

    try :
        
        f = open('data.json', 'a')
        f2 = open('data.txt', 'a')

        f.write( html_doc )
        f2.write( html_doc )

        f.close()
        f2.close()

        return None

    except Exception as e:
        return e