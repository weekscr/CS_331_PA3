import pandas as pd
import math
import numpy as np
from datetime import datetime

def parse(inName): #create wordList in alpha order
    with open(str(inName),'r') as f:
        data = f.readlines()
    f.close()
    
    removeList = '''!@#$%^&*()_+-=1234567890{}[]|\';:,<.>?/'''
    wordList = []
    
    for i in data:
        strpd = ""
        for j in i:
           if j not in removeList:
               strpd = strpd + j

        strpd = strpd.split()
        for j in strpd:
            low = j.lower()
            if low not in wordList:
                wordList.append(low)
    wordList.sort()

    return wordList



def preProcess(inName, wordList): #preProcess cases from fileName using existing wordlist
    with open(str(inName),'r') as f:
        data = f.readlines()
    f.close()
    removeList = '''!@#$%^&*()_+-=1234567890{}[]|\';:,<.>?/'''
    
    freq_data = []                        #go through reviews and note words and 1 vs 0
    for i in data:
        strpd = ""
        for j in i:
           if j not in removeList:
               strpd = strpd + j

        strpd = [x.lower() for x in strpd.split()]

        wordDict = [0]*(len(wordList)+1) 
        for j in range(len(wordList)):
            if wordList[j] in strpd:
                wordDict[j]=1

        wordDict[-1] = int(i.split()[-1])
        
        freq_data.append(wordDict)

    return(freq_data)





def train(fileName):
    
    wL = parse(fileName)
    fD = preProcess(fileName,wL)
    
    countPos = 0 #calculate P(pos)
    for i in fD:
        if i[-1]:
            countPos += 1
    probPos = countPos/len(fD)

    #conditional probabilities for each word: [P(word=1|review=pos), P(word=1|review=neg), P(word=0|review=pos), P(word=0|review=neg)]
    condProbs = []
    for i in range(len(wL)-1):  
        condCountPos = 0
        condCountNeg = 0
        
        for j in fD:
            if j[i] and j[-1]:
                condCountPos += 1
            elif j[i] and not j[-1]:
                condCountNeg += 1
                                                                                                       
        condProbs.append([((condCountPos+1)/(countPos+2)), ((condCountNeg+1)/((len(fD)-countPos)+2)), 1-((condCountPos+1)/(countPos+2)), 1-((condCountNeg+1)/((len(fD)-countPos)+2))])

    return condProbs, probPos, wL




def test(condProbs,probPos,set2Test,setTrainedOn,wL):
    fD = preProcess(str(set2Test),wL)
    correct = 0
    
    for i in fD: # for each test case

        #calculate prob positive
        logSum = 0
        for j in range(len(condProbs)-1):
            if i[j]: #if word is present
                logSum += math.log(condProbs[j][0]) #word present given positive
            else: #if word absent
                logSum += math.log(condProbs[j][2]) #word not present given positive
        Pos = logSum + math.log(probPos)

        #calculate prob negative
        logSum = 0
        for j in range(len(condProbs)-1):
            if i[j]: #if word present
                logSum += math.log(condProbs[j][1]) #word present given negative
            else: #if word absent
                logSum += math.log(condProbs[j][3]) #word not present given negative
        Neg = logSum + math.log(1-probPos)

        #print(Neg,Pos,np.argmax([Neg,Pos]))
        
        if np.argmax([Neg,Pos]) == i[-1]: #check if prediction correct
            correct += 1


    print("Accuracy is:",correct*100/len(fD),"%")    
    with open("results.txt",'a') as f:
        f.write("[" + str(datetime.now().strftime("%H:%M:%S")) + "]: ")
        f.write(str("Accuracy is: "))
        f.write(str(correct*100/len(fD)))
        f.write("%\n")
        f.write("Trained on " + str(setTrainedOn) + "\nTested on " + str(set2Test) + "\n\n")
    f.close()







trainFile = input("please enter the name of the file to train on: ")
try:
    #output trained probabilities matrix
    probsList, probPos, wL = train(trainFile)
    
    testFile = input("please enter the name of the file to test on: ")
    try:
        #test using probabilities from training (probability list, porbability of a positive review, set to test on, set trained on, existing wordList)
        #results in results.txt
        test(probsList, probPos, testFile, trainFile, wL)
    except:
        print("An error occurred. Please try again.")

except:
    print("An error occurred. Please try again.")






