import pandas as pd
import csv
import numpy as np

with open('optimumTrain.csv', 'r') as f:
    print('--------Reading the train data----------')
  
#Reading the csv by using panda  
train_dataframe = pd.read_csv('optimumTrain.csv', encoding='ISO-8859-1',engine='python')

#collecting the train labels
train_labels = train_dataframe.creationTime
labels = list(set(train_labels))
train_labels = np.array([labels.index(x) for x in train_labels])

#assembling the training features
train_features = train_dataframe.Body
col_1 = list(set(train_features))
train_featuress = train_dataframe.Tags
col_2 = list(set(train_featuress))
train_features_1 = np.array([col_1.index(x) for x in train_features]) #converting string data using numpy
train_features_2 = np.array([col_2.index(x) for x in train_featuress])
train_featuresView = train_dataframe.ViewCount
train_featuresView = np.array(train_featuresView)
train_featuresCom = train_dataframe.CommentCount
train_featuresCom = np.array(train_featuresCom)
train_featuresAns = train_dataframe.AnswerCount
train_featuresAns = np.array(train_featuresAns)

train_space = [[] for i in range(len(train_labels))]

for i in range(len(train_labels)):
	train_space[i].append(train_features_1[i])
	train_space[i].append(train_features_2[i])
	train_space[i].append(train_featuresView[i])
	train_space[i].append(train_featuresCom[i])
	train_space[i].append(train_featuresAns[i])


from sklearn import svm

# Training the data by using the SVM linear classification algorithm
classifier = svm.SVC()
classifier.fit(train_space, train_labels)
print('*****Training the data with linear SVM*****')
with open('optimumTest.csv', 'r') as f:
    print('----Reading the test data------')
    
# collecting the test labels
test_dataframe = pd.read_csv('optimumTest.csv', encoding='ISO-8859-1',engine='python')
test_labels = test_dataframe.creationTime
labels = list(set(test_labels))
test_labels = np.array([labels.index(x) for x in test_labels])

#assembling the test features
test_features = test_dataframe.Body
col_1 = list(set(test_features))
test_featuress = test_dataframe.Tags
col_2 = list(set(test_featuress))
test_features_1 = np.array([col_1.index(x) for x in test_features])
test_features_2 = np.array([col_2.index(x) for x in test_featuress])
test_featuresView = test_dataframe.ViewCount
test_featuresView = np.array(test_featuresView)
test_featuresCom = test_dataframe.CommentCount
test_featuresCom = np.array(test_featuresCom)
test_featuresAns = test_dataframe.AnswerCount
test_featuresAns = np.array(test_featuresAns)
test_space = [[] for i in range(len(test_labels))]
for i in range(len(test_labels)):
	test_space[i].append(test_features_1[i])
	test_space[i].append(test_features_2[i])
	test_space[i].append(test_featuresView[i])
	test_space[i].append(test_featuresCom[i])
	test_space[i].append(test_featuresAns[i])


#predict the results by using the trained classifier
results = classifier.predict(test_space)
print('*********Testing the test data by using the trained classifier*********')
print('Mean square error: ')
from sklearn.metrics import mean_squared_error
print(mean_squared_error(test_labels, results))#, sample_weight=None, multioutput='uniform_average')[source])
print('**************************************************************')


sum=0
for x in range(len(test_labels)):
    if results[x] == test_labels[x]:
    	sum=sum+1
    #elif results[x]+1 == test_labels[x]:
    #	sum=sum+1
    #elif results[x]-1 == test_labels[x]:
    #	sum=sum+1

num_correct =sum 
recall = num_correct * 100/ len(test_labels)
print("model accuracy (%): ", recall, "%")

print('*********Prediction for a use case *****************')

#the test case for which optimal time has to be predicted
test_data_contents = """
Body,Tags,ViewCount,CommentCount,AnswerCount,creationTime
how to prepare for interviews?,<java,5000,1890,2432,1
"""
print(test_data_contents)
with open('test2.csv', 'w') as output:
    output.write(test_data_contents)
test_dataframe = pd.read_csv('test2.csv')
test_labels = test_dataframe.creationTime

labels = list(set(test_labels))
test_labels = np.array([labels.index(x) for x in test_labels])


test_features = test_dataframe.Body
col_1 = list(set(test_features))
test_features_1 = np.array([col_1.index(x) for x in test_features])
test_featuress = test_dataframe.Tags
col_2 = list(set(test_featuress))
test_features_1 = np.array([col_1.index(x) for x in test_features])
test_features_2 = np.array([col_2.index(x) for x in test_featuress])
test_featuresView = test_dataframe.ViewCount
test_featuresView = np.array(test_featuresView)
test_featuresCom = test_dataframe.CommentCount
test_featuresCom = np.array(test_featuresCom)
test_featuresAns = test_dataframe.AnswerCount
test_featuresAns = np.array(test_featuresAns)

test_space = [[] for i in range(len(test_labels))]
for i in range(len(test_labels)):
	test_space[i].append(test_features_1[i])
	test_space[i].append(test_features_2[i])
	test_space[i].append(test_featuresView[i])
	test_space[i].append(test_featuresCom[i])
	test_space[i].append(test_featuresAns[i])


#converting the predicted value into appropriate time slot
results = classifier.predict(test_space)
time= results[0]
print('Optimal time to post question is : ')
if time==1 :
	print('00:00 am - 04.00 am')
elif time ==2 :
	print('04:01 am - 08.00 am')
elif time ==3 :
	print('08:01 am - 12.00 pm')
elif time ==4 :
	print('12:01 am - 16.00 pm')
elif time ==5 :
	print('16:01 pm - 20.00 pm')
elif time ==6 :
	print('20:01 pm - 23.59 pm')


