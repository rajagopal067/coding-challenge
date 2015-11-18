# example of program that calculates the number of tweets cleaned
import sys
import json
import codecs
import re


class Cleaner:

    count = 0

    def clean_tweets(self,inputFileName,outputFileName):
        inputFile = open(inputFileName,'r')
        outputFile = open(outputFileName,'w')
        for line in inputFile:
            lineObj = json.loads(line)
            if 'created_at' in lineObj and 'text' in lineObj:
                timestamp = lineObj['created_at']
                text = lineObj['text']
                cleaned_tweet = self.get_cleantext(text)
                outputFile.write(cleaned_tweet + " (timestamp: "+timestamp+ ")\n")

        outputFile.write("\n" + str(self.count) + " tweets contain unicode")


    def isAscii(self,c):
        try:
            return ord(c) <= 127
        except:
            return False

    def get_cleantext(self,text):

        containsUnicode = False
        #remove \n and \t replace with whitespace
        text = text.replace('\n',' ').replace('\t',' ')
        clean_text = ""
        for c in text:
            if self.isAscii(c):
                clean_text += str(c)
            else:
                containsUnicode = True

        if containsUnicode == True:
            self.count += 1

        return clean_text





if __name__ == '__main__':
    inputFilename = sys.argv[1]
    outputFilename = sys.argv[2]

    cleaner = Cleaner()
    cleaner.clean_tweets(inputFilename,outputFilename)