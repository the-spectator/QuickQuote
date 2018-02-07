try:
	from QuickUMLS.quickumls import *
except:
	from quickumls import *
import os

text = '''
Had bypass in 2010. 
takes following medications:
1. Metoprolol (Blood pressure) - diagnosed 2014 - Takes 25 mg daily 
2. Levothyroxine (Thyroid) - diagnosed 2016 - Takes 25 mg daily 
'''

def give_med_terms(text):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	src = dir_path+'/quickumlsfiles/'
	matcher = QuickUMLS(src)
	result = matcher.match(text, best_match=True, ignore_syntax=False)
	set_terms = set()
	for i in result:
		for j in i:
			if j['similarity'] > 0.8:
				set_terms.add(j['ngram'])
	#for i in term:
	#	print(i)
	return set_terms

#print(give_med_terms(text))
