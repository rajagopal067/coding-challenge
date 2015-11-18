# example of program that calculates the average degree of hashtags
import sys
import json
import itertools
import datetime

class GraphBuilder:
    #this will store all the edges and vertices of the graph
    graph = {}
    curr_tweets = []

    def readTweets(self,inputFileName,outputFileName):
        inputFile = open(inputFileName,'r')
        outputFile = open(outputFileName,'w')
        for line in inputFile:
            lineObj = json.loads(line)
            tags = lineObj['entities']['hashtags']
            timestamp = lineObj['created_at']
            dateObj = datetime.datetime.strptime(timestamp, '%a %b %d %H:%M:%S %z %Y')
            hashtags = self.getHashTags(tags)
            self.addTweet((dateObj,hashtags))
            avgdegree = self.computeAverageDegree()
            outputFile.write(str(avgdegree)+"\n")

    def addTweet(self,tweet):
        #tweet is of format tuple(timestamp,list of hashtags)
        if len(self.curr_tweets) == 0:
            self.curr_tweets.append(tweet)
            self.addHashTagsToGraph(tweet)
            self.computeAverageDegree()
            return
        oldest_tweet = self.curr_tweets[0]

        if (tweet[0] - oldest_tweet[0]).seconds < 60:
            self.curr_tweets.append(tweet)
            self.addHashTagsToGraph(tweet)
        else:
            j=0
            while j < len(self.curr_tweets) and (tweet[0] - self.curr_tweets[j][0]).seconds > 60:
                hashtags = self.curr_tweets[j][1]
                edges = itertools.permutations(hashtags,2)
                for edge in edges:
                    self.graph[edge[0]].remove(edge[1])
                j +=1
            if j !=0:
                self.curr_tweets = self.curr_tweets[j:]

    def addHashTagsToGraph(self,tweet):
        hashtags = tweet[1]
        edges = itertools.permutations(hashtags,2)
        for edge in edges:
            if edge[0] not in self.graph:
                self.graph[edge[0]] = [edge[1]]
            else:
                self.graph[edge[0]].append(edge[1])


#this will compute the average degree of all the vertices in the graph.
    def computeAverageDegree(self):
        sum = 0.00
        for key in self.graph.keys():
            sum += len(set(self.graph[key]))

        if sum == 0:
            return '0.00'
        avg_degree = sum / len(self.graph.keys())
        avg_degree = ( "%.2f" % avg_degree)
        return avg_degree


    def getHashTags(self,hashtags):
        tags = []
        for tag in hashtags:
            if len(tag['text']) > 0:
                tags.append(tag['text'].lower())
        return list(set(tags))


if __name__ == '__main__':
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]
    graphbuilder = GraphBuilder()
    graphbuilder.readTweets(inputFileName,outputFileName)