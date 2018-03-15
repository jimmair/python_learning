# List are []
# Tuple are ()
# Tuple are like lists but cannot be changed (immutable)

list1 = [10, 20, 30, 40, 50]
print (list1)
print (type(list1))
print (list1[0])

list2 = ["spam", "bungee", "swallow"]
print (list2)
print (type(list2))


tuple1 = (2, 4, 6, 8)
tuple1 = 2, 4, 6, 8
print (tuple1)
print (type(tuple1))


tuple2 = ("two", "four", "six", "eight",10)
print (tuple2)
print (type(tuple2))
print (type(tuple2[1]))
print (type(tuple2[4]))


tuple3 = ("cheese", "queso"), ("red", "rojo"), ("school", "escuela")
print (tuple3)
print (type(tuple3))
print (type(tuple3[0]))
print (type(tuple3[0][0]))


list3 = [("cheese", "queso"), ("red", "rojo"), ("school", "escuela")]
print (list3)
print (type(list3))
print (list3[0])
print (type(list3[0]))
print (type(list3[0][0]))

not_tuple = (2)
print (type(not_tuple))


