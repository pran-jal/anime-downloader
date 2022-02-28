import requests as r
import servers

def download_episodes(url):

    details = servers.embedUrl(url)
    total_no_episodes = details[1].pop()
    servers_list = details[0]
    print(total_no_episodes)
    print(servers_list)
    try :
        url = servers_list[0][:-2:]
        for i in range(1, 1+int(total_no_episodes, 10)):
            new_url = url +str(i)+'/'
            print(new_url)
    except:
        print("vidstream not working")


download_episodes(input())