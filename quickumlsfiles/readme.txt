Steps.

1. Put umls-simstring.db and cui-semtypes.db in this folder
2. Put quickumlsfiles folder inside QuickUmls folder.
3. Put QuickUmls folder inside QuickQuotes folder.
   tree should be in this orider.
QuickQuotes
├── QuickUMLS
│   ├── quickumlsfiles
│   │   ├── cui-semtypes.db
│   │   └── umls-simstring.db   

Update: 8 Feb 2018

1. Download en_core_web_sm-2.0.0.tar.gz
2. run command: pip install {path}/en_core_web_sm-2.0.0.tar.gz
3. Try this on python interpreter
	import spacy
	import en_core_web_sm
	nlp = en_core_web_sm.load()
	doc = nlp(u'If this works we are good to go.')
	print(doc)

If this workout we are good to go.
