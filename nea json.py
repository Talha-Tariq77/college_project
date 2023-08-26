import json
Lst = ['a','b',1,2]
Dct = {'name':'James','age':34,'Scores':{'test1':50,'test2':65,'test3':45}}
Lst_string = json.dumps(Lst)
Dct_string = json.dumps(Dct)
print(type(Lst),type(Dct))
print(Lst_string,type(Lst_string))
print(Dct_string,type(Dct_string))

highscores = '{"James":600,"Jill":590,"Les":550}'
hscores = json.loads(highscores)
# print(highscores[“James”] #Crashes
print(hscores["James"])

