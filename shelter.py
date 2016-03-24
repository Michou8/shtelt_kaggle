import pandas as pd
train = pd.read_csv('train.csv')
print train[:10]
id_train = train['AnimalID']
target = train['OutcomeType']
suboutcome = train['OutcomeSubtype']
train = train.drop(['AnimalID','OutcomeType','OutcomeSubtype'],axis=1)
columns = train.columns
for col in columns:
	print 'Column name:\t',col
	unique = set(train[col])
	#print 'Unique value:\t',unique
	print 'Size of unique value:\t',len(unique)
	#raw_input()
#### Date trasnformation###
# e.g : 2014-11-10 19:04:00
def year(date):
	return int(date.split('-')[0])
def month(date):
	return int(date.split('-')[1])
def day(date):
	return int(date.split(' ')[0].split('-')[2])
def time(date):
	spl = date.split(' ')[1].split(':')
	return sum([int(spl[i])*(60**(2-i)) for i in xrange(len(spl))])
### Animaltype transformation ###
def animal(animaltype):
	animaltype = animaltype.lower()
	if animaltype == 'cat':
		return 1
	if animaltype == 'dog':
		return 0
def counter(data):
	res = {}
	for k in data:
		if k not in res:
			res[k] = 1
		else:
			res[k] += 1
	return res
#print counter(train['SexuponOutcome'])
#### SexuponOutcome transformation ###
sex_upon = {'nan': 1, 'Spayed Female': 8820, 'Neutered Male': 9779, 'Intact Female': 3511, 'Unknown': 1093, 'Intact Male': 3525}
def sex(sexupon):
	if 'Female' in sexupon:
		return 1
	elif 'Male' in sexupon:
		return 0
	else:
		return -1
#train['sex'] = train['SexuponOutcome'].apply(sex)
def intact(sexupon):
	if 'Spayed' in sexupon or 'Neutered' in sexupon:
		return 0
	elif 'Intact' in sexupon:
		return 1
	else:
		return -1
#train['intact'] = train['SexuponOutcome'].apply(intact)
#train = train.drop(['SexuponOutcome'],axis=1)	

#print counter(train['AgeuponOutcome'])
##### AgeuponOutcome transformation ######
age = {'5 years': 992, '7 months': 288, '13 years': 143, 'nan': 18, '14 years': 97, '19 years': 3, '1 weeks': 171, '9 months': 224, '1 week': 146, '11 years': 126, '6 months': 588, '1 month': 1281, '6 years': 670, '2 months': 3397, '5 days': 24, '12 years': 234, '10 years': 446, '5 weeks': 11, '4 weeks': 334, '3 weeks': 659, '20 years': 2, '6 days': 50, '9 years': 288, '16 years': 36, '0 years': 22, '7 years': 531, '8 years': 536, '4 months': 888, '3 months': 1277, '2 weeks': 529, '17 years': 17, '18 years': 10, '10 months': 457, '3 years': 1823, '4 years': 1071, '3 days': 109, '4 days': 50, '11 months': 166, '15 years': 85, '1 year': 3969, '5 months': 652, '2 years': 3742, '8 months': 402, '1 day': 66, '2 days': 99}
kys_tr = {'month':4,'year':52,'day':1/7.0}
def weeks(AgeuponOutcome):
	AgeuponOutcome = str(AgeuponOutcome).split(' ')
	if len(AgeuponOutcome)>1:
		age = int(AgeuponOutcome[0])
		for key in kys_tr:
			if key in AgeuponOutcome[1]:
				return age*kys_tr[key]
	return -1
#train['ageweeks']  = train['AgeuponOutcome'].apply(weeks)
##### Breed tranformation ####
def uniquebreed(breeds):
	res = {}
	for color in breeds:
		spl = color.split('/')
		if len(spl)>1:
			for c in spl:
				if c not in res:
					res[c] = 1
				else:
					res[c] += 1
		else:
			if color not in res:
				res[color] = 1

			else:	
				res[color] += 1	
	return res
print uniquebreed(train['Breed'])
def coderbreed(data):
	c  = 1
	res = {}
	for k in data:
		res[k] = c
		c += 1
	return res
coders_ = coderbreed(uniquebreed(train['Breed']))
def breed(Breed):
	spl = Breed.split('/')
	r = 0
	if len(spl)>1:
		for s in spl:
			r*= coders_[s]
	else:
		return coders_[Breed]
#print set(train['Breed'].apply(breed))
#def breed(Breed):
	
	
