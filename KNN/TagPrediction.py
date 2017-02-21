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
	post = post.encode("utf-8")

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

	post = post.encode("utf-8").split()

	# Takes the list and removes duplicates
	sorted_list = list(set(post))

	# Sorts the list
	sorted_list.sort()
	
	return sorted_list

def distance(trainScore,testScore,length):
	dist = 0
	for x in range(length):
		dist += pow((trainScore[x] - testScore[x]),2)
	return math.sqrt(dist)

#-------------------------------Main---------------------------#

target = open('result.txt', 'w')
target.truncate()

with open('testS.json') as data_fileTest:    
    dataTest = json.load(data_fileTest)

# Number of train data found
size_json = len(dataTest["posts"]["row"])

accuracy = 0;
for postTest in dataTest["posts"]["row"]:

	# cleaning the entered post
	testPost =  postTest.get("Body")
	
	testPost =  cleanPost(testPost)

	testTags = postTest.get("Tags")
	target.write("Test Tags - "+ testTags + "\n")

	# Openning train data
	with open('trainS.json') as data_file:    
	    data = json.load(data_file)

	# Number of train data found
	size_jsonTrain = len(data["posts"]["row"])

	distances = [0]*size_jsonTrain
	ind = [0]*size_jsonTrain
	p = 0

	for p in range(10):
		post = data["posts"]["row"][p]
		trainPost = cleanPost(post.get("Body"))
		trainTest = []
		trainTest.extend(testPost)
		trainTest.extend(trainPost)
		trainTest_list = list(set(trainTest))
		trainTest_list.sort()

		testScore = [0]*len(trainTest_list)
		for i in range(len(testPost)):
			if testPost[i] in trainTest_list:
				loc = trainTest_list.index(testPost[i])
				testScore[loc] = testScore[loc] + 1

		trainScore = [0]*len(trainTest_list)
		for i in range(len(trainPost)):
			if trainPost[i] in trainTest_list:
				loc = trainTest_list.index(trainPost[i])
				trainScore[loc] = trainScore[loc] + 1

		dist = distance(trainScore,testScore,len(trainScore))	
		distances[p] = dist
		p += 1

	train_loc = distances.index(min(distances))
	trainTags = data["posts"]["row"][train_loc]["Tags"]
	target.write("Train Tags - "+ trainTags+ "\n")

	# Separating train tags
	trainTags = trainTags.replace("<","")
	trainTags = trainTags.replace(">","-")
	trainList = trainTags.split('-')
	trainList.remove('')

	# Separating test tags
	testTags = testTags.replace("<","")
	testTags = testTags.replace(">","-")
	testList = testTags.split('-')
	testList.remove('')
	
	# Check the occurance of train tag in test tags
	flag = 0
	for word1 in testList:
		for word2 in trainList:
			if word1.find(word2) != -1 or word2.find(word1) != -1:
				flag = 1
				accuracy += 1
				target.write("Word is "+word1+" or "+word2+ "\n")
				target.write("Accuracy Inc "+str(accuracy)+ "\n")
				break
		if flag == 1:
			break;
	target.write("------------------------------------------------------\n")

target.write("Correct prediction - "+ str(accuracy)+ "\n")
target.write("Data set length - " + str(len(dataTest["posts"]["row"]))+ "\n")
per = (accuracy/len(dataTest["posts"]["row"])) * 100
print "Accuracy - ", per
target.write("Accuracy - " + str(per))
target.close()



