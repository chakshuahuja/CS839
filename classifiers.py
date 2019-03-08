import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn import svm

# Reads from data.csv file generated
# TODO: read from the newly generated file every time at time of submission.

input_data = pd.read_csv("data.csv")
X = input_data.drop(['label', 'Unnamed: 0'], axis=1)
y = input_data[['label']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

#Neural Net
clf = MLPClassifier(solver='lbfgs', activation='logistic', alpha=0.0001, hidden_layer_sizes=(15), random_state=42)
# print(type(X_train))

X_input_train = X_train.drop(['position', 'token', 'fid'], axis=1)
X_input_test = X_test.drop(['position', 'token', 'fid'], axis=1)

feature_list = list(X_input_test.columns)
print(feature_list)

#SVM
# clf = svm.SVC(gamma='scale', tol=0.00001)

#Random Forest
# clf = RandomForestClassifier(n_estimators = 1000, criterion="entropy", bootstrap=False)

#Decision Tree
# clf = DecisionTreeClassifier(criterion="entropy")

clf.fit(X_input_train, y_train)
y_pred = clf.predict(X_input_test)

# print(clf.feature_importances_)

print(precision_recall_fscore_support(y_test, y_pred, average='macro'))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test,y_pred))


X_test['y_true'] = y_test
X_test['y_pred'] = y_pred
X_test.to_csv("prediction.csv")

# add feature whether more entities are present in the sentence
# capitalized and not first word common names
# distance of each word
# comma or and separated entities
