from itertools import accumulate
import re

class Tokenizer:

	start_tag = "<b>"
	end_tag = "</b>"

	def __init__(self, fname):
		self.fname = fname
		self.fidentifier = self.fname.split('/')[-1].strip('.txt')

		self.fcontents = None	
		self.tokens = [] # Contains all 1,2,3..maximum_len words tokens

		with open(fname,'r') as f:
			self.fcontents = f.read()
			
	def get_label(self, word):
		# Returns label 0 (Not an entity) or 1 (Is an entity)
		entity_word = re.search("(.*)" + Tokenizer.start_tag + "(.+?)" + Tokenizer.end_tag + "(.*)", word)
		if entity_word:
			print(entity_word.groups())
			if re.findall(r"\w+", entity_word.groups()[0]) or re.findall(r"\w+", entity_word.groups()[-1]):
				return 0
			return 1

		return 0

	def clean_token(self, token):
		# Remove the start and end tags
		return token.replace(Tokenizer.start_tag, '').replace(Tokenizer.end_tag, '')

	def get_offset(self, start_tag_count, end_tag_count):
		return len(Tokenizer.start_tag) * start_tag_count - len(Tokenizer.end_tag) * end_tag_count

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

				curr_start_tag += curr_token.count(Tokenizer.start_tag)
				curr_end_tag += curr_token.count(Tokenizer.end_tag)

				self.tokens.append((curr_token, curr_location, curr_label))

		return self.tokens

	def print_tokens(self):
		for t, tp, l in self.tokens:
			print("{f_id} {label} {token} {token_position}".format(f_id=self.fidentifier, token=t, token_position=tp, label=l))

F = Tokenizer("/Users/chakshu/CSMadison839/002.txt")
F.tokenize()
F.print_tokens()
