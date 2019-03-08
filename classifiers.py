import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE

# Reads from data.csv file generated
# TODO: read from the newly generated file every time at time of submission.

input_data = pd.read_csv("data.csv")
X = input_data.drop(['label', 'Unnamed: 0'], axis=1)
y = input_data[['label']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
clf = MLPClassifier(solver='lbfgs', verbose=True, alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
print(type(X_train))
X_input_train = X_train.drop(['position', 'token', 'fid'], axis=1)
X_input_test = X_test.drop(['position', 'token', 'fid'], axis=1)

clf.fit(X_input_train, y_train)    
y_pred = clf.predict(X_input_test)
X_test['y_true'] = y_test
X_test['y_pred'] = y_pred
X_test.to_csv("prediction.csv")
