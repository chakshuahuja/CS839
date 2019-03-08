from itertools import accumulate
import re
from features import *
import pandas as pd

class Tokenizer:

	start_tag = "<b>"
	end_tag = "</b>"

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
		entity_word = re.search("(.*)" + Tokenizer.start_tag + "(.+?)" + Tokenizer.end_tag + "(.*)", word)
		if entity_word:
			if re.findall(r"\w+", entity_word.groups()[0]) or re.findall(r"\w+", entity_word.groups()[-1]):
				return 0
			return 1

		# -- <b>Elon
		entity_word = re.search("(.*)" + Tokenizer.start_tag + "(.*)", word)
		if entity_word:
			if re.findall(r"\w+", entity_word.groups()[0]):
				return 0
			return 1

		# -- Musk</b>
		entity_word = re.search("(.*)" + Tokenizer.end_tag + "(.*)", word)
		if entity_word:
			if re.findall(r"\w+", entity_word.groups()[-1]):
				return 0
			return 1

		return 0

	def clean_token(self, token):
		# Remove the start and end tags
		return token.replace(Tokenizer.start_tag, '').replace(Tokenizer.end_tag, '')

	def get_offset(self, start_tag_count, end_tag_count):
		return len(Tokenizer.start_tag) * start_tag_count + len(Tokenizer.end_tag) * end_tag_count

	def tokenize(self, maximum_len=4):

		def enumerate_words(s):
			words = re.split(r' |\n', s)
			lens = [len(i) + 1 for i in words]
			from itertools import accumulate
			alens = [0] + list(accumulate(lens))
			zipped = zip(words, alens)
			return [(w, l) for w,l in zipped if len(w) > 0]

		unitokens = list(enumerate_words(self.fcontents))

		for curr_len in range(1, maximum_len + 1):
			# Reset the count of start and end tags
			curr_start_tag = 0
			curr_end_tag = 0

			for tid in range(0, len(unitokens)):
				# TODO: fix for the last overflow cases
				if tid + curr_len > len(unitokens):
					break
				curr_token_location_pair = unitokens[tid:tid+curr_len]
				curr_unprocessed_token = ' '.join([t[0] for t in curr_token_location_pair])

				curr_token = self.clean_token(curr_unprocessed_token)
				curr_location = curr_token_location_pair[0][1] - self.get_offset(curr_start_tag, curr_end_tag)

				curr_label = self.get_label(curr_unprocessed_token)

				curr_start_tag += curr_unprocessed_token.count(Tokenizer.start_tag)
				curr_end_tag += curr_unprocessed_token.count(Tokenizer.end_tag)

				self.tokens.append((self.fidentifier, curr_token, curr_location, curr_label))

		return self.tokens

	def filter_tokens(self):
		self.filtered_tokens = []
		for fid, token, tpos, tlabel in self.tokens:
			if allWordsCapitalized(token):
				self.filtered_tokens.append((fid, token, tpos, tlabel))
		return self.filtered_tokens

	def print_tokens(self):
		for fid, t, tp, l in self.filtered_tokens:
			print("{f_id} {label} {token} {token_position}".format(f_id=fid, token=t, token_position=tp, label=l))

	def vectorize(self):
		data = [] 
		pos, neg = 0, 0

		fcontents = self.clean_token(self.fcontents)

		for fid, token, tpos, tlabel in self.filtered_tokens:
			# print(fid, token, tpos, len(self.clean_token(self.fcontents)))
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
			token_vector['lineContainsPronoun'] = int(lineContainsPronoun(tpos, fcontents))
			token_vector['nextLineContainsPronoun'] = int(nextLineContainsPronoun(tpos, fcontents))
			token_vector['isPreceededByFamilyRelation'] = int(isPreceededByFamilyRelation(tpos, fcontents))
			token_vector['isFollowedByFamilyRelation'] = int(isFollowedByFamilyRelation(tpos, fcontents))
			token_vector['isNearStatementWord'] = int(isNearStatementWord(tpos, fcontents))
			token_vector['isPreceededByNonPersonEntity'] = int(isPreceededByNonPersonEntity(tpos, fcontents))
			token_vector['isFollowedByNonPersonEntity'] = int(isFollowedByNonPersonEntity(tpos, fcontents))

			if tlabel == 1: pos += 1
			else: neg += 1
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
print(len(all_data), all_pos, all_neg)
df = pd.DataFrame(all_data)
df.to_csv("data.csv")