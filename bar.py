# while(1):
#     time.sleep(0.1)
#     print('\r .    \r', end='\r')
#     time.sleep(0.1)
#     print('\r ...  \r', end='\r')
#     time.sleep(0.1)
#     print('\r .....\r', end='\r')
#     time.sleep(0.1)    
#     print('\r ...  \r', end='\r')
#     time.sleep(0.1)    
#     print('\r .    \r', end='\r')
#     time.sleep(0.1)    
#     print('\r      \r', end='\r')

# while(1):
#     print('\r | \r', end='\r')
#     time.sleep(0.1)
#     print('\r / \r', end='\r')
#     time.sleep(0.1)
#     # print('\r ̷ \r', end='\r')
#     # time.sleep(0.1)
#     print('\r  ̶ \r', end='\r')
#     time.sleep(0.1)
#     print('\r \ \r', end='\r')
#     time.sleep(0.1)
#     print('\r | \r', end='\r')


for progress in range(101):
    p = 'Progress :'
    s = 'Completed'
    fill = chr(9608)
    filled = int(float(progress))
    bar = fill*filled+'-'*(100-filled)
    print(f"{p} {chr(9616)} {bar} | {progress}% {s}\r", end='\r')