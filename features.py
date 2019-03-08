import re

pronouns = ["I", "you", "he", "she", "we", "they", "me", "you", "him", "her", "us", "them", "mine", "yours", "his", "hers", "ours", "theirs", "myself", "yourself", "yourselves", "himself", "herself", "ourselves", "themselves", "who", "whom", "whose"]
familyRelations = ["brother", "sister", "wife", "husband", "friend", "mother", "father", "son", "daughter", "uncle", "aunt", "worker", "neighbor", "neighbour", "sibling", "niece", "nephew", "cousin", "child", "children", "spouse", "mate", "person", "boy", "girl", "man", "woman", "partner"]
statementWords = ["say", "said", "told", "state", "comment", "replied", "added", "laugh", "joke", "assure", "adds", "tell", "direct", "explain", "mention", "answer", "respond", "speak", "declare", "announce", "remark", "note", "claim", "maintain", "assert", "allege", "affirm", "reveal", "affirm", "express", "convey", "disclose", "suggest"]
nonPersonEntityTypes = ["comedy", "thriller", "drama", "award", "program", "book", "court", "school", "song", "album", "band", "movie", "film", "show", "orchestra", "location", "company", "novel", "place", "park", "hotel", "group", "country", "festival", "county"]
occupationWords = ["director", "executive", "family", "publicist", "guest","icon", "officer", "scientist","contestant", "controller", "cricketer", "assistant", "manager", "player", "dancer", "butler", "owner", "name", "model", "actor", "actress", "singer", "musician", "star", "host", "chair", "stars", "producer", "judge", "veteran", "hero", "lawyer", "leader", "judges", "soap", "comedian", "writer", "producer", "pianist", "guitarist", "drummer", "rapper", "activist", "presenter", "cowriter", "cast", "featuring", "introducing", "starring", "late", "legend", "DJ", "creator", "editor", "critic", "contender"]

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

def isStartOfSentence(offset, text):
	if(offset == 0):
		return True;
	else:
		while offset >= 0:
			offset = offset - 1;
			if text[offset].isalnum():
				return False;
			elif text[offset] == " ":
				continue;
			elif text[offset] == ".":
				return True;
	return False

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
		while text[previousWordOffset] != " " and text[previousWordOffset] != "." and text[previousWordOffset] != "\n":
			previousWord = text[previousWordOffset] + previousWord
			previousWordOffset = previousWordOffset - 1;
	else:
		previousWord = ""
	return previousWord, previousWordOffset + 1

def getNextWord(offset, text):
	nextWordOffset = offset
	nextWord = ""
	length = len(text)
	while nextWordOffset < length and text[nextWordOffset] != "." and text[nextWordOffset] != " "  and text[nextWordOffset] != "\n":
		nextWordOffset = nextWordOffset + 1;
	if nextWordOffset < length and text[nextWordOffset] == " ":
		nextWordOffset = nextWordOffset + 1;
		while nextWordOffset < length and text[nextWordOffset] != "." and text[nextWordOffset] != " " and text[nextWordOffset] != "\n":
			nextWord = nextWord + text[nextWordOffset]
			nextWordOffset = nextWordOffset + 1
	else:
		nextWord = ""
	# while text[nextWordOffset] == " " or text[nextWordOffset] == ".":
	# 	nextWordOffset = nextWordOffset + 1
	
	return nextWord, nextWordOffset - len(nextWord)

def isPartial(offset, text, word):
	previousWord, previousOffset = getPreviousWord(offset, text)
	offset = offset + len(word)
	nextWord, nextOffset = getNextWord(offset, text)

	previousWord = removeSpecialCharacter(previousWord)
	nextWord = removeSpecialCharacter(nextWord)
		
	return allWordsCapitalized(previousWord) or allWordsCapitalized(nextWord)

def hasPartialNameOccurence(offset, text, word):
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

def hasFullNameOccurence(offset, text, word):
	splits = word.split(" ");
	if(len(splits) > 1):
		return False;
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

def isLocation(offset, text):
	wordThreshold = 3
	locationDict = ["in", "on", "at", "near", "around"]
	for i in range(wordThreshold):
		word, offset = getPreviousWord(offset, text)
		word = word.lower()
		if word != "":
			if word in locationDict:
				return True
		else:
			break;
	return False

def isPrecededByWords(offset, text):
	array = occupationWords
	wordThreshold = 3
	for i in range(wordThreshold):
		word, offset = getPreviousWord(offset, text)
		word = word.lower().strip()
		if word != "":
			word = removeSpecialCharacter(word)
			for ele in array:
				ele = ele.lower()
				if ele.startswith(word):
					return True
		else:
			break;
	return False

def isSucceededByWords(offset, text, word):
	array = occupationWords
	wordThreshold = 3
	offset = offset + len(word)
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

def allWordsCapitalized(candidateWord):
	if len(candidateWord) <= 0:
		return False
	words = candidateWord.split()
	for word in words:
		if len(word) > 0 and (not word[0].isupper()):
			return False
	return True



def endsWithApostropheS(candidateWord):
	words = candidateWord.split()
	if len(words) > 0:
		lastWord = (words[len(words) - 1]).strip()
		return lastWord.endswith("'s")
	return False	


def endsWithComma(candidateWord):
	return candidateWord.strip().endswith(",")

def lineContainsPronoun(offset, content):
	
	lineStartIndex = offset
	while(lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.']):
		lineStartIndex = lineStartIndex - 1
	
	lineEndIndex = offset
	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.']):
		lineEndIndex = lineEndIndex + 1
	
	currentLine = content[lineStartIndex:lineEndIndex + 1]

	currentLineWords = currentLine.split()
	for word in currentLineWords:
		word = word.strip()
		re.sub(r'\W+', '', word).lower()	
		if word in pronouns:
			return True
	
	return False
		

def nextLineContainsPronoun(offset, content):
	lineStartIndex = offset
	while(lineStartIndex < len(content) - 1 and content[lineStartIndex] not in ['\n', '.']):
		lineStartIndex = lineStartIndex + 1
	
	while(lineStartIndex < len(content) - 1 and not content[lineStartIndex].isalpha()):
		lineStartIndex = lineStartIndex + 1

	lineEndIndex = lineStartIndex + 1
	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.']):
		lineEndIndex = lineEndIndex + 1
	
	
	line = content[lineStartIndex:lineEndIndex + 1]

	words = line.split()
	for word in words:
		word = word.strip()
		re.sub(r'\W+', '', word).lower()
		if word in pronouns:
			return True

	return False
		

def isPreceededByFamilyRelation(offset, content):
	
	lineStartIndex = offset - 1

	while(lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.']):
		lineStartIndex = lineStartIndex - 1
	
	line = content[lineStartIndex:offset + 1]


	words = line.split()
	for word in words:
		word = word.strip()
		for relation in familyRelations:
			if relation in word:
				return True

	return False

def isFollowedByFamilyRelation(offset, content):
	lineEndIndex = offset + 1

	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.']):
		lineEndIndex = lineEndIndex + 1
	
	line = content[offset:lineEndIndex + 1]

	words = line.split()
	for word in words:
		word = word.strip().lower()
		for relation in familyRelations:
			if relation in word:
				return True

	return False

def isNearStatementWord(offset, content):

	lineStartIndex = offset
	numSpaces = 0

	while (lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.'] and numSpaces < 5):
		lineStartIndex = lineStartIndex - 1
		if content[lineStartIndex] == " ":
			numSpaces = numSpaces + 1


	numSpaces = 0
	lineEndIndex = offset + 1

	while (lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.'] and numSpaces < 5):
		lineEndIndex = lineEndIndex + 1
		if content[lineEndIndex] == " ":
			numSpaces = numSpaces + 1

	line = content[lineStartIndex:lineEndIndex + 1]

	words = line.split()
	for word in words:
		word = word.strip().lower()
		for statementWord in statementWords:
			if statementWord in word:
				return True

	return False

def isPreceededByNonPersonEntity(offset, content):

	lineStartIndex = offset
	numSpaces = 0

	while (lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.'] and numSpaces < 5):
		lineStartIndex = lineStartIndex - 1
		if content[lineStartIndex] == " ":
			numSpaces = numSpaces + 1

	line = content[lineStartIndex:offset + 1]

	words = line.split()
	for word in words:
		word = word.strip().lower()
		for entity in nonPersonEntityTypes:
			if entity in word:
				return True

	return False

def isFollowedByNonPersonEntity(offset, content):

	lineEndIndex = offset + 1
	numSpaces = 0
	
	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.'] and numSpaces < 5):
		lineEndIndex = lineEndIndex + 1
		if content[lineEndIndex] == " ":
			numSpaces = numSpaces + 1
	
	line = content[offset:lineEndIndex + 1]

	words = line.split()
	for word in words:
		word = word.strip().lower()
		for entity in nonPersonEntityTypes:
			if entity in word:
				return True

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


# def main():
# 	text = getDocumentContent(104);
# 	index = text.index("Jools Holland")
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
	# print(allWordsCapitalized("Hello there"));
	# print(allWordsCapitalized("Hello There"));
	# print(endsWithApostropheS("Hello"));
	# print(endsWithApostropheS("Hello's"));
	# print(endsWithComma("Hey There!"));
	# print(endsWithComma("Hello There ,   "));
	# print(lineContainsPronoun(51, 101));
	# print(nextLineContainsPronoun(51, 101));
	# print(isPreceededByFamilyRelation(101, 101))
	# print(isFollowedByFamilyRelation(101, 101))
	# print(isNearStatementWord(101, 101))
	# print(isPreceededByNonPersonEntity(101, 101))
	# print(isFollowedByNonPersonEntity(101, 101))

# main()