# -*- coding: utf-8 -*-


import pandas as pd
import re
import config
from datetime import datetime
try:
	from search_term import give_med_terms
except:
	from QuickUMLS.search_term import give_med_terms

number = r'\d{2,3}'

gender = r'(\b[Mm]ale?)|(\b[Ff]emale?)|(\bFEMALE)|(\bMALE)|(/b)|F/|M/'

Date = r'(([A-Z0-9][A-Z0-9]?[/-])?[A-Z0-9][A-Z0-9]?[/-][A-Z0-9][A-Z0-9][A-Z0-9]?[A-Z0-9]?)|([A-Za-z][A-Za-z][A-Za-z]\s..?[,]\s....)'

DOB  = r'(.*)?DOB|[Dd][aA][tT][eE]\s[oO][fF]\s[Bb][iI][rR][tT][hH]\s?(.*)?'

year_four_digit = r'\b(19|20)\d{2}(w+)?'
year_two_digit = r'\d{2}$(w+)?'

product_type = r'(\b[Pp]roduct\s[Tt]ype):\s?.*'
permanent = r'[Pp][eE][rR][mM]([aA][nN][aA][nN][tT])?'
term = r'[tT][eE][rR][mM]'

#Assuming USA currency dollar
amount_with_dollar = r'(\$\s?\d{1,3}(,\d{2,3})*(\.\d+)?)(\s?[kK]?)(\s?[mM]?[mM]?(illion)?(ILLION)?)([bB]?)'
amount_without_dollar = r'(\$?\s?\d{1,3}(,\d{2,3})*(\.\d+)?)(\s?[kK]?)(\s[mM]?[mM]?(illion)?(ILLION)?)([bB]?)((\s?[Yy][Ee][aA][rR][sS]?)?)'
faceamount = r'(\b[Ff]ace\s?[Aa]mount:?\s?.*)'
termamount = r'(.*)?[Tt][eE][rR][mM](.*)?'   			#Regex to read single line from first newline to next newline
seeking = r'(.*)?[Ss][eE][eE][kK]([iI][nN][gG])?(.*)?'
term_year = r'(y(ea)?r|Y(ea)?r|Y(ea)?r)'
k_conv = r'(\s?[kK])'
m_conv = r'(\s?[mM][mM]?(illion)?(ILLION)?)'
num_conv = r'\d{1,3}'

weight = r'(.*)?\b[wW][eE][iI][gG][hH][tT]\s?(.*)?' 
weight_num = r'(\d*\.?\d+)\s?(lb|lbs|Lbs|LB|LBS|kg|Kg|KG|#)'		#r'(.*)\s?([lL][bB][sS]|[oO][zZ]|[gG]|[kK][Gg])' 

age_simple = r'(.*)?[Aa][Gg][Ee]\s?(.*)?'
age = r'(.*\s?[Yy]([eE][aA])?[rR]?[sS]?\s?([oO][lL][dD])?)'
age_from_gender = r'(.*)?(\b[Mm]ale?)|(\b[Ff]emale?)|(\bFEMALE)|(\bMALE)|(/b)\s?(.*)?' 

height_num = r'\d{1,2}'
height1 = r'((.*)?\s?([Ff][eE][eE][tT])((.*)?\s?([iI][nN][Cc][Hh][Ee][Ss]))?)'			#Two types of inches => "|”
height2 = r'.[\'|\’](\s?.[\"|\”])?' 											
feet = r'\d[\'|\’]'
inches = r'\d[\"|\”]' 

preferred = r'(.*)?(Preferred|preferred)\s?(.*)?'
height_word = r'Height|height'
weight_word = r'Weight|weight' 

build = r'(Build|build)\s?(.*)?'
build_weight = r'\d{3}'
build_height = r'\d\.\d'

smoker = r'(.*)?[sS][Mm][oO][Kk]\s?(.*)?' 
tobacco = r'(.*)?[Tt][oO][bB][aA][cC][cC][oO]\s?(.*)?'
no = r'[nN][oO]'

med = r'(.*)?\b[mM][eE][dD][iI][cC][aA][tT][iI][oO][nN]\s?(.*)?'

family = r'(.*)?(\b[Ff]amily)\s?(.*)?'
family_member = r'(.*)?(\b[Mm]om)|(\b[Ff]ather)|(\b[Dd]ad)|(\b[Ss]ister)|(\b[Bb]rother)|(\b[Hh]usband)|(\b[Ww]ife)\s?(.*)?'

lives = r'(.*)?(\b[Ll]ives)\s?(.*)?'
prop = r'(.*)?(\b[Pp]roperty)\s?(.*)?'

def genderRegex(line):
	ans=" "
	gender = r'(\b[Mm]ale?)|(\b[Ff]emale?)|(\bFEMALE)|(\bMALE)|(/b)|F/|M/'
	#for line in st:
	y = re.search(gender, line, re.I | re.U)
	if(y):
		if(y.group(0)=='F/'):
			ans='Female'
		elif(y.group(0)=='M/'):
			ans='Male'
		else:
			#print (y.group(0)+"\n")
			ans=(y.group(0))
	elif(y and num):
		ans=(y.group(0))
	else:
		ans=" "

	return ans.strip().lower()

def yearRegex(line):
	ans=" "
	num = re.search(number, line, re.I | re.U)
	x = re.search(Date, line, re.I | re.U)
	ans = 0
	z = 0
	x1 = re.search(year_four_digit, line, re.I | re.U)
	if(x):
		x1 = re.search(year_four_digit, x.group(0), re.I | re.U)
		x2 = re.search(year_two_digit, x.group(0), re.I | re.U)				
		if(x1):
			ans=x1.group(0)
		elif(x2):
			z = x2.group(0)									
			#print('Last 2 digits of Year of birth='+z)
			ans= '19'+str(z)
	elif(x1):
		x1 = re.search(year_four_digit, line, re.I | re.U)
		#print (x1.group(0))
		ans=x1.group(0)
	else:
		ans=" "
	return ans.strip().strip()

def productRegex(line):
	ans=" "
	z=re.search(product_type, line, re.I | re.U)
	perm_reg = re.search(permanent, line, re.I | re.U)
	term_type_reg = re.search(term, line, re.I | re.U)
	if(z): 
		#print (z.group(0)+"\n")
		ans=(z.group(0))
	elif(perm_reg):
		final_str = "Product Type: Permanent"
		ans=(final_str)
	elif(term_type_reg):
		final_str= "Product Type: Term"
		ans=(final_str)
	else:
		ans=" "
	return ans.strip()

def weightRegex(line):
	ans=" "
	#Preferred Height & Weight
	pr = ''
	pr = re.search(preferred, line, re.I | re.U)
	if(pr!='' and pr):
		w_reg = re.search(weight_word, pr.group(0), re.I | re.U)
		if(w_reg):
			ans = "196 lbs"
			return ans.strip()
	else:
		x=re.search(weight_num, line, re.I | re.U) 
		wt=re.search(weight, line, re.I | re.U)
		if(x): 
			#print (x.group(0)+"\n")
			ans=(x.group(0))
		elif(wt):
			am = re.search(weight_num,wt.group(0), re.I | re.U)
			if(am):
				ans=(am.group(0))
		else:
			ans=" "
		
	return ans.strip()

def heightRegex(line):
	ans=" "
	#Preferred Height & Weight
	pr = ''
	pr = re.search(preferred, line, re.I | re.U)
	if(pr!='' and pr):
		h_reg = re.search(height_word, pr.group(0), re.I | re.U)
		if(h_reg):
			ans = "5 Feet 9 Inches"
			return ans.strip()
	else:
		ht = re.search(height1, line, re.I | re.U)
		htsym = re.search(height2, line, re.I | re.U)
		if(ht): 
			#print (ht.group(0)+"\n")
			ans=(ht.group(0))
		elif(htsym):
			f = re.search(feet, (htsym.group(0)), re.I | re.U)
			inch = re.search(inches, (htsym.group(0)), re.I | re.U)
			if(f):
				#print(f.group(0))
				am = re.search(height_num, (f.group(0)), re.I | re.U).group(0) + ' Feet'
				if(inch):
					am+=re.search(height_num, (inch.group(0)), re.I | re.U).group(0) + ' Inches' 
				ans=am
		else:
			ans=" "
	return ans.strip()

def ageRegex(line):
	
		
	#--------------------------------------------------------------------


	age_reg = re.search(age, line, re.I | re.U)
	age_simple_reg = re.search(age_simple, line, re.I | re.U)
	dob = re.search(DOB, line, re.I | re.U)
	age_gender_reg = re.search(age_from_gender, line, re.I | re.U)
	x1 = re.search(year_four_digit, line, re.I | re.U)
	
	if(age_gender_reg):										#Male 20
			am = re.search(number, age_gender_reg.group(0), re.I | re.U)
			if(am):
				ans=am.group(0)
		
	if(x1):													#20/03/1996
		#print ("DOB:"+x1.group(0))
		currentYear = datetime.now().year
		#print (currentYear-(int)(x1.group(0)))
		ans=((currentYear-(int)(x1.group(0))))
	
	else:
		if(x1 and dob):										#DOB 20/03/1996
			#print ("DOB:"+x1.group(0))
			currentYear = datetime.now().year
			#print (currentYear-(int)(x1.group(0)))
			ans=((currentYear-(int)(x1.group(0))))
		elif(x1 and y):										#Male 20/03/1996
			#print ("DOB:"+x1.group(0))
			currentYear = datetime.now().year
			#print (currentYear-(int)(x1.group(0)))
			ans=((currentYear-(int)(x1.group(0))))
		else:
			ans=' '
			
		if(age_reg):										#20 years ago
			age_num = age_reg.group(0)			
			an = re.search(number, age_num, re.I | re.U)
			if(an):				
				
				#print ("DOB:"+ an.group(0))
				ans=(an.group(0))
	
		if(age_simple_reg):								#Age 20
			age_num = age_simple_reg.group(0)			
			an = re.search(number, age_num, re.I | re.U)
			if(an):				
				#print ("DOB:"+ an.group(0))
				ans=(an.group(0))
		
		#ans_year = yearRegex(line)
		#print("AAMN")	
		#print(type(ans_year), ans_year)	
		
		#if(ans_year and ans_year!=0):
		#	currentYear = datetime.now().year
			#ans=(currentYear-(int)(ans_year))
	
	# print(ans)	
	return ans.strip()

def habitRegex(line):
	ans=" "
	sm = re.search(smoker, line, re.I | re.U)
	tob = re.search(tobacco, line, re.I | re.U)
	if(sm): 
		if(re.search(no, sm.group(0), re.I | re.U)):
			ans="Non-Tobacco"
		else:
			ans="TObacco"
	elif(tob):
		#print(tob.group(0))
		if(re.search(no, tob.group(0), re.I | re.U)):
			ans="Non-Tobacco"
		else:
			ans="Tobacco"
	else:
		ans=" "
	return ans.strip()
	
def faceamountRegex(line):
	ans=" "
	w = re.search(faceamount, line	, re.I | re.U)
	term_reg = re.search(termamount, line, re.I | re.U)
	seek_reg = re.search(seeking, line, re.I | re.U)
	#With faceAmount
	if(w):
		k = re.search(k_conv, w.group(0), re.I | re.U)
		if(k):
			nn = re.search(num_conv, w.group(0), re.I | re.U)
			ans='Face Amount: $'+((nn.group(0))+',000')
		else:
			ans=(w.group(0))

		#With term Amount
	elif(term_reg):
		amd = re.search(amount_with_dollar, term_reg.group(0), re.I | re.U)
		amwd = re.search(amount_without_dollar, term_reg.group(0), re.I | re.U)			#Find 2nd regex in the same line of 1st regex 
		z = 0
		if(amd):
			k = re.search(k_conv, amd.group(0), re.I | re.U)
			m = re.search(m_conv, amd.group(0), re.I | re.U)
			if(k):
				nn = re.search(num_conv, amd.group(0), re.I | re.U)
				ans='Face Amount: '+((nn.group(0))+',000')
			elif(m):
				nn = re.search(num_conv, amd.group(0), re.I | re.U)
				ans='Face Amount: '+((nn.group(0))+',000,000')
			else:
				ans='Face Amount: '+amd.group(0)
		elif(amwd):
			term_year_reg = re.search(term_year, amwd.group(0), re.I | re.U)
			if(term_year_reg):
				ans='Term Year: '+(amwd.group(0))
			else:
				#ans='Face Amount: $'+(amwd.group(0))
				k = re.search(k_conv, amwd.group(0), re.I | re.U)
				m = re.search(m_conv, amwd.group(0), re.I | re.U)
				if(k):
					nn = re.search(num_conv, amwd.group(0), re.I | re.U)
					ans='Face Amount: $'+((nn.group(0))+',000')
				elif(m):
					nn = re.search(num_conv, amwd.group(0), re.I | re.U)
					ans='Face Amount: $'+((nn.group(0))+',000,000')
				else:
					ans='Face Amount: $'+amwd.group(0)
	#With Seeking
	elif(seek_reg):
		amd = re.search(amount_with_dollar, seek_reg.group(0), re.I | re.U)
		amwd = re.search(amount_without_dollar, seek_reg.group(0), re.I | re.U)			#Find 2nd regex in the same line of 1st regex 
		if(amd):
			#ans='Face Amount: '+(amd.group(0))
			k = re.search(k_conv, amd.group(0), re.I | re.U)
			m = re.search(m_conv, amd.group(0), re.I | re.U)
			if(k):
				nn = re.search(num_conv, amd.group(0), re.I | re.U)
				ans='Face Amount: '+((nn.group(0))+',000')
			elif(m):
				nn = re.search(num_conv, amd.group(0), re.I | re.U)
				ans='Face Amount: '+((nn.group(0))+',000,000')
			else:
				ans='Face Amount: '+amd.group(0)
		elif(amwd):
			term_year_reg = re.search(term_year, amwd.group(0), re.I | re.U)
			if(term_year_reg):
				ans='Term Year: '+(amwd.group(0))
			else:
				#ans='Face Amount: $'+(amwd.group(0))
				k = re.search(k_conv, amwd.group(0), re.I | re.U)
				m = re.search(m_conv, amwd.group(0), re.I | re.U)
				if(k):
					nn = re.search(num_conv, amwd.group(0), re.I | re.U)
					ans='Face Amount: $'+((nn.group(0))+',000')
				elif(m):
					nn = re.search(num_conv, amwd.group(0), re.I | re.U)
					ans='Face Amount: $'+((nn.group(0))+',000,000')
				else:
					ans='Face Amount: $'+amwd.group(0)
	else:
		ans=" "
	return ans.strip()
	
def medicationRegex(line):
	#Medication & Treatment
	ans=" "
	med_reg = (re.search(med,line, re.I | re.U))
	ans = ""
	if(med_reg):
		if(re.search(no, med_reg.group(0), re.I | re.U)):
			ans="No Medication"
	else:
		ans = " "
	return ans.strip()

def propertyRegex(line):
	#Property
	ans =""
	lives_reg = (re.search(lives,line, re.I | re.U))
	prop_reg = (re.search(prop,line, re.I | re.U))
	if(lives_reg):
		ans=lives_reg.groups()
		if(prop_reg):
			ans=lives_reg.groups()+prop_reg.groups()
	elif(prop_reg):
		ans=prop_reg.groups()
	return ans.strip()

def propertyRegex(line):
	#Family
	ans=" "
	family_reg = (re.search(family,line, re.I | re.U))
	family_member_reg = (re.search(family_member,line, re.I | re.U))
	if(family_reg):
		ans=family_reg.groups()
	else:															#Write else outsite condition (to stop rewriting of above cell)
		ans=""
	return ans.strip()


def medicalTerms(doc):
	return give_med_terms(doc)

def regexmain(file):
	df = pd.read_csv(file, encoding='UTF-8')
	df = df.drop(columns=['ID','MessageID','Subject','recepientemail','SentOn','ReceivedOn','Offer_noise_free'])
	df['Gender'] = df['Contents'].apply(genderRegex)
	df['Year_of_Birth'] = df['Contents'].apply(yearRegex)
	df['Age(years)'] = df['Contents'].apply(ageRegex)
	df['Product Type'] = df['Contents'].apply(productRegex)
	df['Weight'] = df['Contents'].apply(weightRegex)
	df['Height'] = df['Contents'].apply(heightRegex)
	df['Habit'] = df['Contents'].apply(habitRegex)
	df['Face Amount'] = df['Contents'].apply(faceamountRegex)
	df['Medication'] = df['Contents'].apply(medicationRegex)
	df['Property'] = df['Contents'].apply(propertyRegex)
	df['Property'] = df['Contents'].apply(propertyRegex)
	df['Medical Data'] = df['Contents'].apply(medicalTerms)
	df['Family'] = df['Contents'].apply(propertyRegex)
	# df['Medical Data'] = df['Contents'].apply(medicalTerms)
	df = df.drop(columns=['Contents'])
	df.to_csv(config.regex_processed_csv,index =False, encoding='utf-8')
	
# regexmain(config.raw_data_csv)	





