#!/usr/bin/env python

import os, sys, json
# change paths for source and target as needed
sourcePath = '/home/my-user/apps/caliper/test_source/'
targetPath = '/home/my-user/apps/caliper/test_target/'

for inFileName in os.listdir(sourcePath):
    sourceFile = sourcePath + inFileName
    targetFile = targetPath + 'fixed_' + inFileName

    # open source and fix data
    with open(sourceFile) as inFile:
        try:
            fixedData = inFile.read()[1:-1].replace('}{','} \n{')
        except:
            break
    # open target and write fixed data
    with open(targetFile, 'a') as outFile:
        try:
            outFile.write('{' + fixedData + '}')
        except:
            break
    # remove source file after processing the target
    try:
        os.remove(sourceFile)
    except:
        break
    print(inFileName + ' has been processed')
