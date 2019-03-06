def removeSpecialCharacter(word):
	cleanString = "";
	for ch in word:
		if ch.isalnum() or ch == " ":
			cleanString = cleanString + str(ch)
	return cleanString

def removeApostrophS(word):
	word = word.replace("'s", "")
	return word

def getDocumentContent(document):
	path = "raw/"
	filename = path + str(document) + ".txt"
	file = open(filename,"r")
	return file.read();

def isStartOfSentence(offset, document):
	if(offset == 0):
		return True;
	else:
		text = getDocumentContent(document)
		while offset >= 0:
			offset = offset - 1;
			if text[offset].isalnum():
				return False;
			elif text[offset] == " ":
				continue;
			elif text[offset] == ".":
				return True;


def isContainPrefix(word):
	listOfPrefixes = ["President", "DJ", "Captain", "Adm", "Atty", "Brother", "Capt", "Chief", "Cmdr", "Col", "Dean", "Dr", "Elder", "Father", "Gen", "Gov", "Hon", "Lt Col", "Maj", "MSgt", "Mr", "Mrs", "Ms", "Prince", "Prof", "Rabbi", "Rev", "Sister", "Sir", "Queen"]
	word = removeSpecialCharacter(word)
	firstWord = word.partition(' ')[0]
	if firstWord in listOfPrefixes:
		return True
	else:
		return False;

def isContainSuffix(word):
	listOfSuffixes = ["II", "III", "IV", "CPA", "DDS", "Esq", "JD", "Jr", "LLD", "MD", "PhD", "Ret", "RN", "Sr", "DO"]
	word = removeSpecialCharacter(word)
	lastWord = word.partition(' ')[-1]
	if lastWord in listOfSuffixes:
		return True
	else:
		return False;

def getPreviousWord(offset, text):
	previousWordOffset = offset - 1;
	previousWord = ""
	if text[previousWordOffset] == " ":
		previousWordOffset = previousWordOffset - 1;
		while text[previousWordOffset] != " " and text[previousWordOffset] != ".":
			previousWord = text[previousWordOffset] + previousWord
			previousWordOffset = previousWordOffset - 1;
	else:
		previousWord = ""
	return previousWord, previousWordOffset + 1

def getNextWord(offset, text):
	nextWordOffset = offset
	nextWord = ""
	while text[nextWordOffset] != "." and text[nextWordOffset] != " ":
		nextWordOffset = nextWordOffset + 1;
	if text[nextWordOffset] == " ":
		nextWordOffset = nextWordOffset + 1;
		while text[nextWordOffset] != "." and text[nextWordOffset] != " ":
			nextWord = nextWord + text[nextWordOffset]
			nextWordOffset = nextWordOffset + 1
	else:
		nextWord = ""
	# while text[nextWordOffset] == " " or text[nextWordOffset] == ".":
	# 	nextWordOffset = nextWordOffset + 1
	
	return nextWord, nextWordOffset - len(nextWord)

def isPartial(offset, document):
	text = getDocumentContent(document)
	
	previousWord, previousOffset = getPreviousWord(offset, text)
	nextWord, nextOffset = getNextWord(offset, text)

	previousWord = removeSpecialCharacter(previousWord)
	nextWord = removeSpecialCharacter(nextWord)
		
	return allWordsCapitalized(previousWord) or allWordsCapitalized(nextWord)

def hasPartialNameOccurence(offset, document, word):
	text = getDocumentContent(document)
	splits = word.split(" ");
	if(len(splits) == 1):
		return False
	for j in range(len(splits)):
		word = splits[j]
		i = 0;
		occurences = [i for i in range(len(text)) if text.startswith(word, i)]
		if len(occurences) > 1:
			return True
	return False

def hasFullNameOccurence(offset, document, word):
	splits = word.split(" ");
	if(len(splits) > 1):
		return False;
	text = getDocumentContent(document)
	word = removeApostrophS(word)
	word = removeSpecialCharacter(word)
	occurences = [i for i in range(len(text)) if text.startswith(word, i)]
	for j in range(len(occurences)):
		newOffset = occurences[j]
		if newOffset == offset:
			continue
		else:
			previousWord, previousOffset = getPreviousWord(newOffset, text)
			nextWord, nextOffset = getNextWord(newOffset, text)
			if allWordsCapitalized(previousWord) or allWordsCapitalized(nextWord):
				return True
	return False

def allWordsCapitalized(candidateWord):
	if len(candidateWord) <= 0:
		return False
	words = candidateWord.split()
	for word in words:
		if len(word) > 0 and (not word[0].isupper()):
			return False
	return True

def isLocation(offset, document):
	wordThreshold = 3
	text = getDocumentContent(document);
	locationDict = ["in", "on", "at", "near"]
	for i in range(wordThreshold):
		word, offset = getPreviousWord(offset, text)
		word = word.lower()
		if word != "":
			if word in locationDict:
				return True
		else:
			break;
	return False

def isPrecededByWords(offset, document):
	text = getDocumentContent(document);
	array = ["model", "actor", "actress", "singer", "musician", "star", "stars", "producer", "judges", "soap", "comedian ", "writer", "producer", "pianist", "guitarist", "drummer", "rapper", "activist", "cowriter", "featuring", "introducing", "starring"]
	wordThreshold = 3
	for i in range(wordThreshold):
		word, offset = getPreviousWord(offset, text)
		word = word.lower()
		if word != "":
			word = removeSpecialCharacter(word)
			for ele in array:
				ele = ele.lower()
				if ele.startswith(word):
					return True
		else:
			break;
	return False

def isSucceededByWords(offset, document):
	text = getDocumentContent(document);
	array = ["model", "actor", "actress", "singer", "musician", "star", "stars", "producer", "judges", "soap", "comedian ", "writer", "producer", "pianist", "guitarist", "drummer", "rapper", "activist", "cowriter", "featuring", "introducing", "starring"]
	wordThreshold = 3
	for i in range(wordThreshold):
		word, offset = getNextWord(offset, text)
		word = word.lower()
		if word != "":
			word = removeSpecialCharacter(word)
			for ele in array:
				ele = ele.lower()
				if ele.startswith(word):
					return True
		else:
			break;
	return False

# def getPreviousName(offset, text):
# 	word = ""
# 	offset = offset - 1;
# 	name = ""
# 	flag = True
# 	count = 0;
# 	while flag == True:
# 		while text[offset] != ",":
# 			name = text[offset] + name
# 			# print(name)
# 			offset = offset - 1;
# 		name = name.replace(" and", "")
# 		print(name)
# 		if allWordsCapitalized(name):
# 			count = count + 1;
# 			offset = offset - 1
# 			name = ""
# 		else:
# 			flag = False
# 	if count > 0:
# 		return True
# 	else:
# 		return False



# def partOfMultipleNames(offset, document):
# 	text = getDocumentContent(document);
# 	print(getPreviousName(offset, text))


def main():
	text = getDocumentContent(104);
	index = text.index("Jools Holland")
	# print(partOfMultipleNames(index, 104))
	# print(index)
	# word = "Martin Scorsese's"
	# word = removeApostrophS(word);
	# print(removeSpecialCharacter(word))
	# isPartial(234, 101)
	# flag = isStartOfSentence(1574, 101)
	# print(flag)
	# flag = isContainSuffix("junior jr")
	# print(flag)
	# flag = hasPartialNameOccurence(794, 102, "Martin Scorsese's")
	# print(flag)

main()