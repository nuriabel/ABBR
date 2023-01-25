#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import io
import csv

import sys
reload(sys)
sys.setdefaultencoding('utf8')


#General Comments
# I couldn't use a python library to process the XML files, as they are not correctly formatted:
# ExpatError: junk after document element: line 2, column 0
# In order to prevent this error I parse the file without using any XML library

# Example of how to call the script: 
# python FLtoBRAT.py /Users/miquelcornudella/Documents/IULA/tasques/FLtoBRAT/input-csv-lists/acro.csv /Users/miquelcornudella/Documents/IULA/tasques/FLtoBRAT/input-csv-lists/abbr.csv /Users/miquelcornudella/Documents/IULA/tasques/FLtoBRAT/input-csv-lists/symbol.csv /Users/miquelcornudella/Documents/IULA/tasques/FLtoBRAT/negation_iac_1_corr.xml /Users/miquelcornudella/Documents/IULA/tasques/FLtoBRAT/output-files/output1.ann

# Initialize the accronym dictionary 
accroDict = {}

# Initialize the abbreviation dictionary 
abbrevDict = {}

# Initialize the symbol dictionary 
symbolDict = {}

def fillAccroDict(accroDict, accroCvsFile):
    # open the accroCvsFile file and read it using ";" as delimiter 
    with io.open(accroCvsFile, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=';')
        # each line is an array
        for row in reader:
            i = 2
            while(i < len(row) -1):
                # for every position different to row[0]
                # if it contains a term, we add it to the dictionary
                if row[i].encode('utf-8') != '':
                    if row[1].encode('utf-8') in accroDict:
                        accroDict[row[1].encode('utf-8')].append(row[i].encode('utf-8'))
                    else:
                        accroDict[row[1].encode('utf-8')] = [row[i].encode('utf-8')]
                    #print "We add " + row[0] + "\t" + row[i]
                    i += 1
                else: # otherwise, break the while
                    break

def fillAbbrevDict(abbrevDict, abbrevCvsFile):
    # open the abbrevCvsFile file and read it using ";" as delimiter 
    with io.open(abbrevCvsFile, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=';')
        # each line is an array
        for row in reader:
            i = 2
            while(i < len(row) -1):
                # for every position different to row[0]
                # if it contains a term, we add it to the dictionary
                if row[i].encode('utf-8') != '':
                    if row[1].encode('utf-8') in abbrevDict:
                        abbrevDict[row[1].encode('utf-8')].append(row[i].encode('utf-8'))
                    else:
                        abbrevDict[row[1].encode('utf-8')] = [row[i].encode('utf-8')]
                    #print "We add " + row[0] + "\t" + row[i]
                    i += 1
                else: # otherwise, break the while
                    break

def fillSymbolDict(symbolDict, symbolCvsFile):
    # open the symbolCvsFile file and read it using ";" as delimiter 
    with io.open(symbolCvsFile, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=';')
        # each line is an array
        for row in reader:
            i = 2
            while(i < len(row) -1):
                # for every position different to row[0]
                # if it contains a term, we add it to the dictionary
                if row[i].encode('utf-8') != '':
                    if row[1].encode('utf-8') in symbolDict:
                        symbolDict[row[1].encode('utf-8')].append(row[i].encode('utf-8'))
                    else:
                        symbolDict[row[1].encode('utf-8')] = [row[i].encode('utf-8')]
                    #print "We add " + row[0] + "\t" + row[i]
                    i += 1
                else: # otherwise, break the while
                    break
                
def generateOutputFile(outputFile, inputXMLFreelingFile):
    # initialize function counters
    num = 1
    numterm = 1
    for line in inputXMLFreelingFile:
        #print line
        if (line.find("<token ") > -1):
            # split line using "\""
            lineSplit = line.split("\"")
            begin = lineSplit[3] # value for begin
            end = lineSplit[5] # value for end
            form = lineSplit[7].encode('utf-8') # value for form (must be read in 'utf-8')
            
            # 1.- we check if the form is in the acronym dictionary
            if form in accroDict.keys(): # if so
                class_value = "ACRO" # we specify the class_value to "ACRO" 
                # write the corresponding line to the output file 
                outputFile.write("T" + str(num) + "\t" + class_value + " " + begin + " " + end + "\t" + form + "\n")
                # we collect the terms associated to the acronym
                terms = ''
                termNumberForAcronym = 1
                for term in accroDict.get(form):
                    terms += term
                    if termNumberForAcronym < len(accroDict[form]):
                        terms += ", "
                    termNumberForAcronym +=1
                # write the associated terms to the output file
                outputFile.write(unicode("#" + str(numterm) + "\t" + "AnnotatorNotes" + " " + "T" + str(num) + "\t" +  terms + "\n"))
                # update function counters
                num += 1
                numterm += 1
                
            # 2.- we check if the form is in the abbreviation dictionary
            if form in abbrevDict.keys(): #if si
                class_value = "ABBR" # we specify the class_value to "ABBR"
                # write the corresponding line to the output file
                outputFile.write("T" + str(num) + "\t" + class_value + " " + begin + " " + end + "\t" + form + "\n")
                # we collect the terms associated to the abbreviation
                terms = ''
                termNumberForAbbreviation = 1
                for term in abbrevDict.get(form):
                    terms += term
                    if termNumberForAbbreviation < len(abbrevDict[form]):
                        terms += ", "
                    termNumberForAbbreviation +=1
                # write the associated terms to the output file
                outputFile.write(unicode("#" + str(numterm) + "\t" + "AnnotatorNotes" + " " + "T" + str(num) + "\t" +  terms + "\n"))
                # update function counters
                num += 1
                numterm += 1
                
            # 3.- we check if the form is in the symbol dictionary
            if form in symbolDict.keys(): #if si
                class_value = "SYMB" # we specify the class_value to "SYMBOL" NB: SYMB
                # write the corresponding line to the output file
                outputFile.write("T" + str(num) + "\t" + class_value + " " + begin + " " + end + "\t" + form + "\n")
                # we collect the terms associated to the abbreviation
                terms = ''
                termNumberForSymbol = 1
                for term in symbolDict.get(form):
                    terms += term
                    if termNumberForSymbol < len(symbolDict[form]):
                        terms += ", "
                    termNumberForSymbol +=1
                # write the associated terms to the output file
                outputFile.write(unicode("#" + str(numterm) + "\t" + "AnnotatorNotes" + " " + "T" + str(num) + "\t" +  terms + "\n"))
                # update function counters
                num += 1
                numterm += 1
        
def main():
     if (len(sys.argv) != 6):
         print "Error, we need the following arguments (in the same order): accro-cvs-file abbrev-cvs-file symbol-cvs-file xml-Freeling-file output-file"
         print "Example: python FLtoBRAT.py accro-cvs-file abbrev-cvs-file symbol-cvs-file xml-Freeling-file output-file"
         sys.exit(1)
     
     # open input files. First the CVS files
     accroCvsFile = sys.argv[1]
     abbrevCvsFile = sys.argv[2]
     symbolCvsFile = sys.argv[3]
     # then the xml file generated by freeling...
     inputXMLFreelingFile = io.open(sys.argv[4], 'r', encoding='utf8')
     # and finally open the outputfile
     outputFile = io.open(sys.argv[5], 'w', encoding='utf8')
     
     print "Thanks for using the FLtoBRAT.py script! \n"
     print "IMPORTANT INFORMATION"
     print "This script assumes that all input files are encoded in \'utf-8\'"
     print "Please ensure that this is the case: otherwise the output file will not be correctly encoded \n"
     
     print "Starting the conversion from FL to BRAT file \n"
     
     print "Step 1: Load the list of acronyms into a dictionary"
     fillAccroDict(accroDict, accroCvsFile)
     print "Step 1 completed. Acronyms correctly loaded\n"
     
     #for key, value in accroDict.iteritems() :
     #    print key, value
     
     print "Step 2: Load the list of abbreviations into a dictionary"
     fillAbbrevDict(abbrevDict, abbrevCvsFile)
     print "Step 2 completed. Abbreviations correctly loaded\n"
     
     #for key, value in abbrevDict.iteritems() :
     #    print key, value
     
     print "Step 3: Load the list of symbols into a dictionary"
     fillSymbolDict(symbolDict, symbolCvsFile)
     print "Step 2 completed. Symbols correctly loaded\n"
     
     #for key, value in symbolDict.iteritems() :
     #    print key, value
     
     print "Step 4: generating the output file..."
     generateOutputFile(outputFile, inputXMLFreelingFile)
     print "Step 4 completed. Output file generated"
     
     print "Bye"
    

#call main    
main()
