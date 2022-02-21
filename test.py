try :
    f = open('data.json')
except :
    print(Exception.__context__)
    # if Exception.__class__.__name__ == 'FileNotFoundError' :
    #     print("yes")
    # else :
    #     print('NO')
