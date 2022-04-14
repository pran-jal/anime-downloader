
def generator(url, total_episodes):

    url = url[::-1]
    end = None
    for i in range(len(url)) :
        if url[i] == '-' :
            if url[:i:][::-1] == 'uncen/':
                end = '-uncen/'
            else:
                if end != '-uncen/':
                    end = '/'
                break 
    url = url[i::][::-1]
    urls = []
    for i in range(1, total_episodes+1):
        urls.append( url+str(i)+end )
    return urls

if __name__ == '__main__':
    print(generator(input(), 12))