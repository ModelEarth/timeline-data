## Uses right column "y" set to 1 for rows that increase by 2% in insubsequent year.

# To run: python automate.py zcta.SQL.txt
import sys
import argparse
import os
import subprocess
import re
def writeNewSQL(sqlFile):
    yearList=['2012','2013','2014','2015','2016','2017']
    outputFiles=[]
    for i in range(5):
        outSQLFile=os.path.abspath(os.path.join("./","zcta_"+yearList[i]+".SQL.txt"))
        outputFiles.append(outSQLFile)
    for k in range(0,5):
        with open(outputFiles[k],'w') as outFH:
            with open(sqlFile,'r')as fh:
                allLines=fh.readlines()
                for i in range(34):
                    outFH.write(allLines[i])#stop at .modecsv
                allLines[35]=os.path.join(".import input/",yearList[k],yearList[k])+"_zcta_industries_sm.csv industries"+"\n"
                outFH.write(allLines[35]+"\n")
                for i in range(36,61):
                    outFH.write(allLines[i])
                
                # Feb 2024 - We can reactivate if we find poverty folder. It was not in community-forecasting/data
                allLines[61]=os.path.join(".import input/poverty/output/",yearList[k]+"_zcta_poverty.csv poverty")
                outFH.write(allLines[61]+ "\n")
                for i in range(62,77):
                    outFH.write(allLines[i])
                allLines[77]=os.path.join(".import input/poverty/output/",yearList[k-1]+"_zcta_poverty.csv povertyPriorYear1")
                outFH.write(allLines[77] +"\n")
                for i in range(78,93):
                    outFH.write(allLines[i])
                allLines[93]=os.path.join(".import input/poverty/output/",yearList[k+1]+"_zcta_poverty.csv povertyNextYear")
                outFH.write(allLines[93] +"\n")
                for i in range(94,158):
                    outFH.write(allLines[i])

                allLines[159]=os.path.join(".output output/",yearList[k],yearList[k]+ "_zcta_sm.csv") + "\nselect * from zcta_output;"
                outFH.write(allLines[159]+"\n") 
                
                for i in range(160,166):
                    outFH.write(allLines[i])
def main():
    inFile=sys.argv[1] # zcta.SQL.txt -- sends to this file.
    
    writeNewSQL(inFile)
    yearList=['2012','2013','2014','2015','2016','2017']
    sqlFiles=[]
    outDir="output/"
    for i in range(0,5):
        if not os.path.exists(os.path.join(outDir,yearList[i])):
            os.makedirs(os.path.join(outDir,yearList[i]))
        outSQLFile=os.path.abspath(os.path.join("./","zcta_"+yearList[i]+".SQL.txt"))
        outSQLFile="zcta_"+yearList[i]+".SQL.txt"
        sqlFiles.append(outSQLFile)
    #print(sqlFiles)
    for sql in sqlFiles:
        commandLine="sqlite3 zcta.db < "+sql +"> zcta.OUT.txt"
        print(commandLine)
        #subprocess.call(["sqlite3","zcta.db < "+sql +" > zcta.OUT.txt"]) #cannot do this in python
        
    
if __name__ == "__main__":
    main()
