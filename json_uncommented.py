import json
import operator

json_file_path = "highscore.txt"
fp = open(json_file_path,"r")
line = fp.readline()
data = json.loads(line)  # converts json string into list of lists

sorted_x = sorted(data.items(), key=operator.itemgetter(1))  # sorts the dict
sorted_x.append(("Joan", 540))
print(sorted_x)
jsn = json.dumps(dict(sorted_x))
print(jsn)
fp.close()

fp = open(json_file_path, "w")
fp.write(jsn+"\n")
fp.close()








