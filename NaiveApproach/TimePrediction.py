from __future__ import division
import json
import string
from pprint import pprint
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
import string

# Openning train data
with open('tags.json') as data_file:    
    tagData = json.load(data_file)

# Number of train data found
size_jsonTag = len(tagData["tags"]["row"])

with open('train.json') as data_file:    
    trainData = json.load(data_file)

# Number of train data found
size_jsonTrain = len(trainData["posts"]["row"])

with open('test.json') as data_file:    
    testData = json.load(data_file)

# Number of train data found
size_jsonTest = len(testData["posts"]["row"])

acc = 0
squareSum = 0

for tagTime in tagData["tags"]["row"]:

	predicted_string = tagTime.get("-TagName")
	
	times = ["0:01 to 4:00 UTC", "4:01 to 8:00 UTC", "8:00 to 12:00 UTC", "12:01 to 16:00 UTC", "16:01 to 20:00 UTC", "20:01 to 0:00 UTC"]
	distances = [0]*6

	for post in trainData["posts"]["row"]:
		tag = post.get("Tags")
		if tag.find(predicted_string) != -1:
			if post.get("AnswerCount") != 0:
				ind = post.get("creationTime")
				distances[ind-1] = distances[ind-1] + 1
				post.get("creationTime")

	trainTime = times[distances.index(max(distances))]
	trainCode = distances.index(max(distances))
	distances = [0]*6

	for post in testData["posts"]["row"]:
		tag = post.get("Tags")
		if tag.find(predicted_string) != -1:
			if post.get("AnswerCount") != 0:
				ind = post.get("creationTime")
				distances[ind-1] = distances[ind-1] + 1
				post.get("creationTime")

	testTime = times[distances.index(max(distances))]
	testCode = distances.index(max(distances))
	if testTime == trainTime:
		acc += 1
	else:
		squareSum = (testCode - trainCode)**2

print "Calculating the Mean Square Error for the Time Predictions for each tag"
print "Mean Square Error - ",squareSum/size_jsonTag
