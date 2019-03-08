import re

pronouns = ["I", "you", "he", "she", "we", "they", "me", "you", "him", "her", "us", "them", "mine", "yours", "his", "hers", "ours", "theirs", "myself", "yourself", "yourselves", "himself", "herself", "ourselves", "themselves", "who", "whom", "whose"]
familyRelations = ["brother", "sister", "wife", "husband", "friend", "mother", "father", "son", "daughter", "uncle", "aunt", "worker", "neighbor", "neighbour", "sibling", "niece", "nephew", "cousin", "child", "children", "spouse", "mate", "person"]
statementWords = ["said", "told", "state", "comment", "replied", "added", "laugh", "joke", "assure", "adds", "tell", "direct", "explain", "mention", "answer", "respond", "speak", "declare", "announce", "remark", "note", "claim", "maintain", "assert", "allege", "affirm", "reveal", "affirm", "express", "convey", "disclose", "suggest"]
nonPersonEntityTypes = ["song", "album", "band", "movie", "film", "show", "orchestra", "location", "company", "novel", "place", "park", "hotel", "group", "country", "festival", "county"]

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

def lineContainsPronoun(offset, fileName):
	with open(str(fileName) + ".txt", 'r') as file:
    		content = file.read()
	
	lineStartIndex = offset
	while(lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.']):
		lineStartIndex = lineStartIndex - 1
	
	lineEndIndex = offset
	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.']):
		lineEndIndex = lineEndIndex + 1
	
	currentLine = content[lineStartIndex:lineEndIndex + 1]
	print(currentLine)

	currentLineWords = currentLine.split()
	for word in currentLineWords:
		word = word.strip()
		re.sub(r'\W+', '', word).lower()	
		if word in pronouns:
			print("word found " + word)
			return True
	
	return False
		

def nextLineContainsPronoun(offset, fileName):
	with open(str(fileName) + '.txt', 'r') as file:
		content = file.read()
	
	lineStartIndex = offset
	while(lineStartIndex < len(content) - 1 and content[lineStartIndex] not in ['\n', '.']):
		lineStartIndex = lineStartIndex + 1
	
	while(not content[lineStartIndex].isalpha()):
		lineStartIndex = lineStartIndex + 1

	lineEndIndex = lineStartIndex + 1
	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.']):
		lineEndIndex = lineEndIndex + 1
	
	
	line = content[lineStartIndex:lineEndIndex + 1]
	print(line)

	words = line.split()
	for word in words:
		word = word.strip()
		re.sub(r'\W+', '', word).lower()
		if word in pronouns:
			return True

	return False
		

def isPreceededByFamilyRelation(offset, fileName):
	with open(str(fileName) + '.txt', 'r') as file:
		content = file.read()
	
	lineStartIndex = offset - 1

	while(lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.']):
		lineStartIndex = lineStartIndex - 1
	
	line = content[lineStartIndex:offset + 1]

	print(line)

	words = line.split()
	for word in words:
		word = word.strip()
		for relation in familyRelations:
			if relation in word:
				return True

	return False

def isFollowedByFamilyRelation(offset, fileName):
	with open(str(fileName) + '.txt', 'r') as file:
		content = file.read()
	
	lineEndIndex = offset + 1

	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.']):
		lineEndIndex = lineEndIndex + 1
	
	line = content[offset:lineEndIndex + 1]

	print(line)

	words = line.split()
	for word in words:
		word = word.strip().lower()
		for relation in familyRelations:
			if relation in word:
				return True

	return False

def isNearStatementWord(offset, fileName):
	with open(str(fileName) + '.txt', 'r') as file:
		content = file.read()

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
	
	print(line)

	words = line.split()
	for word in words:
		word = word.strip().lower()
		for statementWord in statementWords:
			if statementWord in word:
				return True

	return False

def isPreceededByNonPersonEntity(offset, fileName):
	with open(str(fileName) + '.txt', 'r') as file:
		content = file.read()

	lineStartIndex = offset
	numSpaces = 0

	while (lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.'] and numSpaces < 5):
		lineStartIndex = lineStartIndex - 1
		if content[lineStartIndex] == " ":
			numSpaces = numSpaces + 1

	line = content[lineStartIndex:offset + 1]

	print(line)

	words = line.split()
	for word in words:
		word = word.strip().lower()
		for entity in nonPersonEntityTypes:
			if entity in word:
				return True

	return False

def isFollowedByNonPersonEntity(offset, fileName):
	with open(str(fileName) + '.txt', 'r') as file:
		content = file.read()
	
	lineEndIndex = offset + 1
	numSpaces = 0
	
	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.'] and numSpaces < 5):
		lineEndIndex = lineEndIndex + 1
		if content[lineEndIndex] == " ":
			numSpaces = numSpaces + 1
	
	line = content[offset:lineEndIndex + 1]

	print(line)

	words = line.split()
	for word in words:
		word = word.strip().lower()
		for entity in nonPersonEntityTypes:
			if entity in word:
				return True

	return False

# print(allWordsCapitalized("Hello there"));
# print(allWordsCapitalized("Hello There"));
# print(endsWithApostropheS("Hello"));
# print(endsWithApostropheS("Hello's"));
# print(endsWithComma("Hey There!"));
# print(endsWithComma("Hello There ,   "));
# print(lineContainsPronoun(51, 101));
# print(nextLineContainsPronoun(51, 101));
print(isPreceededByFamilyRelation(101, 101))
print(isFollowedByFamilyRelation(101, 101))
print(isNearStatementWord(101, 101))
print(isPreceededByNonPersonEntity(101, 101))
print(isFollowedByNonPersonEntity(101, 101))



# def areMoreEntitiesPresentInSentence(offset, text, candidateWord):
# 	word, offsetPrev = getPreviousWord(offset, text)
# 	lowerEncountered = False
# 	while(word != ""):
# 		# print(word, candidateWord)
# 		if not isStartOfSentence(offsetPrev, text) and lowerEncountered == True and word[0].isupper():
# 			return True
# 		lowerEncountered = True
# 		word, offsetPrev = getPreviousWord(offsetPrev, text)
	
# 	word, offsetNext = getNextWord(offset + len(candidateWord), text)
# 	lowerEncountered = False
# 	while(word != ""):
# 		print(word, candidateWord)
# 		if lowerEncountered == True and word[0].isupper():
# 			return True
# 		lowerEncountered = True
# 		word, offsetNext = getNextWord(offset, text)
	
# 	return False
