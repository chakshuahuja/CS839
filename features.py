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

def getDocumentContent(document):
	path = "raw/"
	filename = path + str(document) + ".txt"
	file = open(filename,"r")
	return file.read();

def isContainPrefix(word):
	listOfPrefixes = ["President", "DJ", "Captain", "Adm", "Atty", "Brother", "Capt", "Chief", "Cmdr", "Col", "Dean", "Dr", "Elder", "Father", "Gen", "Gov", "Hon", "Lt Col", "Maj", "MSgt", "Mr", "Mrs", "Ms", "Prince", "Prof", "Rabbi", "Rev", "Sister", "Sir", "Queen"]
	firstWord = word.partition(' ')[0]
	if firstWord in listOfPrefixes:
		return True
	else:
		return False;

def isContainSuffix(word):
	listOfSuffixes = ["II", "III", "IV", "CPA", "DDS", "Esq", "JD", "Jr", "LLD", "MD", "PhD", "Ret", "RN", "Sr", "DO"]
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
		while text[previousWordOffset].isalnum():
			previousWord = text[previousWordOffset] + previousWord
			previousWordOffset = previousWordOffset - 1;
	else:
		previousWord = ""
	return previousWord

def getNextWord(offset, text):
	nextWordOffset = offset
	nextWord = ""
	while text[nextWordOffset].isalnum():
		nextWordOffset = nextWordOffset + 1;
	if text[nextWordOffset] == " ":
		nextWordOffset = nextWordOffset + 1;
		while text[nextWordOffset] != "." and text[nextWordOffset] != " ":
			nextWord = nextWord + text[nextWordOffset]
			nextWordOffset = nextWordOffset + 1
	else:
		nextWord = ""

def isPartial(offset, document):
	text = getDocumentContent(document)
	
	previousWord = getPreviousWord(offset, text)
	nextWord = getNextWord(offset, text)
		
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
	occurences = [i for i in range(len(text)) if text.startswith(word, i)]
	for j in range(len(occurences)):
		newOffset = occurences[j]
		if newOffset == offset:
			continue
		else:
			previousWord = getPreviousWord(newOffset, text)
			nextWord = getNextWord(newOffset, text)
			if allWordsCapitalized(previousWord) or allWordsCapitalized(nextWord):
				return True
	return False


def main():
	text = getDocumentContent(102);
	index = text.index("Martin Scorsese's")
	print(index)
	# isPartial(234, 101)
	# flag = isStartOfSentence(1574, 101)
	# print(flag)
	# flag = isContainSuffix("junior jr")
	# print(flag)
	flag = hasPartialNameOccurence(794, 102, "Martin Scorsese's")
	print(flag)

main()