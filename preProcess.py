import pandas as pd

def parse(inName,outName):
    with open(str(inName),'r') as f:
        data = f.readlines()
    f.close()
    
    removeList = '''!@#$%^&*()_+-=1234567890{}[]|\';:,<.>?/''' #find all words in alpha order
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


    #write to file
    with open(str(outName),'w') as f:
        for i in wordList:
            f.write(i + ",")
        f.write("classlabel\n")

        for i in freq_data:
            for j in range(len(i)-1):
                f.write(str(i[j]) + ",")
            f.write(str(i[-1]) + "\n")
    f.close()


parse("trainingSet.txt", "preprocessed_train.txt")
parse("testSet.txt", "preprocessed_test.txt")

