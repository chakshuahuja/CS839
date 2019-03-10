"""TOKENIZER CLI

Usage:
    main.py [--shuffle]
    main.py -h | --help

Options:
    -h --help  : Generates test and train data for files from 1-200 and 201-300 by default.
    --shuffle  : Generates test and train data by randomly choosing 100 files and 200 files.

"""

from docopt import docopt
import random
from tokenizer import Tokenizer
import pandas as pd

def get_file_name(i):
	fname = ""
	if i < 10:
		fname = "00" + str(i)
	elif i >= 10 and i < 100:
		fname = "0" + str(i)
	else:
		fname = str(i)
	return fname

TOTAL_FILE_COUNT = 300
TRAIN_FILE_COUNT = 200
TEST_FILE_COUNT = 100

def generateShuffledData():
	train_files = random.sample(range(1, TOTAL_FILE_COUNT+1), TRAIN_FILE_COUNT)
	test_files = list(set(list(range(1, TOTAL_FILE_COUNT+1))) - set(train_files))
	print('Train files indices: ')
	print(train_files)
	print()

	print('Test files indices: ')
	print(test_files)
	print()

	assert(len(test_files) == TEST_FILE_COUNT)

	def getData():
		TRAIN_DATA = []
		TRAIN_POS, TRAIN_NEG = 0, 0

		TEST_DATA = []
		TEST_POS, TEST_NEG = 0, 0

		for i in range(1, TOTAL_FILE_COUNT+1):
			fname = get_file_name(i)
			F = Tokenizer("labelled/" + fname + ".txt")
			F.tokenize()
			F.filter_tokens()

			# F.print_tokens()

			d, p, n = F.vectorize()
			for v in d:
				if int(v['fid']) in train_files:
					TRAIN_DATA.append(v)
				else:
					TEST_DATA.append(v)

			if int(v['fid']) in train_files:
				TRAIN_POS += p
				TRAIN_NEG += n
			else:
				TEST_POS += p
				TEST_NEG += n

		print('Generating Train Data tokens...')
		print("Token generation completed.")
		print('{0: <10} {1: <10} {2: <10}'.format("Total", "Positive", "Negative"))
		print('{0: <10} {1: <10} {2: <10}'.format(len(TRAIN_DATA), TRAIN_POS, TRAIN_NEG))

		print('Generating Test Data tokens...')
		print("Token generation completed.")
		print('{0: <10} {1: <10} {2: <10}'.format("Total", "Positive", "Negative"))
		print('{0: <10} {1: <10} {2: <10}'.format(len(TEST_DATA), TEST_POS, TEST_NEG))

		return TRAIN_DATA, TEST_DATA

	train_data, test_data = getData()
	train_df = pd.DataFrame(train_data)
	train_df.to_csv("train.csv")

	test_df = pd.DataFrame(test_data)
	test_df.to_csv("test.csv")


def generateFixedData():
	def getData(startIndex, endIndex):
		all_data = []
		all_pos = 0
		all_neg = 0
		for i in range(startIndex, endIndex + 1):
			fname = get_file_name(i)
			F = Tokenizer("labelled/" + fname + ".txt")
			F.tokenize()
			F.filter_tokens()

			# F.print_tokens()

			d, p, n = F.vectorize()
			[all_data.append(v) for v in d]
			all_pos += p
			all_neg += n

		print("Token generation completed.")
		print('{0: <10} {1: <10} {2: <10}'.format("Total", "Positive", "Negative"))
		print('{0: <10} {1: <10} {2: <10}'.format(len(all_data), all_pos, all_neg))

		return all_data

	print('Generating Train Data tokens...')
	train_df = pd.DataFrame(getData(101, 300))
	train_df.to_csv("train.csv")

	print('Generating Test Data tokens...')
	test_df = pd.DataFrame(getData(1, 100))
	test_df.to_csv("test.csv")

def main(docopt_args):
	if docopt_args["--shuffle"]:
		print("""
			Shuffle has been set.
			Generating train and test data by choosing random 200 files for training and 100 files for testing
			from folder B (containing all 300 files).
		""")
		generateShuffledData()
	else:
		print("""
			Generating train data from files indexed 101-300 (in folder I) and
			test data from files indexed 1-100 (in folder J).
		""")
		generateFixedData()

if __name__ == "__main__":
	args = docopt(__doc__)
	main(args)
