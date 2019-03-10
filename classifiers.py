import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn import svm

from features import *

def isMixOfAlphabetsAndNumbers(token):
	words = token.split()
	for word in words:
		for i in range(len(word)):
			numbers = 0
			alphabets = 0
			if (word[i].isalnum()):
				if word[i].isalpha():
					alphabets = alphabets + 1
				else:
					numbers = numbers + 1
			
		if alphabets > 0 and numbers > 0:
			print(token)
			return True
	return False

def areAllWordsCapitalized(token):
	words = token.split()
	for word in words:
		for i in range(len(word)):
			if (word[i].isalpha() and word[i].islower()):
				return False
	print(token)
	return True	

# Reads from data.csv file generated
# TODO: read from the newly generated file every time at time of submission.

input_data = pd.read_csv("train.csv")
X_train = input_data.drop(['label', 'Unnamed: 0'], axis=1)
y_train = input_data[['label']]

test_data = pd.read_csv("test.csv")
X_test = test_data.drop(['label', 'Unnamed: 0'], axis=1)
y_test = test_data[['label']]

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

#Neural Net
clf = MLPClassifier(solver='adam', activation='relu', alpha=0.0001, hidden_layer_sizes=(15,15), random_state=42, max_iter=500, verbose=False)
# print(type(X_train))

X_input_train = X_train.drop(['position', 'token', 'fid'], axis=1)
X_input_test = X_test.drop(['position', 'token', 'fid'], axis=1)

feature_list = list(X_input_test.columns)
# print(feature_list)

#SVM
# clf = svm.SVC(gamma='scale', tol=0.00001)

#Random Forest
# clf = RandomForestClassifier(n_estimators = 1000, criterion="entropy", bootstrap=False)

#Decision Tree
# clf = DecisionTreeClassifier(criterion="entropy")

clf.fit(X_input_train, y_train)
y_pred = clf.predict(X_input_test)

# print(clf.feature_importances_)

X_test['y_true'] = y_test
X_test['y_pred'] = y_pred

count_true = 0
count_false = 0
for v in y_pred:
	if v == False: count_false += 1
	else: count_true += 1

print(count_false, count_true)

false_result = []
result = X_test.values
print(isLocation('New York'))
for i in range(len(result)):
	length = len(result[i])
	if result[i][length - 1] == True and result[i][length - 2] == False:
		
		if (isMixOfAlphabetsAndNumbers(result[i][length - 4]) or areAllWordsCapitalized(result[i][length - 4]) or isLocation(result[i][length-4]) or containsCommonWord(result[i][length-4])):
			result[i][length - 1] = False
			y_pred[i] = False
		else:
			false_result.append(result[i])
		

count_true = 0
count_false = 0
for v in y_pred:
	if v == False: count_false += 1
	else: count_true += 1

print(count_false, count_true)

df = pd.DataFrame(false_result)
df.to_csv("false_result.csv")

X_test = pd.DataFrame(result)
X_test.to_csv("prediction.csv")

print(precision_recall_fscore_support(y_test, y_pred, average='macro'))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test,y_pred))

# add feature whether more entities are present in the sentence
# capitalized and not first word common names
# distance of each word
# comma or and separated entities
