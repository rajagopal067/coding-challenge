import sys
import json
import itertools
import datetime

class GraphBuilder:

    graph = {}
    #this will read the tweets input file and write in (timestamp,hashtags) format)
    def readTweets(self,inputFileName):
        inputFile = open(inputFileName,'r')
        tweets = []
        for line in inputFile:
            lineObj = json.loads(line)
            if 'created_at' not in lineObj or 'entities' not in lineObj:
                continue
            tags = lineObj['entities']['hashtags']
            timestamp = lineObj['created_at']
            dateObj = datetime.datetime.strptime(timestamp, '%a %b %d %H:%M:%S +0000 %Y')
            hashtags = self.getHashTags(tags)
            tweets.append((dateObj,hashtags))
        return tweets

    #this will get the hashtags from the entities array
    def getHashTags(self,hashtags):
        tags = []
        for tag in hashtags:
            tag = (tag["text"]).encode("ascii","ignore").lower()
            if len(tag) > 0:
                tags.append(tag)
        return list(set(tags))

    #this will create graph from tweets
    def createGraph(self,tweets,outpuFileName):
        outputFile = open(outputFileName,'w')
        i = 0
        for j in range(len(tweets)):
            while((tweets[j][0] - tweets[i][0]).seconds > 60):

                if len(tweets[i][1]) > 1:
                    edges = itertools.permutations((tweets[i][1]),2)
                    for edge in edges:
                        self.graph[edge[0]].remove(edge[1])
                i+=1

            if len(tweets[j][1]) > 1:
                edges = itertools.permutations((tweets[j][1]),2)
                for edge in edges:
                    if edge[0] in self.graph:
                        self.graph[edge[0]].append(edge[1])
                    else:
                        self.graph[edge[0]] = [edge[1]]

            #Compute the rolling Degree and write to a file
            outputFile.write(self.computeAverageDegree() + "\n")


    def computeAverageDegree(self):
        degree = 0.0
        if len(self.graph) ==0:
            res = format(0.00,'.2f')
        else:
            for node in self.graph:
                degree += len(set((self.graph[node])))
            avg_degree = degree / len(self.graph.keys())
            res = ( "%.2f" % avg_degree)
        return res


if __name__=="__main__":
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]
    graphBuilder = GraphBuilder()

    tweets = graphBuilder.readTweets(inputFileName)
    graphBuilder.createGraph(tweets,outputFileName)

