import sys
import random
dataTrain = ["zero", "one", "two", "three", "four"]
data = ""
def train():
    file = open('train.txt','r')
    list = []
    for line in file:
        list.append(float(line[0:len(line)-1]))
    print "List " + str(list)
    index = dummySetUpTrain(list)
    print index
    print(dataTrain[index])
    if index == 0:
        data = "bad"
    else:
        data = "great"
    if "great" in data:
        list[index] += 1
    elif "bad" in data:
        list[index] -= 1
    file1 = open('train.txt', 'w')
    for i in range(0, len(list)):
        file1.write(str(list[i])+"\n")

def dummySetUpTrain(list):
    myList = [list[i] for i in range(0, len(list))]
    print myList
    for i in range(1, len(myList)):
        myList[i] += myList[i-1]
    print "MyList " + str(myList)
    number = random.randint(0, myList[len(myList)-1])
    print "Number " + str(number)
    if number <= myList[0]:
        return 0
    if number > myList[-1]:
        return -1
    for i in range(1, len(myList)):
        if number <= myList[i] and number > myList[i-1]:
            return i
train()