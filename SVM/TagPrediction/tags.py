import pandas as pd
import csv

with open('tagTrain.csv', 'r') as f:
      print('--------Reading the train data----------')
    
train_dataframe = pd.read_csv('tagTrain.csv', encoding='ISO-8859-1',engine='python')
import numpy as np

#collecting the train labels
train_labels = train_dataframe.Tags
labels = list(train_labels)
train_labels = np.array([labels.index(x) for x in train_labels])

#creating a dictionary of the numpy conversion and the corresponding tags , to obtain the tag name from the predicted numpy number
pairs = {}
for i in range(len(labels)):
	pairs[train_labels[i]] = labels[i]


#assembling the train features for testing
train_features = train_dataframe.Title
col_1 = list(train_features)
train_features_1 = np.array([col_1.index(x) for x in train_features])
train_space = [[] for i in range(len(labels))]
for i in range(len(labels)):
	train_space[i].append(train_features_1[i])
	
from sklearn import svm

#training the data by using linear svm 
classifier = svm.SVC()
classifier.fit(train_space, train_labels)
print('*****Training the data with linear SVM*****')


with open('tagTest.csv', 'r') as f:
    print('----Reading the test data------')
    
test_dataframe = pd.read_csv('tagTest.csv', encoding='ISO-8859-1',engine='python')
test_labels = test_dataframe.Tags
labels = list(test_labels)
test_labels = np.array([labels.index(x) for x in test_labels])

test_features = test_dataframe.Title
col_1 = list(test_features)
test_features_1 = np.array([col_1.index(x) for x in test_features])

test_space = [[] for i in range(len(test_labels))]

for i in range(len(test_labels)):
	test_space[i].append(test_features_1[i])
	

print('*********Testing the test data by using the trained classifier*********')
results = classifier.predict(test_space)

print('**************************************************************')
num_correct = (results == test_labels).sum()
recall = num_correct*100/ 5714
print("model accuracy (%): ", recall * 100, "%")


print('*********Prediction for a use case *****************')
test_data_contents = """
Tags,Title
<database,how to select two rows in SQL?
"""
print(test_data_contents)
with open('test2.csv', 'w') as output:
    output.write(test_data_contents)

test_dataframe = pd.read_csv('test2.csv')
test_labels = test_dataframe.Tags

labels = list(test_labels)
test_labels = np.array([labels.index(x) for x in test_labels])

test_features = test_dataframe.Title
col_1 = list(test_features)
test_features_1 = np.array([col_1.index(x) for x in test_features])
test_space = [[] for i in range(len(test_labels))]
for i in range(len(test_labels)):
	test_space[i].append(test_features_1[i])
	

results = classifier.predict(test_space)
print('Predicted tag')
for t_l, l in pairs.items():
    if t_l == results[0]:
        print(l)
   

