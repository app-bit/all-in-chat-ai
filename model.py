import os 

def get_stream_of_data():
    with open(f'{os.getcwd()}/all_in_transcript.txt','r') as f:
        data = f.readlines()
    stream=[]
    for message in data:
        if len(message.split(':'))>1:
            name=message.split(':')[0]
            if name=='subject':
                name='system'
            elif name in ['Chamath','Friedberg', 'Sacks']:
                name='user'
            elif name=='Jason':
                name='assistant'
            mes=message.split(':')[1].strip('\n')
            stream.append([name,mes])
    return stream

def arrange_chat(ls):
    d={}
    res=[]
    for i in range(len(ls)-1):
    #handling case where current key is not in dict and next item is different 
        if ls[i][0] not in d and ls[i+1][0]!=ls[i][0]:
            #if next key is different 
            d[ls[i][0]]=[ls[i][1]] 
            res.append((ls[i][0],' '.join(d[ls[i][0]])))
            del d[ls[i][0]]

        elif ls[i][0] not in d and ls[i+1][0]==ls[i][0]:
            d[ls[i][0]]=[ls[i][1]]
        elif ls[i][0] in d and ls[i+1][0]!=ls[i][0]:
            d[ls[i][0]].append(ls[i][1])
            res.append((ls[i][0],' '.join(d[ls[i][0]])))
            del d[ls[i][0]]
        else:
            d[ls[i][0]].append(ls[i][1])
    if ls[-1][0]==ls[-2][0]:
        #manipulate the last value in res
        if d[ls[i][0]]:
            d[ls[i][0]].append(ls[-1][1])
            res.append((ls[i][0],(' '.join(d[ls[i][0]]))))
    else:
        res.append((ls[-1][0],ls[-1][1]))
    
    return res

