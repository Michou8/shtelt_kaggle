import pandas as pd
import json
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
print train[:10]
id_train = train['AnimalID']
id_test = test['ID']
target = train['OutcomeType']
suboutcome = train['OutcomeSubtype']
train = train.drop(['AnimalID','OutcomeType','OutcomeSubtype'],axis=1)
test = test.drop(['ID'],axis=1)
columns = train.columns
for col in columns:
	print 'Column name:\t',col
	unique = set(train[col])
	#print 'Unique value:\t',unique
	print 'Size of unique value:\t',len(unique)
	#raw_input()

### Name transformtion ######
def name(Name):
	return len(str(Name))
train['size_name'] = train['Name'].apply(name)
train =train.drop(['Name'],axis=1)
test['size_name'] = test['Name'].apply(name)
test =test.drop(['Name'],axis=1)
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
train['year'] = train['DateTime'].apply(year)
train['month'] = train['DateTime'].apply(month)
train['day'] = train['DateTime'].apply(day)
train['time'] = train['DateTime'].apply(time)
train = train.drop(['DateTime'],axis=1)

test['year'] = test['DateTime'].apply(year)
test['month'] = test['DateTime'].apply(month)
test['day'] = test['DateTime'].apply(day)
test['time'] = test['DateTime'].apply(time)
test = test.drop(['DateTime'],axis=1)
### Animaltype transformation ###
def animal(animaltype):
	animaltype = animaltype.lower()
	if animaltype == 'cat':
		return 1
	if animaltype == 'dog':
		return 0

train['type_'] = train['AnimalType'].apply(animal)
train = train.drop(['AnimalType'],axis=1)
test['type_'] = test['AnimalType'].apply(animal)
test = test.drop(['AnimalType'],axis=1)
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
	sexupon = str(sexupon)
	if 'Female' in sexupon:
		return 1
	elif 'Male' in sexupon:
		return 0
	else:
		return -1
train['sex'] = train['SexuponOutcome'].apply(sex)
test['sex'] = test['SexuponOutcome'].apply(sex)
def intact(sexupon):
	sexupon = str(sexupon)
	if 'Spayed' in sexupon or 'Neutered' in sexupon:
		return 0
	elif 'Intact' in sexupon:
		return 1
	else:
		return -1
train['intact'] = train['SexuponOutcome'].apply(intact)
train = train.drop(['SexuponOutcome'],axis=1)	

test['intact'] = test['SexuponOutcome'].apply(intact)
test = test.drop(['SexuponOutcome'],axis=1)
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

train['ageweeks']  = train['AgeuponOutcome'].apply(weeks)
train = train.drop(['AgeuponOutcome'],axis=1)

test['ageweeks']  = test['AgeuponOutcome'].apply(weeks)
test = test.drop(['AgeuponOutcome'],axis=1)

##### Breed tranformation ####
def uniquebreed(breeds):
	res = {}
	for color in breeds:
		color = color.replace(' ','/')
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
key_code =  coders_.keys()
def breed(Breed):
	spl = Breed.split('/')
	r = 0
	for i in xrange(len(key_code)):
		if key_code[i] in Breed:
			r+= (1.1)**i
	return r
#print set(train['Breed'].apply(breed))
train['breed'] = train['Breed'].apply(breed)
test['breed'] = test['Breed'].apply(breed)
train = train.drop(['Breed'],axis=1)
test  = test.drop(['Breed'],axis=1)
####### COLOR unique #########
def uniquecolor(colors):
	res = {}
	for c in colors:
		r = c.split('/')
		if len(r) >1:
			for s in r:
				for s_i in s.split(' '):
					if s_i not in res:
						res[s_i] = 1
					else:
						res[s_i] += 1
		else:
			r  = c.split(' ')
			for c in r:
				if c not in res:
					res[c] = 1
				else:
					res[c] += 1
	return res
key_color = uniquecolor(train['Color']).keys()
def color_(color):
	res = 1
	for i in xrange(len(key_color)):
		key = key_color[i]
		if key in color:
			res += (0.5)**i
	return res
train['ColorModif'] = train['Color'].apply(color_)
train = train.drop(['Color'],axis=1)

test['ColorModif'] = test['Color'].apply(color_)
test = test.drop(['Color'],axis=1)
print train[:10]		
	
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=200)
rf_ = rf.fit(train,target)
pred = rf.predict(train)
from sklearn.metrics import precision_score
from sklearn.metrics import classification_report
print classification_report(target,pred)
pred_ = rf.predict_proba(test)
cl =  rf_.classes_
sample = {'ID':id_test}
for i in xrange(len(cl)):
	sample[cl[i]] = pred_[:,i]
pd.DataFrame(sample).to_csv('sub.csv',index=False)
