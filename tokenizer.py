from itertools import accumulate
import re

class Tokenizer:

	def __init__(self, fname):
		self.fname = fname
		self.fidentifier = self.fname.split('/')[-1].strip('.txt')

		self.fcontents = None	
		self.tokens = [] # Contains all 1,2,3..maximum_len words tokens

		with open(fname,'r') as f:
			self.fcontents = f.read()
			

	def tokenize(self, maximum_len=4):

		def enumerate_words(s):
			words = re.split(r' |\n', s)
			lens = [len(i) + 1 for i in words]
			from itertools import accumulate
			alens = [0] + list(accumulate(lens))
			zipped = zip(words, alens)
			return [(w, l) for w,l in zipped if len(w) > 0]

		unitokens = list(enumerate_words(self.fcontents))

		start_tag = "<b>"
		end_tag = "</b>"


		for curr_len in range(1, maximum_len + 1):
			# Reset the count of start and end tags
			curr_start_tag = 0
			curr_end_tag = 0

			for tid in range(0, len(unitokens), curr_len):
				# TODO: fix for the last overflow cases
				print(tid + curr_len)
				curr_token_location_pair = unitokens[tid:tid+curr_len]
				
				curr_token = ' '.join([t[0] for t in curr_token_location_pair]).replace(start_tag, '').replace(end_tag, '')
				curr_location = curr_token_location_pair[0][1] - len(start_tag)*curr_start_tag - len(end_tag)*curr_end_tag

				curr_start_tag += curr_token.count(start_tag)
				curr_end_tag += curr_token.count(end_tag)

				self.tokens.append((curr_token, curr_location))

		return self.tokens

	def print_tokens(self):
		for t, tp in self.tokens:
			print("{f_id} {token} {token_position}".format(f_id=self.fidentifier, token=t, token_position=tp))

F = Tokenizer("/Users/chakshu/CSMadison839/001.txt")
F.tokenize()
F.print_tokens()
