import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn import linear_model
from imblearn.over_sampling import SMOTE

DT = "Decision Tree"
RF = "Random Forest"
SVM = "Support Vector"
NB = "Naive Bayes"
NN = "Neural Network"
LR = "Linear Regression"
LOR = "Logistic Regression"
ALL = "All"

class Classifers:

	def __init__(self, fname):
		self.input_data = pd.read_csv(fname)
		self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

	def decision_tree(self):
		clf = DecisionTreeClassifier(criterion="entropy")
		clf.fit(self.X_train, self.y_train)
		y_pred = clf.predict(self.X_test)
		return (precision_recall_fscore_support(self.y_test, y_pred, average='binary'))

	def random_forest(self):
		clf = clf = RandomForestClassifier(n_estimators = 1000, criterion="entropy", bootstrap=False)
		clf.fit(self.X_train, self.y_train.values.ravel())
		y_pred = clf.predict(self.X_test)
		feature_list = list(self.X_test.columns)
		feature_importance = clf.feature_importances_
		for index in range(len(feature_list)):
			print(feature_list[index], feature_importance[index])
		return (precision_recall_fscore_support(self.y_test, y_pred, average='binary'))
		
	def support_vector(self):
		clf = svm.SVC(gamma='scale', tol=0.00001)
		clf.fit(self.X_train, self.y_train.values.ravel())
		y_pred = clf.predict(self.X_test)
		return (precision_recall_fscore_support(self.y_test, y_pred, average='binary'))

	def neural_network(self):
		clf = MLPClassifier(solver='adam', activation='relu', alpha=0.0001, hidden_layer_sizes=(15,15), random_state=42)
		clf.fit(self.X_train, self.y_train.values.ravel())
		y_pred = clf.predict(self.X_test)
		return (precision_recall_fscore_support(self.y_test, y_pred, average='binary'))

	def linear_regression(self):
		clf = linear_model.LinearRegression()
		clf.fit(self.X_train, self.y_train.values.ravel())
		y_pred = clf.predict(self.X_test)
		y_binary_pred = [1 if p > 0.5 else 0 for p in y_pred]
		return (precision_recall_fscore_support(self.y_test, y_binary_pred, average="binary"))

	def logistic_regression(self):
		clf = linear_model.LogisticRegression(max_iter=1000, solver='lbfgs', multi_class='multinomial')
		clf.fit(self.X_train, self.y_train.values.ravel())
		y_pred = clf.predict(self.X_test)
		return (precision_recall_fscore_support(self.y_test, y_pred, average="binary"))

	def print_results(self, clf, result):
		print("{classifier} {precision} {recall}".format(classifier=clf, precision=result[0], recall=result[1]))

	def run(self, classifier):
		X = self.input_data.drop(['label', 'Unnamed: 0', 'position', 'token', 'fid'], axis=1)
		y = self.input_data[['label']]
		
		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.33)

		# smote = SMOTE()
		# self.X_train, self.y_train = smote.fit_sample(self.X_train, self.y_train)
		# self.X_train = pd.DataFrame(self.X_train)
		# self.y_train = pd.DataFrame(self.y_train)

		if classifier == DT: self.print_results(DT, self.decision_tree())
		if classifier == SVM: self.print_results(SVM, self.support_vector())
		if classifier == RF: self.print_results(RF, self.random_forest())
		if classifier == NN: self.print_results(NN, self.neural_network())
		if classifier == LR: self.print_results(LR, self.linear_regression())
		if classifier == LOR: self.print_results(LOR, self.logistic_regression())

clf = Classifers("data.csv")
for classifier in [DT, SVM, RF, NN, LR, LOR]:	
	clf.run(classifier)
