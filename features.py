import re

pronouns = ["I", "you", "he", "she", "we", "they", "me", "you", "him", "her", "us", "them", "mine", "yours", "his", "hers", "ours", "theirs", "myself", "yourself", "yourselves", "himself", "herself", "ourselves", "themselves", "who", "whom", "whose"]
familyRelations = ["brother", "sister", "wife", "husband", "friend", "mother", "father", "son", "daughter", "uncle", "aunt", "worker", "neighbor", "neighbour", "sibling", "niece", "nephew", "cousin", "child", "children", "spouse", "mate", "person", "boy", "girl", "man", "woman", "partner"]
statementWords = ["say", "said", "told", "state", "comment", "replied", "added", "laugh", "joke", "assure", "adds", "tell", "direct", "explain", "mention", "answer", "respond", "speak", "declare", "announce", "remark", "note", "claim", "maintain", "assert", "allege", "affirm", "reveal", "affirm", "express", "convey", "disclose", "suggest"]
nonPersonEntityTypes = ["comedy", "thriller", "drama", "award", "program", "book", "court", "school", "song", "album", "band", "movie", "film", "show", "orchestra", "location", "company", "novel", "place", "park", "hotel", "group", "country", "festival", "county", "weekly", "magazine"]
occupationWords = ["student", "teacher", "director", "producers", "executive", "family", "publicist", "guest","icon", "officer", "scientist","contestant", "controller", "cricketer", "including", "include", "assistant", "manager", "player", "dancer", "butler", "owner", "name", "model", "actor", "actress", "singer", "musician", "star", "host", "chair", "stars", "producer", "judge", "veteran", "hero", "lawyer", "leader", "judges", "soap", "comedian", "writer", "producer", "pianist", "guitarist", "drummer", "rapper", "activist", "presenter", "cowriter", "cast", "featuring", "introducing", "starring", "late", "legend", "DJ", "creator", "editor", "critic", "contender"]
commonWords = ["hey", "a", "ability", "chemical", "fiction", "shoes", "pitch", "plot","people", "christmas", "enterprise", "dvd", "tv", "got", "grammy", "entertainment", "pop", "journey", "join", "wants", "vanity", "able", "about", "above", "accept", "according", "account", "across", "act", "action", "activity", "actually", "add", "address", "administration", "admit", "adult", "affect", "after", "again", "against", "age", "agency", "agent", "ago", "agree", "agreement", "ahead", "air", "all", "allow", "almost", "alone", "along", "already", "also", "although", "always", "American", "among", "amount", "analysis", "and", "animal", "another", "answer", "any", "anyone", "anything", "appear", "apply", "approach", "area", "argue", "arm", "around", "arrive", "art", "article", "artist", "as", "ask", "assume", "at", "attack", "attention", "attorney", "audience", "author", "authority", "available", "avoid", "away", "baby", "back", "bad", "bag", "ball", "bank", "bar", "base", "be", "beat", "beautiful", "because", "become", "bed", "before", "begin", "behavior", "behind", "believe", "benefit", "best", "better", "between", "beyond", "big", "bill", "billion", "bit", "black", "blood", "blue", "board", "body", "book", "born", "both", "box", "boy", "break", "bring", "brother", "budget", "build", "building", "business", "but", "buy", "by", "call", "camera", "campaign", "can", "cancer", "candidate", "capital", "car", "card", "care", "career", "carry", "case", "catch", "cause", "cell", "center", "central", "century", "certain", "certainly", "chair", "challenge", "chance", "change", "character", "charge", "check", "child", "choice", "choose", "church", "citizen", "city", "civil", "claim", "class", "clear", "clearly", "close", "coach", "cold", "collection", "college", "color", "come", "commercial", "common", "community", "company", "compare", "computer", "concern", "condition", "conference", "Congress", "consider", "consumer", "contain", "continue", "control", "cost", "could", "country", "couple", "course", "court", "cover", "create", "crime", "cultural", "culture", "cup", "current", "customer", "cut", "dark", "data", "daughter", "day", "dead", "deal", "death", "debate", "decade", "decide", "decision", "deep", "defense", "degree", "Democrat", "democratic", "describe", "design", "despite", "detail", "determine", "develop", "development", "die", "difference", "different", "difficult", "dinner", "direction", "director", "discover", "discuss", "discussion", "disease", "do", "doctor", "dog", "door", "down", "draw", "dream", "drive", "drop", "drug", "during", "each", "early", "east", "easy", "eat", "economic", "economy", "edge", "education", "effect", "effort", "eight", "either", "election", "else", "employee", "end", "energy", "enjoy", "enough", "enter", "entire", "environment", "environmental", "especially", "establish", "even", "evening", "event", "ever", "every", "everybody", "everyone", "everything", "evidence", "exactly", "example", "executive", "exist", "expect", "experience", "expert", "explain", "eye", "face", "fact", "factor", "fail", "fall", "family", "far", "fast", "father", "fear", "federal", "feel", "feeling", "few", "field", "fight", "figure", "fill", "film", "final", "finally", "financial", "find", "fine", "finger", "finish", "fire", "firm", "first", "fish", "five", "floor", "fly", "focus", "follow", "food", "foot", "for", "force", "foreign", "forget", "form", "former", "forward", "four", "free", "friend", "from", "front", "full", "fund", "future", "game", "garden", "gas", "general", "generation", "get", "girl", "give", "glass", "go", "goal", "good", "government", "great", "green", "ground", "group", "grow", "growth", "guess", "gun", "guy", "hair", "half", "hand", "hang", "happen", "happy", "hard", "have", "he", "head", "health", "hear", "heart", "heat", "heavy", "help", "her", "here", "herself", "high", "him", "himself", "his", "history", "hit", "hold", "home", "hope", "hospital", "hot", "hotel", "hour", "house", "how", "however", "huge", "human", "hundred", "husband", "I", "idea", "identify", "if", "image", "imagine", "impact", "important", "improve", "in", "include", "including", "increase", "indeed", "indicate", "individual", "industry", "information", "inside", "instead", "institution", "interest", "interesting", "international", "interview", "into", "investment", "involve", "issue", "it", "item", "its", "itself", "job", "join", "just", "keep", "key", "kid", "kill", "kind", "kitchen", "know", "knowledge", "land", "language", "large", "last", "late", "later", "laugh", "law", "lawyer", "lay", "lead", "leader", "learn", "least", "leave", "left", "leg", "legal", "less", "let", "letter", "level", "lie", "life", "light", "like", "likely", "line", "list", "listen", "little", "live", "local", "long", "look", "lose", "loss", "lot", "love", "low", "machine", "magazine", "main", "maintain", "major", "majority", "make", "man", "manage", "management", "manager", "many", "market", "marriage", "material", "matter", "may", "maybe", "me", "mean", "measure", "media", "medical", "meet", "meeting", "member", "memory", "mention", "message", "method", "middle", "might", "military", "million", "mind", "minute", "miss", "mission", "model", "modern", "moment", "money", "month", "more", "morning", "most", "mother", "mouth", "move", "movement", "movie", "Mr", "Mrs", "much", "music", "must", "my", "myself", "name", "nation", "national", "natural", "nature", "near", "nearly", "necessary", "need", "network", "never", "new", "news", "newspaper", "next", "nice", "night", "no", "none", "nor", "north", "not", "note", "nothing", "notice", "now", "n't", "number", "occur", "of", "off", "offer", "office", "officer", "official", "often", "oh", "oil", "ok", "old", "on", "once", "one", "only", "onto", "open", "operation", "opportunity", "option", "or", "order", "organization", "other", "others", "our", "out", "outside", "over", "own", "owner", "page", "pain", "painting", "paper", "parent", "part", "participant", "particular", "particularly", "partner", "party", "pass", "past", "patient", "pattern", "pay", "peace", "people", "per", "perform", "performance", "perhaps", "period", "person", "personal", "phone", "physical", "pick", "picture", "piece", "place", "plan", "plant", "play", "player", "PM", "point", "police", "policy", "political", "politics", "poor", "popular", "population", "position", "positive", "possible", "power", "practice", "prepare", "present", "president", "pressure", "pretty", "prevent", "price", "private", "probably", "problem", "process", "produce", "product", "production", "professional", "professor", "program", "project", "property", "protect", "prove", "provide", "public", "pull", "purpose", "push", "put", "quality", "question", "quickly", "quite", "race", "radio", "raise", "range", "rate", "rather", "reach", "read", "ready", "real", "reality", "realize", "really", "reason", "receive", "recent", "recently", "recognize", "record", "red", "reduce", "reflect", "region", "relate", "relationship", "religious", "remain", "remember", "remove", "report", "represent", "Republican", "require", "research", "resource", "respond", "response", "responsibility", "rest", "result", "return", "reveal", "rich", "right", "rise", "risk", "road", "rock", "role", "room", "rule", "run", "safe", "same", "save", "say", "scene", "school", "science", "scientist", "score", "sea", "season", "seat", "second", "section", "security", "see", "seek", "seem", "sell", "send", "senior", "sense", "series", "serious", "serve", "service", "set", "seven", "several", "sex", "sexual", "shake", "share", "she", "shoot", "short", "shot", "should", "shoulder", "show", "side", "sign", "significant", "similar", "simple", "simply", "since", "sing", "single", "sister", "sit", "site", "situation", "six", "size", "skill", "skin", "small", "smile", "so", "social", "society", "soldier", "some", "somebody", "someone", "something", "sometimes", "son", "song", "soon", "sort", "sound", "source", "south", "southern", "space", "speak", "special", "specific", "speech", "spend", "sport", "spring", "staff", "stage", "stand", "standard", "star", "start", "state", "statement", "station", "stay", "step", "still", "stock", "stop", "store", "story", "strategy", "street", "strong", "structure", "student", "study", "stuff", "style", "subject", "success", "successful", "such", "suddenly", "suffer", "suggest", "summer", "support", "sure", "surface", "system", "table", "take", "talk", "task", "tax", "teach", "teacher", "team", "technology", "television", "tell", "ten", "tend", "term", "test", "than", "thank", "that", "the", "their", "them", "themselves", "then", "theory", "there", "these", "they", "thing", "think", "third", "this", "those", "though", "thought", "thousand", "threat", "three", "through", "throughout", "throw", "thus", "time", "to", "today", "together", "tonight", "too", "top", "total", "tough", "toward", "town", "trade", "traditional", "training", "travel", "treat", "treatment", "tree", "trial", "trip", "trouble", "true", "truth", "try", "turn", "TV", "two", "type", "under", "understand", "unit", "until", "up", "upon", "us", "use", "usually", "value", "various", "very", "victim", "view", "violence", "visit", "voice", "vote", "wait", "walk", "wall", "want", "war", "watch", "water", "way", "we", "weapon", "wear", "week", "weight", "well", "west", "western", "what", "whatever", "when", "where", "whether", "which", "while", "white", "who", "whole", "whom", "whose", "why", "wide", "wife", "will", "win", "wind", "window", "wish", "with", "within", "without", "woman", "wonder", "word", "work", "worker", "world", "worry", "would", "write", "writer", "wrong", "yard", "yeah", "year", "yes", "yet", "you", "young", "your", "yourself"]
commonFirstNames = ["JAMES", "JOHN", "ROBERT", "MICHAEL", "WILLIAM", "DAVID", "RICHARD", "CHARLES", "JOSEPH", "THOMAS", "CHRISTOPHER", "DANIEL", "PAUL", "MARK", "DONALD", "GEORGE", "KENNETH", "STEVEN", "EDWARD", "BRIAN", "RONALD", "ANTHONY", "KEVIN", "JASON", "MATTHEW", "GARY", "TIMOTHY", "JOSE", "LARRY", "JEFFREY", "FRANK", "SCOTT", "ERIC", "STEPHEN", "ANDREW", "RAYMOND", "GREGORY", "JOSHUA", "JERRY", "DENNIS", "WALTER", "PATRICK", "PETER", "HAROLD", "DOUGLAS", "HENRY", "CARL", "ARTHUR", "RYAN", "ROGER", "JOE", "JUAN", "JACK", "ALBERT", "JONATHAN", "JUSTIN", "TERRY", "GERALD", "KEITH", "SAMUEL", "WILLIE", "RALPH", "LAWRENCE", "NICHOLAS", "ROY", "BENJAMIN", "BRUCE", "BRANDON", "ADAM", "HARRY", "FRED", "WAYNE", "BILLY", "STEVE", "LOUIS", "JEREMY", "AARON", "RANDY", "HOWARD", "EUGENE", "CARLOS", "RUSSELL", "BOBBY", "VICTOR", "MARTIN", "ERNEST", "PHILLIP", "TODD", "JESSE", "CRAIG", "ALAN", "SHAWN", "CLARENCE", "SEAN", "PHILIP", "CHRIS", "JOHNNY", "EARL", "JIMMY", "ANTONIO", "DANNY", "BRYAN", "TONY", "LUIS", "MIKE", "STANLEY", "LEONARD", "NATHAN", "DALE", "MANUEL", "RODNEY", "CURTIS", "NORMAN", "ALLEN", "MARVIN", "VINCENT", "GLENN", "JEFFERY", "TRAVIS", "JEFF", "CHAD", "JACOB", "LEE", "MELVIN", "ALFRED", "KYLE", "FRANCIS", "BRADLEY", "JESUS", "HERBERT", "FREDERICK", "RAY", "JOEL", "EDWIN", "DON", "EDDIE", "RICKY", "TROY", "RANDALL", "BARRY", "ALEXANDER", "BERNARD", "MARIO", "LEROY", "FRANCISCO", "MARCUS", "MICHEAL", "THEODORE", "CLIFFORD", "MIGUEL", "OSCAR", "JAY", "JIM", "TOM", "CALVIN", "ALEX", "JON", "RONNIE", "BILL", "LLOYD", "TOMMY", "LEON", "DEREK", "WARREN", "DARRELL", "JEROME", "FLOYD", "LEO", "ALVIN", "TIM", "WESLEY", "GORDON", "DEAN", "GREG", "JORGE", "DUSTIN", "PEDRO", "DERRICK", "DAN", "LEWIS", "ZACHARY", "COREY", "HERMAN", "MAURICE", "VERNON", "ROBERTO", "CLYDE", "GLEN", "HECTOR", "SHANE", "RICARDO", "SAM", "RICK", "LESTER", "BRENT", "RAMON", "CHARLIE", "TYLER", "GILBERT", "GENE", "MARC", "REGINALD", "RUBEN", "BRETT", "ANGEL", "NATHANIEL", "RAFAEL", "LESLIE", "EDGAR", "MILTON", "RAUL", "BEN", "CHESTER", "CECIL", "DUANE", "FRANKLIN", "ANDRE", "ELMER", "BRAD", "GABRIEL", "RON", "MITCHELL", "ROLAND", "ARNOLD", "HARVEY", "JARED", "ADRIAN", "KARL", "CORY", "CLAUDE", "ERIK", "DARRYL", "JAMIE", "NEIL", "JESSIE", "CHRISTIAN", "JAVIER", "FERNANDO", "CLINTON", "TED", "MATHEW", "TYRONE", "DARREN", "LONNIE", "LANCE", "CODY", "JULIO", "KELLY", "KURT", "ALLAN", "NELSON", "GUY", "CLAYTON", "HUGH", "MAX", "DWAYNE", "DWIGHT", "ARMANDO", "FELIX", "JIMMIE", "EVERETT", "JORDAN", "IAN", "WALLACE", "KEN", "BOB", "JAIME", "CASEY", "ALFREDO", "ALBERTO", "DAVE", "IVAN", "JOHNNIE", "SIDNEY", "BYRON", "JULIAN", "ISAAC", "MORRIS", "CLIFTON", "WILLARD", "DARYL", "ROSS", "VIRGIL", "ANDY", "MARSHALL", "SALVADOR", "PERRY", "KIRK", "SERGIO", "MARION", "TRACY", "SETH", "KENT", "TERRANCE", "RENE", "EDUARDO", "TERRENCE", "ENRIQUE", "FREDDIE", "WADE", "AUSTIN", "STUART", "FREDRICK", "ARTURO", "ALEJANDRO", "JACKIE", "JOEY", "NICK", "LUTHER", "WENDELL", "JEREMIAH", "EVAN", "JULIUS", "DANA", "DONNIE", "OTIS", "SHANNON", "TREVOR", "OLIVER", "LUKE", "HOMER", "GERARD", "DOUG", "KENNY", "HUBERT", "ANGELO", "SHAUN", "LYLE", "MATT", "LYNN", "ALFONSO", "ORLANDO", "REX", "CARLTON", "ERNESTO", "CAMERON", "NEAL", "PABLO", "LORENZO", "OMAR", "WILBUR", "BLAKE", "GRANT", "HORACE", "RODERICK", "KERRY", "ABRAHAM", "WILLIS", "RICKEY", "JEAN", "IRA", "ANDRES", "CESAR", "JOHNATHAN", "MALCOLM", "RUDOLPH", "DAMON", "KELVIN", "RUDY", "PRESTON", "ALTON", "ARCHIE", "MARCO", "WM", "PETE", "RANDOLPH", "GARRY", "GEOFFREY", "JONATHON", "FELIPE", "BENNIE", "GERARDO", "ED", "DOMINIC", "ROBIN", "LOREN", "DELBERT", "COLIN", "GUILLERMO", "EARNEST", "LUCAS", "BENNY", "NOEL", "SPENCER", "RODOLFO", "MYRON", "EDMUND", "GARRETT", "SALVATORE", "CEDRIC", "LOWELL", "GREGG", "SHERMAN", "WILSON", "DEVIN", "SYLVESTER", "KIM", "ROOSEVELT", "ISRAEL", "JERMAINE", "FORREST", "WILBERT", "LELAND", "SIMON", "GUADALUPE", "CLARK", "IRVING", "CARROLL", "BRYANT", "OWEN", "RUFUS", "WOODROW", "SAMMY", "KRISTOPHER", "MACK", "LEVI", "MARCOS", "GUSTAVO", "JAKE", "LIONEL", "MARTY", "TAYLOR", "ELLIS", "DALLAS", "GILBERTO", "CLINT", "NICOLAS", "LAURENCE", "ISMAEL", "ORVILLE", "DREW", "JODY", "ERVIN", "DEWEY", "AL", "WILFRED", "JOSH", "HUGO", "IGNACIO", "CALEB", "TOMAS", "SHELDON", "ERICK", "FRANKIE", "STEWART", "DOYLE", "DARREL", "ROGELIO", "TERENCE", "SANTIAGO", "ALONZO", "ELIAS", "BERT", "ELBERT", "RAMIRO", "CONRAD", "PAT", "NOAH", "GRADY", "PHIL", "CORNELIUS", "LAMAR", "ROLANDO", "CLAY", "PERCY", "DEXTER", "BRADFORD", "MERLE", "DARIN", "AMOS", "TERRELL", "MOSES", "IRVIN", "SAUL", "ROMAN", "DARNELL", "RANDAL", "TOMMIE", "TIMMY", "DARRIN", "WINSTON", "BRENDAN", "TOBY", "VAN", "ABEL", "DOMINICK", "BOYD", "COURTNEY", "JAN", "EMILIO", "ELIJAH", "CARY", "DOMINGO", "SANTOS", "AUBREY", "EMMETT", "MARLON", "EMANUEL", "JERALD", "EDMOND", "EMIL", "DEWAYNE", "WILL", "OTTO", "TEDDY", "REYNALDO", "BRET", "MORGAN", "JESS", "TRENT", "HUMBERTO", "EMMANUEL", "STEPHAN", "LOUIE", "VICENTE", "LAMONT", "STACY", "GARLAND", "MILES", "MICAH", "EFRAIN", "BILLIE", "LOGAN", "HEATH", "RODGER", "HARLEY", "DEMETRIUS", "ETHAN", "ELDON", "ROCKY", "PIERRE", "JUNIOR", "FREDDY", "ELI", "BRYCE", "ANTOINE", "ROBBIE", "KENDALL", "ROYCE", "STERLING", "MICKEY", "CHASE", "GROVER", "ELTON", "CLEVELAND", "DYLAN", "CHUCK", "DAMIAN", "REUBEN", "STAN", "AUGUST", "LEONARDO", "JASPER", "RUSSEL", "ERWIN", "BENITO", "HANS", "MONTE", "BLAINE", "ERNIE", "CURT", "QUENTIN", "AGUSTIN", "MURRAY", "JAMAL", "DEVON", "ADOLFO", "HARRISON", "TYSON", "BURTON", "BRADY", "ELLIOTT", "WILFREDO", "BART", "JARROD", "VANCE", "DENIS", "DAMIEN", "JOAQUIN", "HARLAN", "DESMOND", "ELLIOT", "DARWIN", "ASHLEY", "GREGORIO", "BUDDY", "XAVIER", "KERMIT", "ROSCOE", "ESTEBAN", "ANTON", "SOLOMON", "SCOTTY", "NORBERT", "ELVIN", "WILLIAMS", "NOLAN", "CAREY", "ROD", "QUINTON", "HAL", "BRAIN", "ROB", "ELWOOD", "KENDRICK", "DARIUS", "MOISES", "SON", "MARLIN", "FIDEL", "THADDEUS", "CLIFF", "MARCEL", "ALI", "JACKSON", "RAPHAEL", "BRYON", "ARMAND", "ALVARO", "JEFFRY", "DANE", "JOESPH", "THURMAN", "NED", "SAMMIE", "RUSTY", "MICHEL", "MONTY", "RORY", "FABIAN", "REGGIE", "MASON", "GRAHAM", "KRIS", "ISAIAH", "VAUGHN", "GUS", "AVERY", "LOYD", "DIEGO", "ALEXIS", "ADOLPH", "NORRIS", "MILLARD", "ROCCO", "GONZALO", "DERICK", "RODRIGO", "GERRY", "STACEY", "CARMEN", "WILEY", "RIGOBERTO", "ALPHONSO", "TY", "SHELBY", "RICKIE", "NOE", "VERN", "BOBBIE", "REED", "JEFFERSON", "ELVIS", "BERNARDO", "MAURICIO", "HIRAM", "DONOVAN", "BASIL", "RILEY", "OLLIE", "NICKOLAS", "MAYNARD", "SCOT", "VINCE", "QUINCY", "EDDY", "SEBASTIAN", "FEDERICO", "ULYSSES", "HERIBERTO", "DONNELL", "COLE", "DENNY", "DAVIS", "GAVIN", "EMERY", "WARD", "ROMEO", "JAYSON", "DION", "DANTE", "CLEMENT", "COY", "ODELL", "MAXWELL", "JARVIS", "BRUNO", "ISSAC", "MARY", "DUDLEY", "BROCK", "SANFORD", "COLBY", "CARMELO", "BARNEY", "NESTOR", "HOLLIS", "STEFAN", "DONNY", "ART", "LINWOOD", "BEAU", "WELDON", "GALEN", "ISIDRO", "TRUMAN", "DELMAR", "JOHNATHON", "SILAS", "FREDERIC", "DICK", "KIRBY", "IRWIN", "CRUZ", "MERLIN", "MERRILL", "CHARLEY", "MARCELINO", "LANE", "HARRIS", "CLEO", "CARLO", "TRENTON", "KURTIS", "HUNTER", "AURELIO", "WINFRED", "VITO", "COLLIN", "DENVER", "CARTER", "LEONEL", "EMORY", "PASQUALE", "MOHAMMAD", "MARIANO", "DANIAL", "BLAIR", "LANDON", "DIRK", "BRANDEN", "ADAN", "NUMBERS", "CLAIR", "BUFORD", "GERMAN", "BERNIE", "WILMER", "JOAN", "EMERSON", "ZACHERY", "FLETCHER", "JACQUES", "ERROL", "DALTON", "MONROE", "JOSUE", "DOMINIQUE", "EDWARDO", "BOOKER", "WILFORD", "SONNY", "SHELTON", "CARSON", "THERON", "RAYMUNDO", "DAREN", "TRISTAN", "HOUSTON", "ROBBY", "LINCOLN", "JAME", "GENARO", "GALE", "BENNETT", "OCTAVIO", "CORNELL", "LAVERNE", "HUNG", "ARRON", "ANTONY", "HERSCHEL", "ALVA", "GIOVANNI", "GARTH", "CYRUS", "CYRIL", "RONNY", "STEVIE", "LON", "FREEMAN", "ERIN", "DUNCAN", "KENNITH", "CARMINE", "AUGUSTINE", "YOUNG", "ERICH", "CHADWICK", "WILBURN", "RUSS", "REID", "MYLES", "ANDERSON", "MORTON", "JONAS", "FOREST", "MITCHEL", "MERVIN", "ZANE", "RICH", "JAMEL", "LAZARO", "ALPHONSE", "RANDELL", "MAJOR", "JOHNIE", "JARRETT", "BROOKS", "ARIEL", "ABDUL", "DUSTY", "LUCIANO", "LINDSEY", "TRACEY", "SEYMOUR", "SCOTTIE", "EUGENIO", "MOHAMMED", "SANDY", "VALENTIN", "CHANCE", "ARNULFO", "LUCIEN", "FERDINAND", "THAD", "EZRA", "SYDNEY", "ALDO", "RUBIN", "ROYAL", "MITCH", "EARLE", "ABE", "WYATT", "MARQUIS", "LANNY", "KAREEM", "JAMAR", "BORIS", "ISIAH", "EMILE", "ELMO", "ARON", "LEOPOLDO", "EVERETTE", "JOSEF", "GAIL", "ELOY", "DORIAN", "RODRICK", "REINALDO", "LUCIO", "JERROD", "WESTON", "HERSHEL", "BARTON", "PARKER", "LEMUEL", "LAVERN", "BURT", "JULES", "GIL", "ELISEO", "AHMAD", "NIGEL", "EFREN", "ANTWAN", "ALDEN", "MARGARITO", "COLEMAN", "REFUGIO", "DINO", "OSVALDO", "LES", "DEANDRE", "NORMAND", "KIETH", "IVORY", "ANDREA", "MARY", "PATRICIA", "LINDA", "BARBARA", "ELIZABETH", "JENNIFER", "MARIA", "SUSAN", "MARGARET", "DOROTHY", "LISA", "NANCY", "KAREN", "BETTY", "HELEN", "SANDRA", "DONNA", "CAROL", "RUTH", "SHARON", "MICHELLE", "LAURA", "SARAH", "KIMBERLY", "DEBORAH", "JESSICA", "SHIRLEY", "CYNTHIA", "ANGELA", "MELISSA", "BRENDA", "AMY", "ANNA", "REBECCA", "VIRGINIA", "KATHLEEN", "PAMELA", "MARTHA", "DEBRA", "AMANDA", "STEPHANIE", "CAROLYN", "CHRISTINE", "MARIE", "JANET", "CATHERINE", "FRANCES", "ANN", "JOYCE", "DIANE", "ALICE", "JULIE", "HEATHER", "TERESA", "DORIS", "GLORIA", "EVELYN", "JEAN", "CHERYL", "MILDRED", "KATHERINE", "JOAN", "ASHLEY", "JUDITH", "ROSE", "JANICE", "KELLY", "NICOLE", "JUDY", "CHRISTINA", "KATHY", "THERESA", "BEVERLY", "DENISE", "TAMMY", "IRENE", "JANE", "LORI", "RACHEL", "MARILYN", "ANDREA", "KATHRYN", "LOUISE", "SARA", "ANNE", "JACQUELINE", "WANDA", "BONNIE", "JULIA", "RUBY", "LOIS", "TINA", "PHYLLIS", "NORMA", "PAULA", "DIANA", "ANNIE", "LILLIAN", "EMILY", "ROBIN", "PEGGY", "CRYSTAL", "GLADYS", "RITA", "DAWN", "CONNIE", "FLORENCE", "TRACY", "EDNA", "TIFFANY", "CARMEN", "ROSA", "CINDY", "GRACE", "WENDY", "VICTORIA", "EDITH", "KIM", "SHERRY", "SYLVIA", "JOSEPHINE", "THELMA", "SHANNON", "SHEILA", "ETHEL", "ELLEN", "ELAINE", "MARJORIE", "CARRIE", "CHARLOTTE", "MONICA", "ESTHER", "PAULINE", "EMMA", "JUANITA", "ANITA", "RHONDA", "HAZEL", "AMBER", "EVA", "DEBBIE", "APRIL", "LESLIE", "CLARA", "LUCILLE", "JAMIE", "JOANNE", "ELEANOR", "VALERIE", "DANIELLE", "MEGAN", "ALICIA", "SUZANNE", "MICHELE", "GAIL", "BERTHA", "DARLENE", "VERONICA", "JILL", "ERIN", "GERALDINE", "LAUREN", "CATHY", "JOANN", "LORRAINE", "LYNN", "SALLY", "REGINA", "ERICA", "BEATRICE", "DOLORES", "BERNICE", "AUDREY", "YVONNE", "ANNETTE", "JUNE", "SAMANTHA", "MARION", "DANA", "STACY", "ANA", "RENEE", "IDA", "VIVIAN", "ROBERTA", "HOLLY", "BRITTANY", "MELANIE", "LORETTA", "YOLANDA", "JEANETTE", "LAURIE", "KATIE", "KRISTEN", "VANESSA", "ALMA", "SUE", "ELSIE", "BETH", "JEANNE", "VICKI", "CARLA", "TARA", "ROSEMARY", "EILEEN", "TERRI", "GERTRUDE", "LUCY", "TONYA", "ELLA", "STACEY", "WILMA", "GINA", "KRISTIN", "JESSIE", "NATALIE", "AGNES", "VERA", "WILLIE", "CHARLENE", "BESSIE", "DELORES", "MELINDA", "PEARL", "ARLENE", "MAUREEN", "COLLEEN", "ALLISON", "TAMARA", "JOY", "GEORGIA", "CONSTANCE", "LILLIE", "CLAUDIA", "JACKIE", "MARCIA", "TANYA", "NELLIE", "MINNIE", "MARLENE", "HEIDI", "GLENDA", "LYDIA", "VIOLA", "COURTNEY", "MARIAN", "STELLA", "CAROLINE", "DORA", "JO", "VICKIE", "MATTIE", "TERRY", "MAXINE", "IRMA", "MABEL", "MARSHA", "MYRTLE", "LENA", "CHRISTY", "DEANNA", "PATSY", "HILDA", "GWENDOLYN", "JENNIE", "NORA", "MARGIE", "NINA", "CASSANDRA", "LEAH", "PENNY", "KAY", "PRISCILLA", "NAOMI", "CAROLE", "BRANDY", "OLGA", "BILLIE", "DIANNE", "TRACEY", "LEONA", "JENNY", "FELICIA", "SONIA", "MIRIAM", "VELMA", "BECKY", "BOBBIE", "VIOLET", "KRISTINA", "TONI", "MISTY", "MAE", "SHELLY", "DAISY", "RAMONA", "SHERRI", "ERIKA", "KATRINA", "CLAIRE", "LINDSEY", "LINDSAY", "GENEVA", "GUADALUPE", "BELINDA", "MARGARITA", "SHERYL", "CORA", "FAYE", "ADA", "NATASHA", "SABRINA", "ISABEL", "MARGUERITE", "HATTIE", "HARRIET", "MOLLY", "CECILIA", "KRISTI", "BRANDI", "BLANCHE", "SANDY", "ROSIE", "JOANNA", "IRIS", "EUNICE", "ANGIE", "INEZ", "LYNDA", "MADELINE", "AMELIA", "ALBERTA", "GENEVIEVE", "MONIQUE", "JODI", "JANIE", "MAGGIE", "KAYLA", "SONYA", "JAN", "LEE", "KRISTINE", "CANDACE", "FANNIE", "MARYANN", "OPAL", "ALISON", "YVETTE", "MELODY", "LUZ", "SUSIE", "OLIVIA", "FLORA", "SHELLEY", "KRISTY", "MAMIE", "LULA", "LOLA", "VERNA", "BEULAH", "ANTOINETTE", "CANDICE", "JUANA", "JEANNETTE", "PAM", "KELLI", "HANNAH", "WHITNEY", "BRIDGET", "KARLA", "CELIA", "LATOYA", "PATTY", "SHELIA", "GAYLE", "DELLA", "VICKY", "LYNNE", "SHERI", "MARIANNE", "KARA", "JACQUELYN", "ERMA", "BLANCA", "MYRA", "LETICIA", "PAT", "KRISTA", "ROXANNE", "ANGELICA", "JOHNNIE", "ROBYN", "FRANCIS", "ADRIENNE", "ROSALIE", "ALEXANDRA", "BROOKE", "BETHANY", "SADIE", "BERNADETTE", "TRACI", "JODY", "KENDRA", "JASMINE", "NICHOLE", "RACHAEL", "CHELSEA", "MABLE", "ERNESTINE", "MURIEL", "MARCELLA", "ELENA", "KRYSTAL", "ANGELINA", "NADINE", "KARI", "ESTELLE", "DIANNA", "PAULETTE", "LORA", "MONA", "DOREEN", "ROSEMARIE", "ANGEL", "DESIREE", "ANTONIA", "HOPE", "GINGER", "JANIS", "BETSY", "CHRISTIE", "FREDA", "MERCEDES", "MEREDITH", "LYNETTE", "TERI", "CRISTINA", "EULA", "LEIGH", "MEGHAN", "SOPHIA", "ELOISE", "ROCHELLE", "GRETCHEN", "CECELIA", "RAQUEL", "HENRIETTA", "ALYSSA", "JANA", "KELLEY", "GWEN", "KERRY", "JENNA", "TRICIA", "LAVERNE", "OLIVE", "ALEXIS", "TASHA", "SILVIA", "ELVIRA", "CASEY", "DELIA", "SOPHIE", "KATE", "PATTI", "LORENA", "KELLIE", "SONJA", "LILA", "LANA", "DARLA", "MAY", "MINDY", "ESSIE", "MANDY", "LORENE", "ELSA", "JOSEFINA", "JEANNIE", "MIRANDA", "DIXIE", "LUCIA", "MARTA", "FAITH", "LELA", "JOHANNA", "SHARI", "CAMILLE", "TAMI", "SHAWNA", "ELISA", "EBONY", "MELBA", "ORA", "NETTIE", "TABITHA", "OLLIE", "JAIME", "WINIFRED", "KRISTIE", "MARINA", "ALISHA", "AIMEE", "RENA", "MYRNA", "MARLA", "TAMMIE", "LATASHA", "BONITA", "PATRICE", "RONDA", "SHERRIE", "ADDIE", "FRANCINE", "DELORIS", "STACIE", "ADRIANA", "CHERI", "SHELBY", "ABIGAIL", "CELESTE", "JEWEL", "CARA", "ADELE", "REBEKAH", "LUCINDA", "DORTHY", "CHRIS", "EFFIE", "TRINA", "REBA", "SHAWN", "SALLIE", "AURORA", "LENORA", "ETTA", "LOTTIE", "KERRI", "TRISHA", "NIKKI", "ESTELLA", "FRANCISCA", "JOSIE", "TRACIE", "MARISSA", "KARIN", "BRITTNEY", "JANELLE", "LOURDES", "LAUREL", "HELENE", "FERN", "ELVA", "CORINNE", "KELSEY", "INA", "BETTIE", "ELISABETH", "AIDA", "CAITLIN", "INGRID", "IVA", "EUGENIA", "CHRISTA", "GOLDIE", "CASSIE", "MAUDE", "JENIFER", "THERESE", "FRANKIE", "DENA", "LORNA", "JANETTE", "LATONYA", "CANDY", "MORGAN", "CONSUELO", "TAMIKA", "ROSETTA", "DEBORA", "CHERIE", "POLLY", "DINA", "JEWELL", "FAY", "JILLIAN", "DOROTHEA", "NELL", "TRUDY", "ESPERANZA", "PATRICA", "KIMBERLEY", "SHANNA", "HELENA", "CAROLINA", "CLEO", "STEFANIE", "ROSARIO", "OLA", "JANINE", "MOLLIE", "LUPE", "ALISA", "LOU", "MARIBEL", "SUSANNE", "BETTE", "SUSANA", "ELISE", "CECILE", "ISABELLE", "LESLEY", "JOCELYN", "PAIGE", "JONI", "RACHELLE", "LEOLA", "DAPHNE", "ALTA", "ESTER", "PETRA", "GRACIELA", "IMOGENE", "JOLENE", "KEISHA", "LACEY", "GLENNA", "GABRIELA", "KERI", "URSULA", "LIZZIE", "KIRSTEN", "SHANA", "ADELINE", "MAYRA", "JAYNE", "JACLYN", "GRACIE", "SONDRA", "CARMELA", "MARISA", "ROSALIND", "CHARITY", "TONIA", "BEATRIZ", "MARISOL", "CLARICE", "JEANINE", "SHEENA", "ANGELINE", "FRIEDA", "LILY", "ROBBIE", "SHAUNA", "MILLIE", "CLAUDETTE", "CATHLEEN", "ANGELIA", "GABRIELLE", "AUTUMN", "KATHARINE", "SUMMER", "JODIE", "STACI", "LEA", "CHRISTI", "JIMMIE", "JUSTINE", "ELMA", "LUELLA", "MARGRET", "DOMINIQUE", "SOCORRO", "RENE", "MARTINA", "MARGO", "MAVIS", "CALLIE", "BOBBI", "MARITZA", "LUCILE", "LEANNE", "JEANNINE", "DEANA", "AILEEN", "LORIE", "LADONNA", "WILLA", "MANUELA", "GALE", "SELMA", "DOLLY", "SYBIL", "ABBY", "LARA", "DALE", "IVY", "DEE", "WINNIE", "MARCY", "LUISA", "JERI", "MAGDALENA", "OFELIA", "MEAGAN", "AUDRA", "MATILDA", "LEILA", "CORNELIA", "BIANCA", "SIMONE", "BETTYE", "RANDI", "VIRGIE", "LATISHA", "BARBRA", "GEORGINA", "ELIZA", "LEANN", "BRIDGETTE", "RHODA", "HALEY", "ADELA", "NOLA", "BERNADINE", "FLOSSIE", "ILA", "GRETA", "RUTHIE", "NELDA", "MINERVA", "LILLY", "TERRIE", "LETHA", "HILARY", "ESTELA", "VALARIE", "BRIANNA", "ROSALYN", "EARLINE", "CATALINA", "AVA", "MIA", "CLARISSA", "LIDIA", "CORRINE", "ALEXANDRIA", "CONCEPCION", "TIA", "SHARRON", "RAE", "DONA", "ERICKA", "JAMI", "ELNORA", "CHANDRA", "LENORE", "NEVA", "MARYLOU", "MELISA", "TABATHA", "SERENA", "AVIS", "ALLIE", "SOFIA", "JEANIE", "ODESSA", "NANNIE", "HARRIETT", "LORAINE", "PENELOPE", "MILAGROS", "EMILIA", "BENITA", "ALLYSON", "ASHLEE", "TANIA", "TOMMIE", "ESMERALDA", "KARINA", "EVE", "PEARLIE", "ZELMA", "MALINDA", "NOREEN", "TAMEKA", "SAUNDRA", "HILLARY", "AMIE", "ALTHEA", "ROSALINDA", "JORDAN", "LILIA", "ALANA", "GAY", "CLARE", "ALEJANDRA", "ELINOR", "MICHAEL", "LORRIE", "JERRI", "DARCY", "EARNESTINE", "CARMELLA", "TAYLOR", "NOEMI", "MARCIE", "LIZA", "ANNABELLE", "LOUISA", "EARLENE", "MALLORY", "CARLENE", "NITA", "SELENA", "TANISHA", "KATY", "JULIANNE", "JOHN", "LAKISHA", "EDWINA", "MARICELA", "MARGERY", "KENYA", "DOLLIE", "ROXIE", "ROSLYN", "KATHRINE", "NANETTE", "CHARMAINE", "LAVONNE", "ILENE", "KRIS", "TAMMI", "SUZETTE", "CORINE", "KAYE", "JERRY", "MERLE", "CHRYSTAL", "LINA", "DEANNE", "LILIAN", "JULIANA", "ALINE", "LUANN", "KASEY", "MARYANNE", "EVANGELINE", "COLETTE", "MELVA", "LAWANDA", "YESENIA", "NADIA", "MADGE", "KATHIE", "EDDIE", "OPHELIA", "VALERIA", "NONA", "MITZI", "MARI", "GEORGETTE", "CLAUDINE", "FRAN", "ALISSA", "ROSEANN", "LAKEISHA", "SUSANNA", "REVA", "DEIDRE", "CHASITY", "SHEREE", "CARLY", "JAMES", "ELVIA", "ALYCE", "DEIRDRE", "GENA", "BRIANA", "ARACELI", "KATELYN", "ROSANNE", "WENDI", "TESSA", "BERTA", "MARVA", "IMELDA", "MARIETTA", "MARCI", "LEONOR", "ARLINE", "SASHA", "MADELYN", "JANNA", "JULIETTE", "DEENA", "AURELIA", "JOSEFA", "AUGUSTA", "LILIANA", "YOUNG", "CHRISTIAN", "LESSIE", "AMALIA", "SAVANNAH", "ANASTASIA", "VILMA", "NATALIA", "ROSELLA", "LYNNETTE", "CORINA", "ALFREDA", "LEANNA", "CAREY", "AMPARO", "COLEEN", "TAMRA", "AISHA", "WILDA", "KARYN", "CHERRY", "QUEEN", "MAURA", "MAI", "EVANGELINA", "ROSANNA", "HALLIE", "ERNA", "ENID", "MARIANA", "LACY", "JULIET", "JACKLYN", "FREIDA", "MADELEINE", "MARA", "HESTER", "CATHRYN", "LELIA", "CASANDRA", "BRIDGETT", "ANGELITA", "JANNIE", "DIONNE", "ANNMARIE", "KATINA", "BERYL", "PHOEBE", "MILLICENT", "KATHERYN", "DIANN", "CARISSA", "MARYELLEN", "LIZ", "LAURI", "HELGA", "GILDA", "ADRIAN", "RHEA", "MARQUITA", "HOLLIE", "TISHA", "TAMERA", "ANGELIQUE", "FRANCESCA", "BRITNEY", "KAITLIN", "LOLITA", "FLORINE", "ROWENA", "REYNA", "TWILA", "FANNY", "JANELL", "INES", "CONCETTA", "BERTIE", "ALBA", "BRIGITTE", "ALYSON", "VONDA", "PANSY", "ELBA", "NOELLE", "LETITIA", "KITTY", "DEANN", "BRANDIE", "LOUELLA", "LETA", "FELECIA", "SHARLENE", "LESA", "BEVERLEY", "ROBERT", "ISABELLA", "HERMINIA", "TERRA", "CELINA"]
commonLastNames = [ "SMITH", "JOHNSON,", "WILLIAMS", "JONES", "BROWN", "DAVIS", "MILLER", "WILSON", "MOORE", "TAYLOR", "ANDERSON", "THOMAS", "JACKSON", "WHITE", "HARRIS", "MARTIN", "THOMPSON", "GARCIA", "MARTINEZ", "ROBINSON", "CLARK", "RODRIGUEZ", "LEWIS", "LEE", "WALKER", "HALL", "ALLEN", "YOUNG", "HERNANDEZ", "KING", "WRIGHT", "LOPEZ", "HILL", "SCOTT", "GREEN", "ADAMS", "BAKER", "GONZALEZ", "NELSON", "CARTER", "MITCHELL", "PEREZ", "ROBERTS", "TURNER", "PHILLIPS", "CAMPBELL", "PARKER", "EVANS", "EDWARDS", "COLLINS", "STEWART", "SANCHEZ", "MORRIS", "ROGERS", "REED", "COOK", "MORGAN", "BELL", "MURPHY", "BAILEY", "RIVERA", "COOPER", "RICHARDSON", "COX", "HOWARD", "WARD", "TORRES", "PETERSON", "GRAY", "RAMIREZ", "JAMES", "WATSON", "BROOKS", "KELLY", "SANDERS", "PRICE", "BENNETT", "WOOD", "BARNES", "ROSS", "HENDERSON", "COLEMAN", "JENKINS", "PERRY", "POWELL", "LONG", "PATTERSON", "HUGHES", "FLORES", "WASHINGTON", "BUTLER", "SIMMONS", "FOSTER", "GONZALES", "BRYANT", "ALEXANDER", "RUSSELL", "GRIFFIN", "DIAZ", "HAYES", "MYERS", "FORD", "HAMILTON", "GRAHAM", "SULLIVAN", "WALLACE", "WOODS", "COLE", "WEST", "JORDAN", "OWENS", "REYNOLDS", "FISHER", "ELLIS", "HARRISON", "GIBSON", "MCDONALD", "CRUZ", "MARSHALL", "ORTIZ", "GOMEZ", "MURRAY", "FREEMAN", "WELLS", "WEBB", "SIMPSON", "STEVENS", "TUCKER", "PORTER", "HUNTER", "HICKS", "CRAWFORD", "HENRY", "BOYD", "MASON", "MORALES", "KENNEDY", "WARREN", "DIXON", "RAMOS", "REYES", "BURNS", "GORDON", "SHAW", "HOLMES", "RICE", "ROBERTSON", "HUNT", "BLACK", "DANIELS", "PALMER", "MILLS", "NICHOLS", "GRANT", "KNIGHT", "FERGUSON", "ROSE", "STONE", "HAWKINS", "DUNN", "PERKINS", "HUDSON", "SPENCER", "GARDNER", "STEPHENS", "PAYNE", "PIERCE", "BERRY", "MATTHEWS", "ARNOLD", "WAGNER", "WILLIS", "RAY", "WATKINS", "OLSON", "CARROLL", "DUNCAN", "SNYDER", "HART", "CUNNINGHAM", "BRADLEY", "LANE", "ANDREWS", "RUIZ", "HARPER", "FOX", "RILEY", "ARMSTRONG", "CARPENTER", "WEAVER", "GREENE", "LAWRENCE", "ELLIOTT", "CHAVEZ", "SIMS", "AUSTIN", "PETERS", "KELLEY", "FRANKLIN", "LAWSON", "FIELDS", "GUTIERREZ", "RYAN", "SCHMIDT", "CARR", "VASQUEZ", "CASTILLO", "WHEELER", "CHAPMAN", "OLIVER", "MONTGOMERY", "RICHARDS", "WILLIAMSON", "JOHNSTON", "BANKS", "MEYER", "BISHOP", "MCCOY", "HOWELL", "ALVAREZ", "MORRISON", "HANSEN", "FERNANDEZ", "GARZA", "HARVEY", "LITTLE", "BURTON", "STANLEY", "NGUYEN", "GEORGE", "JACOBS", "REID", "KIM", "FULLER", "LYNCH", "DEAN", "GILBERT", "GARRETT", "ROMERO", "WELCH", "LARSON", "FRAZIER", "BURKE", "HANSON", "DAY", "MENDOZA", "MORENO", "BOWMAN", "MEDINA", "FOWLER", "BREWER", "HOFFMAN", "CARLSON", "SILVA", "PEARSON", "HOLLAND", "DOUGLAS", "FLEMING", "JENSEN", "VARGAS", "BYRD", "DAVIDSON", "HOPKINS", "MAY", "TERRY", "HERRERA", "WADE", "SOTO", "WALTERS", "CURTIS", "NEAL", "CALDWELL", "LOWE", "JENNINGS", "BARNETT", "GRAVES", "JIMENEZ", "HORTON", "SHELTON", "BARRETT", "OBRIEN", "CASTRO", "SUTTON", "GREGORY", "MCKINNEY", "LUCAS", "MILES", "CRAIG", "RODRIQUEZ", "CHAMBERS", "HOLT", "LAMBERT", "FLETCHER", "WATTS", "BATES", "HALE", "RHODES", "PENA", "BECK", "NEWMAN", "HAYNES", "MCDANIEL", "MENDEZ", "BUSH", "VAUGHN", "PARKS", "DAWSON", "SANTIAGO", "NORRIS", "HARDY", "LOVE", "STEELE", "CURRY", "POWERS", "SCHULTZ", "BARKER", "GUZMAN", "PAGE", "MUNOZ", "BALL", "KELLER", "CHANDLER", "WEBER", "LEONARD", "WALSH", "LYONS", "RAMSEY", "WOLFE", "SCHNEIDER", "MULLINS", "BENSON", "SHARP", "BOWEN", "DANIEL", "BARBER", "CUMMINGS", "HINES", "BALDWIN", "GRIFFITH", "VALDEZ", "HUBBARD", "SALAZAR", "REEVES", "WARNER", "STEVENSON", "BURGESS", "SANTOS", "TATE", "CROSS", "GARNER", "MANN", "MACK", "MOSS", "THORNTON", "DENNIS", "MCGEE", "FARMER", "DELGADO", "AGUILAR", "VEGA", "GLOVER", "MANNING", "COHEN", "HARMON", "RODGERS", "ROBBINS", "NEWTON", "TODD", "BLAIR", "HIGGINS", "INGRAM", "REESE", "CANNON", "STRICKLAND", "TOWNSEND", "POTTER", "GOODWIN", "WALTON", "ROWE", "HAMPTON", "ORTEGA", "PATTON", "SWANSON", "JOSEPH", "FRANCIS", "GOODMAN", "MALDONADO", "YATES", "BECKER", "ERICKSON", "HODGES", "RIOS", "CONNER", "ADKINS", "WEBSTER", "NORMAN", "MALONE", "HAMMOND", "FLOWERS", "COBB", "MOODY", "QUINN", "BLAKE", "MAXWELL", "POPE", "FLOYD", "OSBORNE", "PAUL", "MCCARTHY", "GUERRERO", "LINDSEY", "ESTRADA", "SANDOVAL", "GIBBS", "TYLER", "GROSS", "FITZGERALD", "STOKES", "DOYLE", "SHERMAN", "SAUNDERS", "WISE", "COLON", "GILL", "ALVARADO", "GREER", "PADILLA", "SIMON", "WATERS", "NUNEZ", "BALLARD", "SCHWARTZ", "MCBRIDE", "HOUSTON", "CHRISTENSEN", "KLEIN", "PRATT", "BRIGGS", "PARSONS", "MCLAUGHLIN", "ZIMMERMAN", "FRENCH", "BUCHANAN", "MORAN", "COPELAND", "ROY", "PITTMAN", "BRADY", "MCCORMICK", "HOLLOWAY", "BROCK", "POOLE", "FRANK", "LOGAN", "OWEN", "BASS", "MARSH", "DRAKE", "WONG", "JEFFERSON", "PARK", "MORTON", "ABBOTT", "SPARKS", "PATRICK", "NORTON", "HUFF", "CLAYTON", "MASSEY", "LLOYD", "FIGUEROA", "CARSON", "BOWERS", "ROBERSON", "BARTON", "TRAN", "LAMB", "HARRINGTON", "CASEY", "BOONE", "CORTEZ", "CLARKE", "MATHIS", "SINGLETON", "WILKINS", "CAIN", "BRYAN", "UNDERWOOD", "HOGAN", "MCKENZIE", "COLLIER", "LUNA", "PHELPS", "MCGUIRE", "ALLISON", "BRIDGES", "WILKERSON", "NASH", "SUMMERS", "ATKINS", "WILCOX", "PITTS", "CONLEY", "MARQUEZ", "BURNETT", "RICHARD", "COCHRAN", "CHASE", "DAVENPORT", "HOOD", "GATES", "CLAY", "AYALA", "SAWYER", "ROMAN", "VAZQUEZ", "DICKERSON", "HODGE", "ACOSTA", "FLYNN", "ESPINOZA", "NICHOLSON", "MONROE", "WOLF", "MORROW", "KIRK", "RANDALL", "ANTHONY", "WHITAKER", "OCONNOR", "SKINNER", "WARE", "MOLINA", "KIRBY", "HUFFMAN", "BRADFORD", "CHARLES", "GILMORE", "DOMINGUEZ", "ONEAL", "BRUCE", "LANG", "COMBS", "KRAMER", "HEATH", "HANCOCK", "GALLAGHER", "GAINES", "SHAFFER", "SHORT", "WIGGINS", "MATHEWS", "MCCLAIN", "FISCHER", "WALL", "SMALL", "MELTON", "HENSLEY", "BOND", "DYER", "CAMERON", "GRIMES", "CONTRERAS", "CHRISTIAN", "WYATT", "BAXTER", "SNOW", "MOSLEY", "SHEPHERD", "LARSEN", "HOOVER", "BEASLEY", "GLENN", "PETERSEN", "WHITEHEAD", "MEYERS", "KEITH", "GARRISON", "VINCENT", "SHIELDS", "HORN", "SAVAGE", "OLSEN", "SCHROEDER", "HARTMAN", "WOODARD", "MUELLER", "KEMP", "DELEON", "BOOTH", "PATEL", "CALHOUN", "WILEY", "EATON", "CLINE", "NAVARRO", "HARRELL", "LESTER", "HUMPHREY", "PARRISH", "DURAN", "HUTCHINSON", "HESS", "DORSEY", "BULLOCK", "ROBLES", "BEARD", "DALTON", "AVILA", "VANCE", "RICH", "BLACKWELL", "YORK", "JOHNS", "BLANKENSHIP", "TREVINO", "SALINAS", "CAMPOS", "PRUITT", "MOSES", "CALLAHAN", "GOLDEN", "MONTOYA", "HARDIN", "GUERRA", "MCDOWELL", "CAREY", "STAFFORD", "GALLEGOS", "HENSON", "WILKINSON", "BOOKER", "MERRITT", "MIRANDA", "ATKINSON", "ORR", "DECKER", "HOBBS", "PRESTON", "TANNER", "KNOX", "PACHECO", "STEPHENSON", "GLASS", "ROJAS", "SERRANO", "MARKS", "HICKMAN", "ENGLISH", "SWEENEY", "STRONG", "PRINCE", "MCCLURE", "CONWAY", "WALTER", "ROTH", "MAYNARD", "FARRELL", "LOWERY", "HURST", "NIXON", "WEISS", "TRUJILLO", "ELLISON", "SLOAN", "JUAREZ", "WINTERS", "MCLEAN", "RANDOLPH", "LEON", "BOYER", "VILLARREAL", "MCCALL", "GENTRY", "CARRILLO", "KENT", "AYERS", "LARA", "SHANNON", "SEXTON", "PACE", "HULL", "LEBLANC", "BROWNING", "VELASQUEZ", "LEACH", "CHANG", "HOUSE", "SELLERS", "HERRING", "NOBLE", "FOLEY", "BARTLETT", "MERCADO", "LANDRY", "DURHAM", "WALLS", "BARR", "MCKEE", "BAUER", "RIVERS", "EVERETT", "BRADSHAW", "PUGH", "VELEZ", "RUSH", "ESTES", "DODSON", "MORSE", "SHEPPARD", "WEEKS", "CAMACHO", "BEAN", "BARRON", "LIVINGSTON", "MIDDLETON", "SPEARS", "BRANCH", "BLEVINS", "CHEN", "KERR", "MCCONNELL", "HATFIELD", "HARDING", "ASHLEY", "SOLIS", "HERMAN", "FROST", "GILES", "BLACKBURN", "WILLIAM", "PENNINGTON", "WOODWARD", "FINLEY", "MCINTOSH", "KOCH", "BEST", "SOLOMON", "MCCULLOUGH", "DUDLEY", "NOLAN", "BLANCHARD", "RIVAS", "BRENNAN", "MEJIA", "KANE", "BENTON", "JOYCE", "BUCKLEY", "HALEY", "VALENTINE", "MADDOX", "RUSSO", "MCKNIGHT", "BUCK", "MOON", "MCMILLAN", "CROSBY", "BERG", "DOTSON", "MAYS", "ROACH", "CHURCH", "CHAN", "RICHMOND", "MEADOWS", "FAULKNER", "ONEILL", "KNAPP", "KLINE", "BARRY", "OCHOA", "JACOBSON", "GAY", "AVERY", "HENDRICKS", "HORNE", "SHEPARD", "HEBERT", "CHERRY", "CARDENAS", "MCINTYRE", "WHITNEY", "WALLER", "HOLMAN", "DONALDSON", "CANTU", "TERRELL", "MORIN", "GILLESPIE", "FUENTES", "TILLMAN", "SANFORD", "BENTLEY", "PECK", "KEY", "SALAS", "ROLLINS", "GAMBLE", "DICKSON", "BATTLE", "SANTANA", "CABRERA", "CERVANTES", "HOWE", "HINTON", "HURLEY", "SPENCE", "ZAMORA", "YANG", "MCNEIL", "SUAREZ", "CASE", "PETTY", "GOULD", "MCFARLAND", "SAMPSON", "CARVER", "BRAY", "ROSARIO", "MACDONALD", "STOUT", "HESTER", "MELENDEZ", "DILLON", "FARLEY", "HOPPER", "GALLOWAY", "POTTS", "BERNARD", "JOYNER", "STEIN", "AGUIRRE", "OSBORN", "MERCER", "BENDER", "FRANCO", "ROWLAND", "SYKES", "BENJAMIN", "TRAVIS", "PICKETT", "CRANE", "SEARS", "MAYO", "DUNLAP", "HAYDEN", "WILDER", "MCKAY", "COFFEY", "MCCARTY", "EWING", "COOLEY", "VAUGHAN", "BONNER", "COTTON", "HOLDER", "STARK", "FERRELL", "CANTRELL", "FULTON", "LYNN", "LOTT", "CALDERON", "ROSA", "POLLARD", "HOOPER", "BURCH", "MULLEN", "FRY", "RIDDLE", "LEVY", "DAVID", "DUKE", "ODONNELL", "GUY", "MICHAEL", "BRITT", "FREDERICK", "DAUGHERTY", "BERGER", "DILLARD", "ALSTON", "JARVIS", "FRYE", "RIGGS", "CHANEY", "ODOM", "DUFFY", "FITZPATRICK", "VALENZUELA", "MERRILL", "MAYER", "ALFORD", "MCPHERSON", "ACEVEDO", "DONOVAN", "BARRERA", "ALBERT", "COTE", "REILLY", "COMPTON", "RAYMOND", "MOONEY", "MCGOWAN", "CRAFT", "CLEVELAND", "CLEMONS", "WYNN", "NIELSEN", "BAIRD", "STANTON", "SNIDER", "ROSALES", "BRIGHT", "WITT", "STUART", "HAYS", "HOLDEN", "RUTLEDGE", "KINNEY", "CLEMENTS", "CASTANEDA", "SLATER", "HAHN", "EMERSON", "CONRAD", "BURKS", "DELANEY", "PATE", "LANCASTER", "SWEET", "JUSTICE", "TYSON", "SHARPE", "WHITFIELD", "TALLEY", "MACIAS", "IRWIN", "BURRIS", "RATLIFF", "MCCRAY", "MADDEN", "KAUFMAN", "BEACH", "GOFF", "CASH", "BOLTON", "MCFADDEN", "LEVINE", "GOOD", "BYERS", "KIRKLAND", "KIDD", "WORKMAN", "CARNEY", "DALE", "MCLEOD", "HOLCOMB", "ENGLAND", "FINCH", "HEAD", "BURT", "HENDRIX", "SOSA", "HANEY", "FRANKS", "SARGENT", "NIEVES", "DOWNS", "RASMUSSEN", "BIRD", "HEWITT", "LINDSAY", "LE", "FOREMAN", "VALENCIA", "ONEIL", "DELACRUZ", "VINSON", "DEJESUS", "HYDE", "FORBES", "GILLIAM", "GUTHRIE", "WOOTEN", "HUBER", "BARLOW", "BOYLE", "MCMAHON", "BUCKNER", "ROCHA", "PUCKETT", "LANGLEY", "KNOWLES", "COOKE", "VELAZQUEZ", "WHITLEY", "NOEL", "VANG"]

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

def isCommonName(word):
	array = word.split(" ")
	for i in range(len(array)):
		word = array[i].upper()
		word = removeSpecialCharacter(word)
		word = removeApostrophS(word)
		# print(word)
		if word in commonFirstNames or word in commonLastNames:
			return True
	return False

def containsCommonWord(word):
	array = word.split(" ")
	for i in range(len(array)):
		word = array[i].lower()
		word = removeSpecialCharacter(word)
		word = removeApostrophS(word)
		if word in commonWords or word in pronouns or word in familyRelations or word in statementWords or word in nonPersonEntityTypes or word in occupationWords:
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
	listOfPrefixes = ["President", "DJ", "Captain", "Adm", "Atty", "Brother", "Capt", "Chief", "Cmdr", "Col", "Dean", "Dr", "Elder", "Father", "Gen", "Gov", "Hon", "Lt Col", "Maj", "MSgt", "Mr", "Mrs", "Ms", "Prof", "Rabbi", "Rev", "Sister", "Sir", "Queen", "Reverend"]
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

def allCharactersCapitalized(token):
	return all([c.isupper() for c in token]) and len(token) > 1

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

	previousWord = previousWord.strip()
	nextWord = nextWord.strip()

	if (word.endswith(",") or word.endswith(".")) and not (allWordsCapitalized(previousWord)):
		return False

	if (previousWord.endswith(",") or previousWord.endswith("!")) or (not allWordsCapitalized(nextWord)) or word.endswith(",") or word.endswith("."):
		return False
	
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
	
	lineStartIndex = offset

	while(lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.']):
		lineStartIndex = lineStartIndex - 1
	
	line = content[lineStartIndex:offset + 1]

	words = line.split()
	index = 1
	for word in words:
		if not(index == 1 and word[0].isupper()):
			word = word.strip().lower()
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
		if (not word[0].isupper()):
			word = word.strip().lower()
			for relation in familyRelations:
				if relation in word:
					return True

	return False

def isPreceededByThe(offset, content):
	lineStartIndex = offset
	while(lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.']):
		lineStartIndex = lineStartIndex - 1

	line = content[lineStartIndex:offset + 1]
	words = list(reversed(line.split()))
	
	for word in words:
		word = word.strip()
		if (not word[0].isupper()):
			if (word.lower() == "the"):
				return True
			else:
				return False
		
		if (word.lower() == "the"):
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

def isPrecededByOtherEntities(offset, content):
	lineStartIndex = offset
	
	while (lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.']):
		lineStartIndex = lineStartIndex - 1
	
	line = content[lineStartIndex:offset + 1]
	
	words = list(reversed(line.split()))

	for word in words:
		word = word.strip()
		if not allWordsCapitalized(word):
			return False
		if word.endswith(",") or word in ["and", "&"]:
			return True

	return False


def isSucceededByOtherEntities(offset, content):
	lineEndIndex = offset + 1

	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.']):
		lineEndIndex = lineEndIndex + 1

	line = content[offset:lineEndIndex + 1]

	words = line.split()
	checkNextWord = False
	for word in words:
		word = word.strip()
		if checkNextWord and allWordsCapitalized(word):
			return True
		if word in ["and", "&"]:
			return True
		if word.endswith(","):
			checkNextWord = True
		if not allWordsCapitalized(word):
			return False
	return False

def isPreceededByNonPersonEntity(offset, content):

	lineStartIndex = offset
	numSpaces = 0
	threshold = 5
	while (lineStartIndex > 0 and content[lineStartIndex] not in ['\n', '.'] and numSpaces < threshold):
		lineStartIndex = lineStartIndex - 1
		if content[lineStartIndex] == " ":
			numSpaces = numSpaces + 1

	line = content[lineStartIndex:offset + 1]

	words = line.split()
	index = 0
	for word in words:
		index = index + 1
		word = word.strip().lower()
		for entity in nonPersonEntityTypes:
			if entity in word:
				return (True, threshold - index)

	return (False, -1 * threshold)

def isFollowedByNonPersonEntity(offset, content):
	threshold = 5
	lineEndIndex = offset + 1
	numSpaces = 0
	
	while(lineEndIndex < len(content) - 1 and content[lineEndIndex] not in ['\n', '.'] and numSpaces < threshold):
		lineEndIndex = lineEndIndex + 1
		if content[lineEndIndex] == " ":
			numSpaces = numSpaces + 1
	
	line = content[offset:lineEndIndex + 1]

	words = line.split()
	index = 0
	for word in words:
		index = index + 1
		word = word.strip().lower()
		for entity in nonPersonEntityTypes:
			if entity in word:
				return (True, index)

	return (False, -1 * threshold)

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
	# text = getDocumentContent(133);
	# index = text.index("Mariah Carey")
	print(isCommonName("Golden Globe Awards,"))
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
