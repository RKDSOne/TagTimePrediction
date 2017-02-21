import json
import string
from pprint import pprint
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
import string

# Opening train data
with open('test.txt', 'r') as myfile:
    o = myfile.read().replace('\n', '')

print "Post - "
print o

# Removes encoded html tags
o = o.replace('&lt;','<')
o = o.replace('&gt;','>')

# Removes HTML tahs
soup = BeautifulSoup(o, 'html.parser')
o = soup.get_text()

# To lower case
o = o.lower()

# Removes punctuation
exclude = set(string.punctuation)
o = ''.join(ch for ch in o if ch not in exclude)

# Removes stop words
stop = set(stopwords.words('english'))
o = ' '.join([word for word in o.split() if word not in (stopwords.words('english'))])

word_list = o.split()

# Loads the Tags from Tags.json file
with open('Tags.json') as data_file:    
    data = json.load(data_file)

# Number of Tags found
size_json = len((data["tags"]["row"]))

# Loading the tags in the list
tags = []

for i in range(size_json):
	tags.append((data["tags"]["row"][i]["-TagName"]).encode("utf-8"))

predicted = []

# Checks if words in a sentence are present in a Tags array
for word in word_list:
	if word in tags:
		if word not in predicted:
			predicted.append(word.encode("utf-8"))

print "Predicted Tags for query - "
print predicted

# Loading the csv that contains creation time for the post
with open('train.json') as data_file:    
    data = json.load(data_file)

# Number of train data found
size_json = len(data["posts"]["row"])

print "Predicted Times to post query- "

# Checking the predicted tags for appropriate time to post the question
for predicted_string in predicted:

	times = ["0:01 to 4:00 UTC", "4:01 to 8:00 UTC", "8:00 to 12:00 UTC", "12:01 to 16:00 UTC", "16:01 to 20:00 UTC", "20:01 to 0:00 UTC"]
	distances = [0]*6

	for post in data["posts"]["row"]:
		tag = post.get("Tags")
		if tag.find(predicted_string) != -1:
			if post.get("AnswerCount") != 0:
				ind = post.get("creationTime")
				distances[ind-1] = distances[ind-1] + 1
				post.get("creationTime")

	print "Optimal Time for Tag - ",predicted_string
	print times[distances.index(max(distances)) + 1]

	