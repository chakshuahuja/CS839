import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE

# Reads from data.csv file generated
# TODO: read from the newly generated file every time at time of submission.

input_data = pd.read_csv("data.csv")
X = input_data.drop(['position', 'token', 'fid', 'label', 'Unnamed: 0'], axis=1)
y = input_data[['label']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

# smote = SMOTE(ratio='minority')
# X_train, y_train = smote.fit_sample(X_train, y_train)

clf = MLPClassifier(activation='logistic', solver='lbfgs', alpha=0.5, hidden_layer_sizes=(15,15), random_state=1)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

X_test['label'] = y_test
X_test['pred'] = y_pred

df = pd.DataFrame(X_test)
df.to_csv("output.csv")

# print(df)

# y_test = y_test.values
# print(type(y_pred))
# print(type(y_test.as_matrix()))
# for i in range(len(y_pred)):
# 	print(y_pred[i], y_test[i][0])

print(precision_recall_fscore_support(y_test, y_pred, average='macro'))
print(confusion_matrix(y_test,y_pred))  
print(classification_report(y_test,y_pred))
# print(len(X_train), len(X_test), len(X))
# print(len(y_train), len(y_test), len(y))
