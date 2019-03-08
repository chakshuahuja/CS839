from itertools import accumulate
import re
from features import *
import pandas as pd


class Token:
    def __repr__(self):
        return "Tok<{string}, {pos}, {raw_pos}>".format(
            string=Tokenizer.clean(self.string), pos=self.labelled_pos, raw_pos=self.raw_pos
        )

    def __init__(self, string, pos, raw_pos):
        self.string = string
        self.labelled_pos = pos
        self.raw_pos = raw_pos

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
        if start_tag in curr_word: rm_chars += len(start_tag)
        if end_tag in curr_word: rm_chars += len(end_tag)

        result = Token(
            curr_word,
            self.labelled_cursor + (len(start_tag) if curr_word.startswith(start_tag) else 0),
            self.raw_cursor,
        )

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
        )

def test(data):
	for i, token_vector in enumerate(data):

		text = getDocumentContent(token_vector['fid'])
		vector_val = token_vector['isStartOfSentence']
		all_indices = [m.start() for m in re.finditer(token_vector['token'], text)]
		if token_vector['position'] in all_indices:
			feature_val = int(isStartOfSentence(token_vector['position'], text))
		else:
			print('ALL INDICES', '--' + token_vector['token'] + '--' , all_indices)

		if vector_val != feature_val:
			print(token_vector['token'], vector_val, feature_val, token_vector['position'])
			return False

	return True

class Tokenizer:

	def __init__(self, fname):

		self.fname = fname
		self.fidentifier = self.fname.split('/')[-1].strip('.txt')

		self.fcontents = None	
		self.tokens = [] # Contains all 1,2,3..maximum_len words tokens
		self.filtered_tokens = [] # Only all capitalized tokens

		with open(fname,'r') as f:
			self.fcontents = f.read()
			
	def get_label(self, word):
		# Returns label 0 (Not an entity) or 1 (Is an entity) -- <b>Elon Musk</b>
		entity_word = re.search("(.*)" + UnigramIterator.START_TAG + "(.+?)" + UnigramIterator.END_TAG + "(.*)", word)
		if entity_word:
			if re.findall(r"\w+", entity_word.groups()[0]) or re.findall(r"\w+", entity_word.groups()[-1]):
				return 0
			return 1

		# -- <b>Elon
		entity_word = re.search("(.*)" + UnigramIterator.START_TAG + "(.*)", word)
		if entity_word:
			if re.findall(r"\w+", entity_word.groups()[0]):
				return 0
			return 1

		# -- Musk</b>
		entity_word = re.search("(.*)" + UnigramIterator.END_TAG + "(.*)", word)
		if entity_word:
			if re.findall(r"\w+", entity_word.groups()[-1]):
				return 0
			return 1

		return 0

	@classmethod
	def clean(self, token):
		# Remove the start and end tags
		return token.replace(UnigramIterator.START_TAG, '').replace(UnigramIterator.END_TAG, '')

	def tokenize(self, maximum_len=4):

		for curr_len in range(1, maximum_len + 1):
			word_iterator = NgramIterator(self.fcontents, curr_len)
			for token in list(word_iterator):
				curr_label = self.get_label(token.string)
				self.tokens.append((self.fidentifier, self.clean(token.string), token.raw_pos, curr_label))

		return self.tokens

	def filter_tokens(self):
		self.filtered_tokens = []
		for fid, token, tpos, tlabel in self.tokens:
			if allWordsCapitalized(token) and "the" not in token.lower():
				self.filtered_tokens.append((fid, token, tpos, tlabel))
		return self.filtered_tokens

	# def print_tokens(self):
	# 	for fid, t, tp, l in self.filtered_tokens:
	# 		print("{f_id} {label} {token} {token_position}".format(f_id=fid, token=t, token_position=tp, label=l))

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
			token_vector['isLocation'] = int(isLocation(tpos, fcontents))
			token_vector['isPrecededByWords'] = int(isPrecededByWords(tpos, fcontents))
			token_vector['isSucceededByWords'] = int(isSucceededByWords(tpos, fcontents, token))
			# token_vector['allWordsCapitalized'] = int(allWordsCapitalized(token))
			token_vector['endsWithApostropheS'] = int(endsWithApostropheS(token))
			token_vector['endsWithComma'] = int(endsWithComma(token))
			token_vector['numWords'] = int(len(token))
			token_vector['lineContainsPronoun'] = int(lineContainsPronoun(tpos, fcontents))
			token_vector['nextLineContainsPronoun'] = int(nextLineContainsPronoun(tpos, fcontents))
			token_vector['isPreceededByFamilyRelation'] = int(isPreceededByFamilyRelation(tpos, fcontents))
			token_vector['isFollowedByFamilyRelation'] = int(isFollowedByFamilyRelation(tpos, fcontents))
			token_vector['isNearStatementWord'] = int(isNearStatementWord(tpos, fcontents))
			token_vector['isPreceededByNonPersonEntity'] = int(isPreceededByNonPersonEntity(tpos, fcontents))
			token_vector['isFollowedByNonPersonEntity'] = int(isFollowedByNonPersonEntity(tpos, fcontents))

			if tlabel == 1: pos += 1
			else: neg += 1
			# print(token_vector)
			data.append(token_vector)

		return data, pos, neg

all_data = []
all_pos = 0
all_neg = 0

for i in range(1, 301):
	fname = ""
	if i < 10:
		fname = "00" + str(i)
	elif i >= 10 and i < 100:
		fname = "0" + str(i)
	else:
		fname = str(i)
	# print(fname)
	F = Tokenizer("labelled/" + fname + ".txt")
	F.tokenize()
	F.filter_tokens()

	# F.print_tokens()

	d, p, n = F.vectorize()

	[all_data.append(v) for v in d]
	all_pos += p
	all_neg += n

# print(len(all_data), all_pos, all_neg)
df = pd.DataFrame(all_data)
df.to_csv("data.csv")