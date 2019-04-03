import csv, re
aamzon = {}
bnb = {}

def read_and_generate(file_name):
	with open(file_name) as f:
		csv_reader = csv.reader(f, delimiter=',')
		data = list(csv_reader)
		header = data[0]
		rows = data[1:]
		
		D = {i: {h: v for h, v in zip(header, row)} for i, row in enumerate(rows)}
		# print(len(D))
		return D

def read_isbn(file_name):
	isbn = []
	with open(file_name) as f:
		csv_reader = csv.reader(f, delimiter=',')
		data = list(csv_reader)
		header = data[0]
		rows = data[1:]

		D = {i: {h: v for h, v in zip(header, row)} for i, row in enumerate(rows)}
		
		print(D)
		for index in range(len(D)):
			isbn.append(D[index]['isbn13'])
		
		return isbn

isbn = read_isbn('match.csv')
bnb = read_and_generate('barnesAndNoble/barnesAndNoble-final.csv')

# matches = 0
# for ia in range(len(amazon)):
# 	for ib in range(len(bnb)):
# 		if not (re.sub("[^0-9]", "", amazon[ia]["isbn13"]) == re.sub("[^0-9]", "", bnb[ib]["isbn13"])):
# 			# matches += 1
# 			# print(amazon[ia]['title'])
# 			# with open('match.csv', mode='a+') as match_file:
# 			# 	match_writer = csv.writer(match_file, delimiter=',')
# 			# 	#match_writer.writerow(list(amazon[ia].values()))
# 			# 	match_writer.writerow(list(bnb[ib].values()))
# 		# else:
# 			with open('bAndN.csv', mode='a+') as un_match_file:
# 				match_writer = csv.writer(un_match_file, delimiter=',')
# 				match_writer.writerow(list(bnb[ib].values()))
# # print(matches)

num_deleted = 0
for ib in range(len(bnb)):
	if ib % 3 == 0 and not bnb[ib]['isbn13'] in isbn:
		num_deleted += 1
	else:
		with open('bAndN.csv', mode='a+') as new_file:
			writer = csv.writer(new_file, delimiter=',')
			writer.writerow(list(bnb[ib].values()))

