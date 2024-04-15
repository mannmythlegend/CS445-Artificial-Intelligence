import csv

# open file
with open('cleanData.csv', 'r') as file:
    reader = csv.reader(file)

    currentRow = 0
    testRows = []
    trainRows = []

    # i am personally doing 80% train, and 20% test
    for row in reader:
    
        # test every fifth row
        if currentRow % 5 == 0:
            testRows.append(row)
        # train rest
        else:
            trainRows.append(row)
        
        currentRow += 1

threshold = 5.0
initWeight = 1.0
step = 0.1
rounds = 5

#find location of answer within a given row
answer = len(trainRows[1])-1
perceptrons = []

# starting the trains
for i in range(rounds):
    if i==0:
        for j in range(len(trainRows[1])-1):
            perceptrons.append(initWeight)

    newPerceptrons = perceptrons.copy()

    for row in trainRows:
        output = 0
        ans = int(row[answer])

        for i in range(len(row)-1):
            output = output + (int(row[i]) * newPerceptrons[i])

        if output > threshold:
            predict = 1
        else:
            predict = 0

        if predict == ans:
            continue

        # wrong prediction case
        elif predict < ans: # if we underestimated
            for j in range(len(row)-1):
                if int(row[j]) == 1:
                    newVal = newPerceptrons[j] + step
                    newPerceptrons[j] = round(newVal,2)
        else: # overestimated
            for j in range(len(row)-1):
                if int(row[j]) == 1:
                    newVal = newPerceptrons[j] - step
                    newPerceptrons[j] = round(newVal,2)
            
    #check convergence
    if(newPerceptrons == perceptrons):
        break
    else:
        perceptrons = newPerceptrons.copy()

# starting test
predPos = 0

for test in testRows:
    testOutput = 0
    testAns = int(test[answer])

    for n in range(len(test)-1):
        testOutput = testOutput + (int(test[n]) * perceptrons[n])

    if testOutput > threshold:
        predict = 1
    else:
        predict = 0

    if predict == testAns:
        predPos += 1
    else:
        continue

# write answers to weights.txt
with open('weights.txt', 'w') as file:
    file.write(str(threshold))
    file.write('\n')

    index = 1
    for p in perceptrons:
        file.write(str(index))
        file.write(". ")
        file.write(str(p))
        file.write('\n')
        index +=1