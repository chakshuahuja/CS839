import re

pronouns = ["I", "you", "he", "she", "we", "they", "me", "you", "him", "her", "us", "them", "mine", "yours", "his", "hers", "ours", "theirs", "myself", "yourself", "yourselves", "himself", "herself", "ourselves", "themselves", "who", "whom", "whose"];

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
		

print(allWordsCapitalized("Hello there"));
print(allWordsCapitalized("Hello There"));
print(endsWithApostropheS("Hello"));
print(endsWithApostropheS("Hello's"));
print(endsWithComma("Hey There!"));
print(endsWithComma("Hello There ,   "));
print(lineContainsPronoun(51, 101));
print(nextLineContainsPronoun(51, 101));

