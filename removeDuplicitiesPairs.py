import os.path
from itertools import groupby
import string
import sys
import argparse

parser = argparse.ArgumentParser(description='Counts duplicate pairs for a file with interlaced pairs and creates a file without duplicate pairs.')
parser.add_argument('-f', '--filename',
                   help='insert filename', required = True)
parser.add_argument('-r', '--resDir',
                   help='insert directory for results', required = True)
args = vars(parser.parse_args())

inname = args['filename']

inname = os.path.normpath(inname)
pathList =  inname.split(os.sep)
fileName = pathList[len(pathList) - 1]
fileNameSplit = fileName.split('.')
infix = fileNameSplit[0]
suffix = fileNameSplit[1]

resDir = args['resDir']
if not os.path.isdir(resDir):
    os.mkdir(resDir)
    
withoutDupName = resDir + os.sep + infix + '_withoutDuplicities.' + suffix
resultsName  = resDir + os.sep + infix + '_sumOfRes.txt' 

ishead = lambda x: x.startswith('>')
seqDict = {}
numOfDuplTotal = 0
numOfDuplGroups = 0
numOfLine = 0
isOne = False
seq1=''
seq2=''
head1 = ''
head2 = ''
with open(inname) as handle:
    head = None
    for h, lines in groupby(handle, ishead):
        numOfLine += 1
        if h:
            head = next(lines)
            if head.endswith('1\n') and not isOne:
                head1 = head
                isOne = True
            elif head.endswith('2\n') and isOne:
                head2 = head
                isOne = False
            else:
                print('error ', numOfLine, ' ', head)
        else:
            seq = next(lines) 
            seq = seq.strip() 
            if isOne:
                seq1 = seq
            else:
                seq2 = seq
                seq12 = seq1 + seq2
                seq21 = seq2 + seq1
                if seq12 in seqDict:
                    #12 is duplicate
                    numOfDuplTotal += 1
                    if seqDict[seq12] == 1:
                        numOfDuplTotal += 1
                        numOfDuplGroups +=1
                    seqDict[seq12] += 1
                elif seq21 in seqDict:
                    #21 is duplicate)
                    numOfDuplTotal += 1
                    if seqDict[seq21] == 1:
                        numOfDuplTotal += 1
                        numOfDuplGroups +=1
                    seqDict[seq21] +=1        
                else:
                    #first occurence
                    seqDict[seq12] = 1
                    with open(withoutDupName, 'a') as withoutDup:
                        withoutDup.write('%s%s\n%s%s\n' % (head1, seq1, head2, seq2))
                        
print ('numOfDuplTotal:', numOfDuplTotal, 'numOfDuplGroups:', numOfDuplGroups)
with open(resultsName, 'a') as resFile:
    resFile.write('numOfDuplTotal: %d numOfDuplGroups: %d' % (numOfDuplTotal, numOfDuplGroups))




