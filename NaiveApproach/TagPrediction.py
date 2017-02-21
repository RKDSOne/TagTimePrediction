from __future__ import division
import json
import string
from pprint import pprint
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
import string

# Openning train data
with open('test.json') as data_file:    
    data = json.load(data_file)

# Number of train data found
size_json = len(data["posts"]["row"])

accuracy = 0;
for post in data["posts"]["row"]:

	o =  post.get("Body")

	# Removes encoded html tags
	o = o.replace('&lt;','<')
	o = o.replace('&gt;','>')
	o = o.encode("utf-8")

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

	# Loads the Tags from Tags.json file
	with open('Tags.json') as data_file:    
	    data = json.load(data_file)

	# Number of Tags found
	size_json = len((data["tags"]["row"]))

	tags = []

	for i in range(size_json):
		tags.append((data["tags"]["row"][i]["-TagName"]).encode("utf-8"))

	word_list = o.split()

	predicted = []

	# Checks if words in a sentence are present in a Tags array
	for word in word_list:
		if word in tags:
			if word not in predicted:
				predicted.append(word.encode("utf-8"))

	tag = post.get("Tags")

	for word in predicted:
		word = "<" + word + ">"
		if tag.find(word) != -1:			
			accuracy += 1
			break;

with open('test.json') as data_file:    
    data = json.load(data_file)

# Number of train data found
size_json = len(data["posts"]["row"])

per = (accuracy/size_json) * 100
print "Accuracy - ", per