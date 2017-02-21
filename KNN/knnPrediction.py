from __future__ import division
import json
import string
from pprint import pprint
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
import string
import numpy
import math

# Function that takes the Stackoverflow post and cleans it.
def cleanPost(post):
	
	# Removes encoded html tags
	post = post.replace('&lt;','<')
	post = post.replace('&gt;','>')

	# Removes HTML tags
	soup = BeautifulSoup(post, 'html.parser')
	post = soup.get_text()

	# To lower case
	post = post.lower()

	# Removes punctuation
	exclude = set(string.punctuation)
	post = ''.join(ch for ch in post if ch not in exclude)

	# Removes stop words
	stop = set(stopwords.words('english'))
	post = ' '.join([word for word in post.split() if word not in (stopwords.words('english'))])

	post = post.split()

	# Takes the list and removes duplicates
	sorted_list = list(set(post))
	
	# Sorts the list
	sorted_list.sort()
	
	return sorted_list

# Function to compute distance between two vectors
def distance(trainScore,testScore,length):
	dist = 0
	for x in range(length):
		dist += pow((trainScore[x] - testScore[x]),2)
	return math.sqrt(dist)

#-------------------------------Main---------------------------#

# Opening train data
with open('test.txt', 'r') as myfile:
    o = myfile.read().replace('\n', '')

accuracy = 0;

# cleaning the entered post
testPost =  o

testPost =  cleanPost(testPost)

# Opening train data
with open('train.json') as data_file:    
    data = json.load(data_file)

# Number of train data found
size_jsonTrain = len(data["posts"]["row"])

distances = [0]*size_jsonTrain
ind = [0]*size_jsonTrain

# For each train data find the distance with the test data
for p in range(size_jsonTrain):
	post = data["posts"]["row"][p]
	trainPost = cleanPost(post.get("Body"))
	trainTest = []
	trainTest.extend(testPost)
	trainTest.extend(trainPost)
	trainTest_list = list(set(trainTest))
	trainTest_list.sort()

	# Computing test vector
	testScore = [0]*len(trainTest_list)
	for i in range(len(testPost)):
		if testPost[i] in trainTest_list:
			loc = trainTest_list.index(testPost[i])
			testScore[loc] = testScore[loc] + 1

	# Computing train vector
	trainScore = [0]*len(trainTest_list)
	for i in range(len(trainPost)):
		if trainPost[i] in trainTest_list:
			loc = trainTest_list.index(trainPost[i])
			trainScore[loc] = trainScore[loc] + 1

	dist = distance(trainScore,testScore,len(trainScore))	
	distances[p] = dist
	p += 1


# Finding the minimum distance data point in train data
train_loc = distances.index(min(distances))
trainTags = data["posts"]["row"][train_loc]["Tags"]

# Separating Tags as a string array
trainTags = trainTags.replace("<","")
trainTags = trainTags.replace(">","-")
trainList = trainTags.split('-')
trainList.remove('')
print "Predicted Tags for the question  - ", trainList