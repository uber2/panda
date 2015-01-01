import logging
logging.basicConfig(level=logging.WARNING)
import json
import os

class data_handler():

	def __init__(self,file,option="r"):
		self.logger = logging.getLogger("data")
		self.file = "./data/" + file
		if not os.path.exists(self.file):
			self.logger.info("file %s does not exist. File was created from scratch for you",self.file)
			f=open(self.file,"w")
			f.close()
		
		self.option = option
		self.logger.debug("accessing file %s with option %s",self.file, self.option)

	def save(self,documents):
		self.logger.debug("saving documents ...")
		if type(documents) is not list:
			documents = [documents]
		
		my_file = open(self.file,self.option)
		self.logger.debug("accesing file %s with option %s",self.file,self.option)
		try:
			for document in documents:
				document = json.dumps(document)
				my_file.write(str(document)+"\n")
			my_file.close()
			self.logger.info("%i records saved. File %s closed successfully",len(documents),self.file)
			return 0
		except:
			my_file.close()
			self.logger.error("save_documents: something went wrong")
			return 1

	def load(self):
		self.logger.debug("loading documents ...")
		with open(self.file) as f:
			content = f.readlines()
	
		my_list =[]
		for item in content:
			my_list.append(json.loads(item))
		
		return my_list
	