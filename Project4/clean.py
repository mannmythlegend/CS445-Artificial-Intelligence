import csv

# open file
with open('alcoholism_traintest.csv', 'r') as file:

    reader = csv.reader(file)

    
    cleanData = [] # holds all the clean rows

    # index var
    i=0

    # loop over every row
    for row in reader:

        cleanRow = [] # will hold one row at a time that is cleaned

        # skip first column for each row
        if(i==0):
            i=1
            continue

        # make sure all values are filled in row
        if not all(row):
            continue

        # remove all rows with -999 as i consider this weird data
        if "-999" in row:
            del row
            continue
        
        # start clean
        for value in row[1:]:
        
            # translate value to int so we can observe
            value = int(value)
            
            if value==1 or value==-1 or value==0:
                cleanRow.append(value)
            elif value<=3 and value >=0:
                cleanRow.append(0)
            elif value >= 99 or value <= -2:
                cleanRow.append(-1)
            else:
                cleanRow.append(1)

        # add the cleaned row to the array
        cleanData.append(cleanRow)

# put cleaned csv in a new csv
with open('cleanData.csv', 'w', newline='') as file:

    writer = csv.writer(file)
    for row in cleanData:
        writer.writerow(row)