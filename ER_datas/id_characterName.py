def LoadCharacter():
    i=1
    strings=[]
    character_name={}
    with open("test2.txt", "r", encoding='utf-8') as f:
        while i<71:
            string=f.readline()
            string=string.replace('┃','\n').replace('/','\n')
            string=string.split('\n')
            character_name[string[2]]=string[3]
            strings+=[string]
            i+=1
    return character_name
# character_name=LoadCharacter()

