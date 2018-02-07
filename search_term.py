try:
	from QuickUMLS.quickumls import *
except:
	from quickumls import *
import os

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
