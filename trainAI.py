import mainFunction
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import sys
#training part
global samples
global responses

samples = []
responses = []
print samples
print responses
def train():
    fileSample = open('./ml_data/samples.txt', 'a')
    fileResponse = open('./ml_data/responses.txt', 'a')
    while True:
        try:
            while True:
                print "Getting data"
                global samples
                dataIn = mainFunction.recordAudio()
                if len(dataIn) != 0:
                    break
            #samples.append(dataIn)
            fileSample.write(dataIn + "\n")
            while True:
                print "Getting response"
                global responses
                dataRes = mainFunction.recordAudio()
                if len(dataRes) != 0:
                    break
            #responses.append(dataRes)
            fileResponse.write(dataRes + "\n")
            print "Continue?"
            data = mainFunction.recordAudio()
            if "stop" in data or "top" in data:
                print "Saving"
                #samples = np.array(samples)
                #samples.reshape((samples.size,))
                #np.savetxt('./ml_data/samples.data',samples.shape)
                #fileSample.write(str(samples))
                #responses = np.array(responses)
                #responses.reshape((responses.size,))
                #np.savetxt('./ml_data/responses.data',responses.shape)
                #fileResponse.write(str(responses))
                

                break
        except (KeyboardInterrupt, EOFError, SystemExit):
            print "Saving"
            np.savetxt('./ml_data/samples.txt',samples)
            np.savetxt('./ml_data/responses.txt',responses)
            break
#test part
def test():
    fileSample = open('./ml_data/samples.txt', 'r')
    fileResponse = open('./ml_data/responses.txt', 'r')
    for line in fileSample:
        samples.append(line)
    for line in fileResponse:
        responses.append(line)
    #samples = np.loadtxt('./ml_data/samples.data', np.string_)
    #responses = np.loadtxt('./ml_data/responses.data', np.string_)
    #print samples
    #samples.reshape(samples.size,)
    #responses.reshape(responses.size,)
    #print samples[0]
    while True:
        try:
            while True:
                data = mainFunction.recordAudio()
                if len(data) != 0:
                    break
            min = float("inf")
            res = ""
            for i in range(0, len(samples)):
                #print samples[i] + " "  str(dist(data,samples[i]))
                if dist(data, samples[i]) <= min:
                    res = responses[i]
                    min = dist(data, samples[i])
            mainFunction.speak(res)
        except (KeyboardInterrupt, EOFError, SystemExit):
            break
def dist(data, samp):
    dataArray = data.split(" ")
    sampArray = samp.split(" ")
    count = 9999
    for dat in dataArray:
        if dat in sampArray:
            count -= 1
    return count
    # model = cv2.KNearest()
    # model.train(samples,responses)
    # knn = KNeighborsClassifier()
    # knn.fit(samples, responses)
    # while True:
    #     data = mainFunction.recordAudio()
    #     print knn.predict(data)

#train()
test()