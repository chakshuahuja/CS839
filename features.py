import re

pronouns = ["I", "you", "he", "she", "we", "they", "me", "you", "him", "her", "us", "them", "mine", "yours", "his", "hers", "ours", "theirs", "myself", "yourself", "yourselves", "himself", "herself", "ourselves", "themselves", "who", "whom", "whose"]
familyRelations = ["brother", "sister", "wife", "husband", "friend", "mother", "father", "son", "daughter", "uncle", "aunt", "worker", "neighbor", "neighbour", "sibling", "niece", "nephew", "cousin", "child", "children", "spouse", "mate", "person", "boy", "girl", "man", "woman", "partner"]
statementWords = ["say", "said", "told", "state", "comment", "replied", "added", "laugh", "joke", "assure", "adds", "tell", "direct", "explain", "mention", "answer", "respond", "speak", "declare", "announce", "remark", "note", "claim", "maintain", "assert", "allege", "affirm", "reveal", "affirm", "express", "convey", "disclose", "suggest"]
nonPersonEntityTypes = ["comedy", "thriller", "drama", "award", "program", "book", "court", "school", "song", "album", "band", "movie", "film", "show", "orchestra", "location", "company", "novel", "place", "park", "hotel", "group", "country", "festival", "county", "weekly", "magazine"]
occupationWords = ["student", "teacher", "director", "executive", "family", "publicist", "guest","icon", "officer", "scientist","contestant", "controller", "cricketer", "including", "include", "assistant", "manager", "player", "dancer", "butler", "owner", "name", "model", "actor", "actress", "singer", "musician", "star", "host", "chair", "stars", "producer", "judge", "veteran", "hero", "lawyer", "leader", "judges", "soap", "comedian", "writer", "producer", "pianist", "guitarist", "drummer", "rapper", "activist", "presenter", "cowriter", "cast", "featuring", "introducing", "starring", "late", "legend", "DJ", "creator", "editor", "critic", "contender"]
commonWords = ["a", "ability", "able", "about", "above", "accept", "according", "account", "across", "act", "action", "activity", "actually", "add", "address", "administration", "admit", "adult", "affect", "after", "again", "against", "age", "agency", "agent", "ago", "agree", "agreement", "ahead", "air", "all", "allow", "almost", "alone", "along", "already", "also", "although", "always", "American", "among", "amount", "analysis", "and", "animal", "another", "answer", "any", "anyone", "anything", "appear", "apply", "approach", "area", "argue", "arm", "around", "arrive", "art", "article", "artist", "as", "ask", "assume", "at", "attack", "attention", "attorney", "audience", "author", "authority", "available", "avoid", "away", "baby", "back", "bad", "bag", "ball", "bank", "bar", "base", "be", "beat", "beautiful", "because", "become", "bed", "before", "begin", "behavior", "behind", "believe", "benefit", "best", "better", "between", "beyond", "big", "bill", "billion", "bit", "black", "blood", "blue", "board", "body", "book", "born", "both", "box", "boy", "break", "bring", "brother", "budget", "build", "building", "business", "but", "buy", "by", "call", "camera", "campaign", "can", "cancer", "candidate", "capital", "car", "card", "care", "career", "carry", "case", "catch", "cause", "cell", "center", "central", "century", "certain", "certainly", "chair", "challenge", "chance", "change", "character", "charge", "check", "child", "choice", "choose", "church", "citizen", "city", "civil", "claim", "class", "clear", "clearly", "close", "coach", "cold", "collection", "college", "color", "come", "commercial", "common", "community", "company", "compare", "computer", "concern", "condition", "conference", "Congress", "consider", "consumer", "contain", "continue", "control", "cost", "could", "country", "couple", "course", "court", "cover", "create", "crime", "cultural", "culture", "cup", "current", "customer", "cut", "dark", "data", "daughter", "day", "dead", "deal", "death", "debate", "decade", "decide", "decision", "deep", "defense", "degree", "Democrat", "democratic", "describe", "design", "despite", "detail", "determine", "develop", "development", "die", "difference", "different", "difficult", "dinner", "direction", "director", "discover", "discuss", "discussion", "disease", "do", "doctor", "dog", "door", "down", "draw", "dream", "drive", "drop", "drug", "during", "each", "early", "east", "easy", "eat", "economic", "economy", "edge", "education", "effect", "effort", "eight", "either", "election", "else", "employee", "end", "energy", "enjoy", "enough", "enter", "entire", "environment", "environmental", "especially", "establish", "even", "evening", "event", "ever", "every", "everybody", "everyone", "everything", "evidence", "exactly", "example", "executive", "exist", "expect", "experience", "expert", "explain", "eye", "face", "fact", "factor", "fail", "fall", "family", "far", "fast", "father", "fear", "federal", "feel", "feeling", "few", "field", "fight", "figure", "fill", "film", "final", "finally", "financial", "find", "fine", "finger", "finish", "fire", "firm", "first", "fish", "five", "floor", "fly", "focus", "follow", "food", "foot", "for", "force", "foreign", "forget", "form", "former", "forward", "four", "free", "friend", "from", "front", "full", "fund", "future", "game", "garden", "gas", "general", "generation", "get", "girl", "give", "glass", "go", "goal", "good", "government", "great", "green", "ground", "group", "grow", "growth", "guess", "gun", "guy", "hair", "half", "hand", "hang", "happen", "happy", "hard", "have", "he", "head", "health", "hear", "heart", "heat", "heavy", "help", "her", "here", "herself", "high", "him", "himself", "his", "history", "hit", "hold", "home", "hope", "hospital", "hot", "hotel", "hour", "house", "how", "however", "huge", "human", "hundred", "husband", "I", "idea", "identify", "if", "image", "imagine", "impact", "important", "improve", "in", "include", "including", "increase", "indeed", "indicate", "individual", "industry", "information", "inside", "instead", "institution", "interest", "interesting", "international", "interview", "into", "investment", "involve", "issue", "it", "item", "its", "itself", "job", "join", "just", "keep", "key", "kid", "kill", "kind", "kitchen", "know", "knowledge", "land", "language", "large", "last", "late", "later", "laugh", "law", "lawyer", "lay", "lead", "leader", "learn", "least", "leave", "left", "leg", "legal", "less", "let", "letter", "level", "lie", "life", "light", "like", "likely", "line", "list", "listen", "little", "live", "local", "long", "look", "lose", "loss", "lot", "love", "low", "machine", "magazine", "main", "maintain", "major", "majority", "make", "man", "manage", "management", "manager", "many", "market", "marriage", "material", "matter", "may", "maybe", "me", "mean", "measure", "media", "medical", "meet", "meeting", "member", "memory", "mention", "message", "method", "middle", "might", "military", "million", "mind", "minute", "miss", "mission", "model", "modern", "moment", "money", "month", "more", "morning", "most", "mother", "mouth", "move", "movement", "movie", "Mr", "Mrs", "much", "music", "must", "my", "myself", "name", "nation", "national", "natural", "nature", "near", "nearly", "necessary", "need", "network", "never", "new", "news", "newspaper", "next", "nice", "night", "no", "none", "nor", "north", "not", "note", "nothing", "notice", "now", "n't", "number", "occur", "of", "off", "offer", "office", "officer", "official", "often", "oh", "oil", "ok", "old", "on", "once", "one", "only", "onto", "open", "operation", "opportunity", "option", "or", "order", "organization", "other", "others", "our", "out", "outside", "over", "own", "owner", "page", "pain", "painting", "paper", "parent", "part", "participant", "particular", "particularly", "partner", "party", "pass", "past", "patient", "pattern", "pay", "peace", "people", "per", "perform", "performance", "perhaps", "period", "person", "personal", "phone", "physical", "pick", "picture", "piece", "place", "plan", "plant", "play", "player", "PM", "point", "police", "policy", "political", "politics", "poor", "popular", "population", "position", "positive", "possible", "power", "practice", "prepare", "present", "president", "pressure", "pretty", "prevent", "price", "private", "probably", "problem", "process", "produce", "product", "production", "professional", "professor", "program", "project", "property", "protect", "prove", "provide", "public", "pull", "purpose", "push", "put", "quality", "question", "quickly", "quite", "race", "radio", "raise", "range", "rate", "rather", "reach", "read", "ready", "real", "reality", "realize", "really", "reason", "receive", "recent", "recently", "recognize", "record", "red", "reduce", "reflect", "region", "relate", "relationship", "religious", "remain", "remember", "remove", "report", "represent", "Republican", "require", "research", "resource", "respond", "response", "responsibility", "rest", "result", "return", "reveal", "rich", "right", "rise", "risk", "road", "rock", "role", "room", "rule", "run", "safe", "same", "save", "say", "scene", "school", "science", "scientist", "score", "sea", "season", "seat", "second", "section", "security", "see", "seek", "seem", "sell", "send", "senior", "sense", "series", "serious", "serve", "service", "set", "seven", "several", "sex", "sexual", "shake", "share", "she", "shoot", "short", "shot", "should", "shoulder", "show", "side", "sign", "significant", "similar", "simple", "simply", "since", "sing", "single", "sister", "sit", "site", "situation", "six", "size", "skill", "skin", "small", "smile", "so", "social", "society", "soldier", "some", "somebody", "someone", "something", "sometimes", "son", "song", "soon", "sort", "sound", "source", "south", "southern", "space", "speak", "special", "specific", "speech", "spend", "sport", "spring", "staff", "stage", "stand", "standard", "star", "start", "state", "statement", "station", "stay", "step", "still", "stock", "stop", "store", "story", "strategy", "street", "strong", "structure", "student", "study", "stuff", "style", "subject", "success", "successful", "such", "suddenly", "suffer", "suggest", "summer", "support", "sure", "surface", "system", "table", "take", "talk", "task", "tax", "teach", "teacher", "team", "technology", "television", "tell", "ten", "tend", "term", "test", "than", "thank", "that", "the", "their", "them", "themselves", "then", "theory", "there", "these", "they", "thing", "think", "third", "this", "those", "though", "thought", "thousand", "threat", "three", "through", "throughout", "throw", "thus", "time", "to", "today", "together", "tonight", "too", "top", "total", "tough", "toward", "town", "trade", "traditional", "training", "travel", "treat", "treatment", "tree", "trial", "trip", "trouble", "true", "truth", "try", "turn", "TV", "two", "type", "under", "understand", "unit", "until", "up", "upon", "us", "use", "usually", "value", "various", "very", "victim", "view", "violence", "visit", "voice", "vote", "wait", "walk", "wall", "want", "war", "watch", "water", "way", "we", "weapon", "wear", "week", "weight", "well", "west", "western", "what", "whatever", "when", "where", "whether", "which", "while", "white", "who", "whole", "whom", "whose", "why", "wide", "wife", "will", "win", "wind", "window", "wish", "with", "within", "without", "woman", "wonder", "word", "work", "worker", "world", "worry", "would", "write", "writer", "wrong", "yard", "yeah", "year", "yes", "yet", "you", "young", "your", "yourself"]
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

def containsCommonWord(word):
	array = word.split(" ")
	for i in range(len(array)):
		word = array[i].lower()
		if word in commonWords:
			return True
	return False

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
	listOfPrefixes = ["President", "DJ", "Captain", "Adm", "Atty", "Brother", "Capt", "Chief", "Cmdr", "Col", "Dean", "Dr", "Elder", "Father", "Gen", "Gov", "Hon", "Lt Col", "Maj", "MSgt", "Mr", "Mrs", "Ms", "Prince", "Prof", "Rabbi", "Rev", "Sister", "Sir", "Queen", "Reverend"]
	word = removeSpecialCharacter(word)
	firstWord = word.partition(' ')[0]
	if firstWord in listOfPrefixes:
		return True
	else:
		return False;

def isPrecededByBy(offset, text):
	word, offset = getPreviousWord(offset, text)
	if word == "by":
		return True
	else:
		return False

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
	locationDict = ["in", "on", "at", "near", "around", "of"]
	for i in range(wordThreshold):
		word, offset = getPreviousWord(offset, text)
		word = word.lower()
		if word != "":
			if word in locationDict:
				return True
		else:
			break;
	return False

def isPrecededByOccupationWords(offset, text):
	array = occupationWords
	wordThreshold = 5
	for i in range(wordThreshold):
		word, offset = getPreviousWord(offset, text)
		word = removeSpecialCharacter(word.strip())
		word = word.lower()
		if word != "":
			# ignoring words that start with an upper case and are not the 
			# first word (though the first word considered here may also not be the actual first word)
			if word[0].isupper() and i > 1:
				return (False, -1 * wordThreshold)
			for ele in array:
				ele = ele.lower()
				if ele in word:
					return (True, i)
		else:
			break;
	return (False, -1 * wordThreshold)

def isSucceededByOccupationWords(offset, text, word):
	array = occupationWords
	wordThreshold = 5
	offset = offset + len(word)
	for i in range(wordThreshold):
		word, offset = getNextWord(offset, text)
		word = removeSpecialCharacter(word.strip())
		word = word.lower()
		if word != "":
			# ignoring words that start with caps (what about cases like Chicago Film Festival)
			if word[0].isupper():
				return (False, -1 * wordThreshold)
			for ele in array:
				ele = ele.lower()
				if ele in word:
					return (True, i)
		else:
			break;
	return (False, -1 * wordThreshold)


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
		return lastWord.endswith("'s") or lastWord.endswith("s'")
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
# 	text = getDocumentContent(133);
# 	index = text.index("Mariah Carey")
# 	print(isPrecededByOccupationWords(index, text))
	# print(partOfMultipleNames(index, 104))
	# print(index)
	# word = "Martin Scorsese's"
	# word = removeApostrophS(word);
	# print(removeSpecialCharacter(word))
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
