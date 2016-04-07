'''
K-fold cross validation
'''
import random
from bayes import *
import copy
def training_indices(k):
	'''
	Calculate k bins, each bin has indices for training set
	original_set[k] is tested against the training sets
	e.g. k:4
	element indices:0,1,2,3

	testing_set_index:training_set_index
	0:1,2,3
	1:0,2,3
	2:0,1,3
	3:0,1,2

	indices are used to run bayesian classification
		classify()
	'''
	x = [i for i in range(0,k)]
	indices = []
	for i in range(0,k):
		indices.append([])	# empty partitions
	for i in range(0,len(x)):
		to_insert = [b for b in x if b != x[i]]
		indices[i].extend(to_insert)
	print "indices:",indices
	return indices

def randomize_list(k, orig_list):
	list_size = len(orig_list)
	print "orig list:",orig_list
	random_list = []
	for i in range(0,k):
		random_list.append([])	# empty partitions

	while len(orig_list) > 0:
		for i in range(0,k):
			x = random.choice(orig_list)
			orig_list.remove(x)
			random_list[i].extend([x])

	print "randomized, partitioned:",random_list
	return random_list

def classify_folds(input_set, indices):
	'''
	Run Bayesian classifier on input_set multiple times based on 
	 given indices. Indices format is described in training_indices()
	'''
	
	print "\n\ninput_set:",input_set
	all_accuracies = []
	for test_index, all_train_sets in enumerate(indices):
		print "test index:", test_index
		test_set = input_set[test_index]
		print "testing set:", test_set
		print "training indices:", all_train_sets
		for train_index in all_train_sets:
			train_set = input_set[train_index]
			print "training set:", train_set
			accuracy = classify(test_set,train_set)
			all_accuracies.extend([accuracy])
			print "accuracy:", accuracy
		print "\n"

		# training_set = input_set[train_index]
		# print "training_set:",training_set

		# classify([test_index], train_index)
	print "all accs:", all_accuracies
	max_acc = max(all_accuracies)
	max_index = all_accuracies.index(max_acc)
	
	flat_indices = [x for y in indices for x in y]	# flatten list of lists
	print "flat:", flat_indices
	# best_training = input_set[max_index]

	print "average acc:", sum(all_accuracies)/len(all_accuracies)
	print "highest acc:", max_acc
	print "list:", max_index
	# print "training set best:", best_training

	
def main():
	random.seed(3)
	list_size = 1000
	k = 4
	# orig_list = [i for i in range(0,list_size)]
	input_set = parse_lines("cartrain2.data")
	print input_set
	input_set = randomize_list(k, input_set)
	indices = training_indices(k)
	classify_folds(input_set, indices)

if __name__ == '__main__':
	main()