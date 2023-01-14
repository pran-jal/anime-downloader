import requests as r
RAPID_API = "https://rapid-cloud.co/ajax/embed-6/getSources?id="

def get(id):
    data =  r.get(RAPID_API + id).json()

    sources = data["sources"]
    sources_backup = data["sourcesBackup"]
    sub = [i['file'] for i in data['tracks'] if i.get('label') == 'English'][0]

    print(sources, sources_backup, sub)




print(get("7ppphq8wiFCk"))