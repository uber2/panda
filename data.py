import json
import logging
import os
logging.basicConfig(level=logging.ERROR)

class data_handler():

	def __init__(self,file,option="r"):
		
		self.file = "./data/" + file
		if not os.path.exists(self.file):
			logging.info("file %s does not exist. File was created from scratch for you",self.file)
			f=open(self.file,"w")
			f.close()
		
		self.option = option
		
		logging.debug("class initiated with file %s",self.file)
		logging.debug("class initiated with option %s",self.option)

	def save(self,documents):
		logging.debug("entering save:")
		if type(documents) is not list:
			documents = [documents]
		
		my_file = open(self.file,self.option)
		try:
			for document in documents:
				document = json.dumps(document)
				my_file.write(str(document)+"\n")
			my_file.close()
			logging.debug("file written and closed successfully")
			return 0
		except:
			my_file.close()
			logging.error("save_documents: something went wrong")
			return 1

	def load(self):
		logging.debug("entering load:")
		with open(self.file) as f:
			content = f.readlines()
	
		my_list =[]
		for item in content:
			my_list.append(json.loads(item))
		
		return my_list
	