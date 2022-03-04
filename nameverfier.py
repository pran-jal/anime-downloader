def nameverifier(name):
    for i in name:
        if i not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_.' :
            j = name.find(i)
            if (name[j-1] == '_' and j>0) or j==0:
                name = name[:j:]+name[j+1::]
            else :
                name = name[:j:]+'_'+name[j+1::]
    return name