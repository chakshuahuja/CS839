"""TOKENIZER CLI

Usage:
    tokenizer.py [--shuffle]
    tokenizer.py -h | --help

Options:
    -h --help  : Generates test and train data for files from 1-200 and 201-300 by default.
    --shuffle  : Generates test and train data by randomly choosing 100 files and 200 files.

"""

from docopt import docopt

from itertools import accumulate
import re
from features import *
import pandas as pd
from collections import Counter
import random

class Token:
    def __repr__(self):
        return "Tok<{string}, {pos}, {raw_pos} {has_name}>".format(
            string=Tokenizer.clean(self.string), pos=self.labelled_pos, raw_pos=self.raw_pos, has_name=self.has_name
        )

    def __init__(self, string, pos, raw_pos, has_name):
        self.string = string
        self.labelled_pos = pos
        self.raw_pos = raw_pos
        self.has_name = has_name

class UnigramIterator:
    START_TAG = "<b>"
    END_TAG = "</b>"
    def __init__(self, string):
        self.string = string

        # TODO: handle cases for different delimiters
        self.words = re.split(r' |\n', string)
        self.counter = -1
        self.labelled_cursor = 0
        self.raw_cursor = 0
        self.has_name = False

    def __iter__(self):
        return self

    def __next__(self):

        start_tag = self.START_TAG
        end_tag = self.END_TAG

        self.counter += 1
        if self.counter >= len(self.words):
            raise StopIteration

        curr_word = self.words[self.counter]
        rm_chars = 0
        has_name = self.has_name

        if start_tag in curr_word:
        	rm_chars += len(start_tag)
        	has_name = True

        if end_tag in curr_word:
        	rm_chars += len(end_tag)

        result = Token(
            curr_word,
            self.labelled_cursor + (len(start_tag) if curr_word.startswith(start_tag) else 0),
            self.raw_cursor,
            has_name
        )
        # Reset if closing tag encountered
        self.has_name = has_name if end_tag not in curr_word else False

        self.raw_cursor = self.raw_cursor + len(curr_word) + 1 - rm_chars
        self.labelled_cursor = self.labelled_cursor + len(curr_word) + 1

        if result.string == "": return next(self)

        return result

class NgramIterator():

    def __init__(self, string, n):
        self.ui = UnigramIterator(string)
        self.prev = []
        self.n = n

    def __iter__(self): return self
    def __next__(self):
        new_tokens = [next(self.ui) for i in range(self.n)] if not self.prev else [next(self.ui)]
        curr_tokens = self.prev + new_tokens

        self.prev = curr_tokens[1:]
        return Token(
            ' '.join([t.string for t in curr_tokens]),
            curr_tokens[0].labelled_pos, 
            curr_tokens[0].raw_pos,
            all([t.has_name for t in curr_tokens])
        )

def test(data):
	for i, token_vector in enumerate(data):

		text = Tokenizer.clean(getDocumentContent(token_vector['fid']))
		vector_val = token_vector['isStartOfSentence']
		all_indices = [i for i in range(len(text)) if text.startswith(token_vector['token'], i)]

		if token_vector['position'] in all_indices:
			feature_val = int(isStartOfSentence(token_vector['position'], text))
		# else:
		# 	print('ALL INDICES', '--' + token_vector['token'] + '--' , all_indices, token_vector['fid'])

		if vector_val != feature_val:
			# print(token_vector['token'], vector_val, feature_val, token_vector['position'])
			return False

	return True

class Tokenizer:

	def __init__(self, fname):

		self.fname = fname
		self.fidentifier = self.fname.split('/')[-1].strip('.txt')

		self.fcontents = None	
		self.tokens = [] # Contains all 1,2,3..maximum_len words tokens
		self.freq_tokens = Counter() # Contains mapping of token -> freq
		self.filtered_tokens = [] # Only all capitalized tokens

		with open(fname,'r') as f:
			self.fcontents = f.read()

	@classmethod
	def clean(self, token):
		# Remove the start and end tags
		return token.replace(UnigramIterator.START_TAG, '').replace(UnigramIterator.END_TAG, '')

	def tokenize(self, maximum_len=4):

		for curr_len in range(1, maximum_len + 1):
			word_iterator = NgramIterator(self.fcontents, curr_len)
			for token in list(word_iterator):
				curr_label = token.has_name
				self.tokens.append((self.fidentifier, self.clean(token.string), token.raw_pos, curr_label))

		return self.tokens

	def _has_special_char(self, token):
		def f(word):
			return word.endswith(",") or word.endswith("!") or word.endswith(".") or word.endswith("'s") or word.endswith("s'")

		return any([f(w.strip()) for w in token.split()[:-1]])

	def _has_more_than_threshold_freq(self, token, threshold=10):
		if self.freq_tokens.get(token, 0) > threshold:
			return True
		return False

	def filter_tokens(self):
		self.freq_tokens = Counter([t[1] for t in self.tokens])
		self.filtered_tokens = []
		for fid, token, tpos, tlabel in self.tokens:
			# BLOCKING 1: Remove token where every word in the token is not capitalized
			# BLOCKING 2: Remove token if it contains , . or !
			# BLOCKING 3: Remove token if freq in that document > threshold
			if allWordsCapitalized(token) and not self._has_special_char(token):
				if not self._has_more_than_threshold_freq(token):
					self.filtered_tokens.append((fid, token, tpos, tlabel))
		return self.filtered_tokens

	def print_tokens(self):
		for fid, t, tp, l in self.filtered_tokens:
			print("{f_id} {label} {token} {token_position}".format(f_id=fid, token=t, token_position=tp, label=l))

	def vectorize(self):
		data = []
		pos, neg = 0, 0
		fcontents = self.clean(self.fcontents)

		for fid, token, tpos, tlabel in self.filtered_tokens:
			# print(fid, token, tpos, len(self.clean(self.fcontents)))
			token_vector = {'fid': fid, 'token': token, 'position': tpos, 'label': tlabel}
			token_vector['isStartOfSentence'] = int(isStartOfSentence(tpos, fcontents))
			token_vector['isContainPrefix'] = int(isContainPrefix(token))
			token_vector['isContainSuffix'] = int(isContainSuffix(token))
			token_vector['isPartial'] = int(isPartial(tpos, fcontents, token))
			token_vector['hasPartialNameOccurence'] = int(hasPartialNameOccurence(tpos, fcontents, token))
			token_vector['hasFullNameOccurence'] = int(hasFullNameOccurence(tpos, fcontents, token))
			token_vector['hasPreposition'] = int(hasPreposition(tpos, fcontents))
			token_vector['isPrecededByOccupationWords'] = int(isPrecededByOccupationWords(tpos, fcontents)[0])
			token_vector['precedingOccupationWordDistance'] = int(isPrecededByOccupationWords(tpos,fcontents)[1])  #this seems to be degrading performance
			token_vector['isSucceededByOccupationWords'] = int(isSucceededByOccupationWords(tpos, fcontents, token)[0])
			token_vector['succeededByOccupationWordDistance'] = int(isSucceededByOccupationWords(tpos, fcontents, token)[1])
			token_vector['allWordsCapitalized'] = int(allWordsCapitalized(token))
			# # token_vector['areMoreEntitiesPresentInSentence'] = int(areMoreEntitiesPresentInSentence(tpos, fcontents, token))
			token_vector['endsWithApostropheS'] = int(endsWithApostropheS(token))
			# token_vector['endsWithComma'] = int(endsWithComma(token))
			token_vector['numWords'] = int(len(token.split()))
			token_vector['totalLength'] = int(len(token))
			# token_vector['lineContainsPronoun'] = int(lineContainsPronoun(tpos, fcontents))
			# token_vector['nextLineContainsPronoun'] = int(nextLineContainsPronoun(tpos, fcontents))
			token_vector['isPreceededByFamilyRelation'] = int(isPreceededByFamilyRelation(tpos, fcontents))
			token_vector['isFollowedByFamilyRelation'] = int(isFollowedByFamilyRelation(tpos, fcontents))
			token_vector['isNearStatementWord'] = int(isNearStatementWord(tpos, fcontents))
			token_vector['isPreceededByNonPersonEntity'] = int(isPreceededByNonPersonEntity(tpos, fcontents)[0])
			token_vector['distancePrecedingNonPersonEntity'] = int(isPreceededByNonPersonEntity(tpos, fcontents)[1]) #works fine with Random Forest, degrades performance with NN
			token_vector['distanceSucceedingNonPersonEntity'] = int(isFollowedByNonPersonEntity(tpos, fcontents)[1])
			token_vector['isFollowedByNonPersonEntity'] = int(isFollowedByNonPersonEntity(tpos, fcontents)[0])
			token_vector['containsCommonWord'] = int(containsCommonWord(token))
			token_vector['isPrecededByOtherEntities'] = int(isPrecededByOtherEntities(tpos, fcontents))
			token_vector['isSucceededByOtherEntities'] = int(isSucceededByOtherEntities(tpos, fcontents))
			token_vector['isPreceededByThe'] = int(isPreceededByThe(tpos, fcontents))
			token_vector['containsCommonWord'] = int(containsCommonWord(token))
			token_vector['isCommonName'] = int(isCommonName(token))
			token_vector['allCharactersCapitalized'] = int(allCharactersCapitalized(token))
			token_vector['isLocation'] = int(isLocation(token))
			token_vector['isOnlyTitle'] = int(is_only_title(token))

			if tlabel == 1: pos += 1
			else: neg += 1
			# print(token_vector)
			data.append(token_vector)

		return data, pos, neg


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
			print(fname)
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
