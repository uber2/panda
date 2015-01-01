import data
import json

test1 =[{"make":"Mercedes","model":"B-Class"},{"make":"Opel","model":"Insignia"}]
data = data.leaf("test.json","w")

data.save(test1)
test2 = data.load()
print "test2", test2, "\n"
print test2[1]
print (type(test2[1]))
