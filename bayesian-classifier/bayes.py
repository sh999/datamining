'''
Bayesian classifier for car-buying dataset
Data source:
            http://archive.ics.uci.edu/ml/datasets/Car+Evaluation
The data contain classification of cars into unacceptable to very good
Car attributes include buying price, maintenance price, # doors,
 capacity, luggage size, and safety estimate
I am using 1000 of the car entries as training set; the remaining 728
 are the training set
'''
import copy
import sys
def make_table(training_set):
	'''
	Bayesian classifier table with absolute counts
	First make table w/ 0 values
	Next call update_table to tally data entries
	'''
	table = {"unacc":{
					"count":0,
					"buying":{"vhigh":0,"high":0,"med":0,"low":0},
					"maint":{"vhigh":0,"high":0,"med":0,"low":0},
					"doors":{"2":0,"3":0,"4":0,"5more":0},
					"persons":{"2":0,"4":0,"more":0},
					"lug_boot":{"small":0,"med":0,"big":0},
					"safety":{"low":0,"med":0,"high":0}
					},
			"acc":{
					"count":0,
					"buying":{"vhigh":0,"high":0,"med":0,"low":0},
					"maint":{"vhigh":0,"high":0,"med":0,"low":0},
					"doors":{"2":0,"3":0,"4":0,"5more":0},
					"persons":{"2":0,"4":0,"more":0},
					"lug_boot":{"small":0,"med":0,"big":0},
					"safety":{"low":0,"med":0,"high":0}
					},
			"good":{
					"count":0,
					"buying":{"vhigh":0,"high":0,"med":0,"low":0},
					"maint":{"vhigh":0,"high":0,"med":0,"low":0},
					"doors":{"2":0,"3":0,"4":0,"5more":0},
					"persons":{"2":0,"4":0,"more":0},
					"lug_boot":{"small":0,"med":0,"big":0},
					"safety":{"low":0,"med":0,"high":0}
					},
			"vgood":{
					"count":0,
					"buying":{"vhigh":0,"high":0,"med":0,"low":0},
					"maint":{"vhigh":0,"high":0,"med":0,"low":0},
					"doors":{"2":0,"3":0,"4":0,"5more":0},
					"persons":{"2":0,"4":0,"more":0},
					"lug_boot":{"small":0,"med":0,"big":0},
					"safety":{"low":0,"med":0,"high":0}
					}
			}
	for i in training_set:	# increment attribute values for all entries
		table = update_table(table, i)
	return table

def parse_lines(f):
	'''
	Convert txt file to a list of attribute strings
	 for each data entry
	'''
	training_set = open(f)
	inputstrings = training_set.readlines()
	output = []				# processed input
	for i in inputstrings:
		# print "i:",i
		temp = i.split(",")
		# print "temp",temp
		output.extend([temp])
	return output

def update_table(table, input):
	'''
	For each data entry, update all table values by tallying
	'''
	classification = input[-1].rstrip()
	table[classification]['count'] += 1
	# print "classification:",classification	
	for i, j in enumerate(input):
		# print "checking: ",i,"and",j
		if i == 0:
			table[classification]["buying"][j] += 1
		elif i == 1:
			table[classification]["maint"][j] += 1
		elif i == 2:
			table[classification]["doors"][j] += 1
		elif i == 3:
			table[classification]["persons"][j] += 1
		elif i == 4:
			table[classification]["lug_boot"][j] += 1
		elif i == 5:
			table[classification]["safety"][j] += 1
	return table

def display_table(table):
	'''
	Verbose printing of Bayesian classifier table
	'''
	for classification in table:
		print "Class = ",classification 
		for attribute in table[classification]:
			print "\t",attribute,"=", table[classification][attribute]

def freq_table(table):
	'''
	Convert Bayesian classifier table (raw integer counts) 
	 into frequency values (value/total entries)
	'''
	total_entries = 0
	for i in table:
		total_entries += table[i]['count']
	
	for classification in table:
		for attribute in table[classification]:
			if attribute != 'count':
				for value in table[classification][attribute]:
					table[classification][attribute][value] /= float(table[classification]['count'])
	for classification in table:
		table[classification]['count'] /= float(total_entries)
	return table

def single_odds(f_table, input):
	'''
	Input: All conditions with one classification
	Returns: Odds of this condition to have this classification
	'''
	classification = input[-1]
	a = ["buying","maint","doors","persons","lug_boot","safety"]
	odds = 1
	for i in range(0,len(input)-1):
		this_condit = f_table[classification][a[i]][input[i]]
		odds = odds * this_condit
		# print input[i], this_condit, odds
	# print "this condit:", odds
	return odds

def get_accuracy(f_table, input_set):
	'''
	Input: Frequency table and testing set; testing set contains
	 	   attribute values and classification. We're comparing
	 	   the classifications to what the Bayesian classifier
	 	   predicts
	Returns: Accuracy (# of entries with same classification as
			 Bayesian prediction/# of entries)
	'''
	match = 0.0
	no_match = 0.0
	testing_set = copy.deepcopy(input_set)
	for input in testing_set:
		# print "==========================\n"
		test_classification = input[-1].rstrip()
		classifications = ["unacc","acc","good","vgood"]
		class_odds = {"unacc":0,"acc":0,"good":0,"vgood":0}
		for c in classifications:
			input[-1] = c
			# print "input:",input
			odds = single_odds(f_table, input)
			# print "\tclass",c,"odds:",odds
			class_odds[c] = odds
		# print "\nAll class odds:",class_odds
		prediction = max(class_odds, key=lambda i: class_odds[i])
		# print "Bayes classification:", prediction
		# print "Test classification:",test_classification
		# print "Bayesian classification:", prediction
		# print "Match?",
		if prediction == test_classification:
			match += 1
			# print "YES"
		else:
			no_match += 1
			# print "NO"
		# print "# match:", match
		# print "# no match:", no_match
		accuracy = match/(match+no_match)
		# print "Accuracy:", accuracy
	return accuracy

def classify(training, testing):
	'''
	Wrapper for getting accuracy based on Bayesian prediction
		See get_accuracy() for more description
	Inputs: Filename string OR list of parsed lines for training, testing set
	Output: Accuracy of testing set classification 

	'''
	'''
	if type(training) == str and type(testing) == str:
		training_set = parse_lines(training)
		testing_set = parse_lines(testing)'''
	
	if type(training) == str:
		training_set = parse_lines(training)
	else: 
		training_set = training
	if type(testing) == str:
			testing_set = parse_lines(testing)
	else: 
		testing_set = testing
	table = make_table(training_set)
	f_table = freq_table(table)

	# print "Bayesian classifier table:"
	if __name__ == "__main__":
		display_table(f_table)
	# print "=============================="
	accuracy = get_accuracy(f_table, testing_set)
	return accuracy


def main():
	if(len(sys.argv)==3):
		train_filename = sys.argv[1]
		test_filename = sys.argv[2]
	else:
		train_filename = "cartrain2.data"
		test_filename = "cartest2.data"
	accuracy = classify(train_filename,test_filename)
	print "Accuracy:", accuracy

if __name__ == "__main__":
	main()

