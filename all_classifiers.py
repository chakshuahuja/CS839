import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm

DT = "Decision Tree"
RF = "Random Forest"
SVM = "Support Vector"
NB = "Naive Bayes"
ALL = "All"

class Classifers:

	def __init__(self, fname):
		self.input_data = pd.read_csv(fname)
		self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

	def decision_tree(self):
		clf = DecisionTreeClassifier(criterion="entropy")
		clf.fit(self.X_train, self.y_train)
		y_pred = clf.predict(self.X_test)
		return (precision_recall_fscore_support(self.y_test, y_pred, average='macro'))

	def random_forest(self):
		clf = clf = RandomForestClassifier(n_estimators = 1000, criterion="entropy", bootstrap=False)
		clf.fit(self.X_train, self.y_train.values.ravel())
		y_pred = clf.predict(self.X_test)
		return (precision_recall_fscore_support(self.y_test, y_pred, average='macro'))
		
	def support_vector(self):
		clf = svm.SVC(gamma='scale', tol=0.00001)
		clf.fit(self.X_train, self.y_train.values.ravel())
		y_pred = clf.predict(self.X_test)
		return (precision_recall_fscore_support(self.y_test, y_pred, average='macro'))

	def print_results(self, clf, result):
		print("{classifier} {precision} {recall}".format(classifier=clf, precision=result[0], recall=result[0]))

	def run(self, classifier):
		X = self.input_data.drop(['label', 'Unnamed: 0', 'position', 'token', 'fid'], axis=1)
		y = self.input_data[['label']]
		
		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.33)

		if classifier == DT: self.print_results(DT, self.decision_tree())
		if classifier == SVM: self.print_results(SVM, self.support_vector())
		if classifier == RF: self.print_results(RF, self.random_forest())

clf = Classifers("data.csv")
for classifier in [DT, RF, SVM]:	
	clf.run(classifier)
