import pandas as pd
import re


def genderRegex(doc):
	return ans


def yearRegex(doc):
	return ans


def productRegex(doc):
	return ans


def weightRegex(doc):
	return ans


def ageRegex(doc):
	return ans


def habitRegex(doc):
	return ans


def medicationRegex(doc):
	return ans


def propertyRegex(doc):
	return ans


def medicalTerms(doc):
	return search_med_terms(doc)


def regexmain(file):
	df = pd.read_csv(file, encoding='UTF-8')
	df['Gender'] = df['Contents'].apply(genderRegex)
	df['Year_of_Birth'] = df['Contents'].apply(yearRegex)
	df['Age(years)'] = df['Contents'].apply(ageRegex)
	df['Product Type'] = df['Contents'].apply(productRegex)
	df['Face Amount'] = df['Contents'].apply(weightRegex)
	df['Height'] = df['Contents'].apply(heightRegex)
	df['Habit'] = df['Contents'].apply(habitRegex)
	df['Medication'] = df['Contents'].apply(medicationRegex)
	df['Property'] = df['Contents'].apply(propertyRegex)
	df['Medical Data'] = df['Contents'].apply(medicalTerms)
