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
		print(len(D))
		return D


amazon = read_and_generate('Amazon/cleaned.csv')
bnb = read_and_generate('barnesAndNoble/barnesAndNoble-final.csv')

with open('match.csv', mode='w') as csv_file:
	field_names = ['title', 'authors', 'book_format', 'cur_price', 'old_price', 'isbn13', 'publisher', 'publication_date', 'pages', 'product_dimensions']
	writer = csv.DictWriter(csv_file, fieldnames=field_names)
	writer.writeheader()

matches = 0
for ia in range(len(amazon)):
	for ib in range(len(bnb)):
		if re.sub("[^0-9]", "", amazon[ia]["isbn13"]) == re.sub("[^0-9]", "", bnb[ib]["isbn13"]):
			matches += 1
			# print(amazon[ia]['title'])
			with open('match.csv', mode='a+') as match_file:
				field_names = ['title', 'authors', 'book_format', 'cur_price', 'old_price', 'isbn13', 'publisher', 'publication_date', 'pages', 'product_dimensions']
				match_writer = csv.DictWriter(match_file, fieldnames=field_names, delimiter=',', extrasaction='ignore')
				match_writer.writerow(amazon[ia])
				match_writer.writerow(bnb[ib])

print(matches)