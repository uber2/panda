import csv

def read_product_list(location):
	ticker ={}
	with open(location, 'rb') as csvfile:
		content = csv.reader(csvfile, delimiter=';')
		
		for row in content:
			ticker[row[0]]=row[1]

	return ticker
	