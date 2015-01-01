import logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
import data
import sys
sys.path.append('../bfapi/')
import bfapi


class trackinglist():

	def __init__(self):
		self.logger = logging.getLogger("trackinglist")

	### checks if asset is being tracked
	def istracked(self,isin_wkn_ticker):
		isin = bfapi.asset_exists(isin_wkn_ticker)
		if isin:
			zebra = data.data_handler("assets.json")
			assets = zebra.load()
			self.loger.debug("assets = zebra.load(): %s", assets)
			if len(assets)==0:
				self.loger.debug("list is empty")
				return False
			else:
				assets = assets[0]
				self.loger.info("%s is tracked as %s",isin_wkn_ticker,isin)
				self.loger.debug("assets[0]: %s",assets)
				self.loger.debug("isin: %s in assets[\"isins\"]: %s: %s",isin, assets.values(), isin in assets["isins"])
				return isin in assets["isins"]
		else:
			self.loger.info("asset %s is not listed online. Check asset page",self,isin_wkn_ticker)
	
	### adds asset to tracking list
	def track(self,isin_wkn_ticker):
		self.loger.debug("trying to add %s to tracking list",isin_wkn_ticker)
		isin = bfapi.asset_exists(isin_wkn_ticker)
			
		self.loger.info("track: isin confirmed as %s",isin)
		if isin: # check if asset has a proper page online
			if not self.istracked(isin): # check if asset is tracked already
				self.loger.info("asset %s is going to be saved as %s",isin_wkn_ticker,isin)
				zebra = data.data_handler("assets.json","w")
				li_assets = zebra.load()
				self.loger.debug("li_assets = zebra.load(): %s",li_assets)
				if len(li_assets)==0:
					list_of_assets = [isin]
				else:
					list_of_assets=li_assets[0]["isins"]
					list_of_assets.append(isin)
					
				self._save_list_of_assets_to_file(list_of_assets)
				self.loger.info("asset %s added to tracking list",isin)
				return 0
			else:
				self.loger.info("assets %s is already tracked",isin)
				return 1
		else:
			self.loger.info("asset %s is not listed online. Check asset page",isin_wkn_ticker)
			return 1
			
	### removes asset from tracking list
	def untrack(self,isin_wkn_ticker):
		isin = bfapi.asset_exists(isin_wkn_ticker)
		if isin:
			if self.istracked(isin):
				zebra = data.data_handler("assets.json","w")
				assets = zebra.load()[0]["isins"]
				self.loger.debug("assets directly after load: %s",assets)
				assets.remove(isin)
				self.loger.debug("removing asset %s",isin)
				self.loger.debug("assets directly after removal: %s",assets)
				self._save_list_of_assets_to_file(assets)
				self.loger.info("assets %s has been removed from the tracking list",isin)
			else:
				self.loger.info("asset has not been tracked in the first place")
	
	### convenience function: does what it says
	def _save_list_of_assets_to_file(self,isins):
		if not type(isins) is list:
			isins = [isins]
		
		di_assets = {"isins":isins}
		zebra = data.data_handler("assets.json","w")
		zebra.save(di_assets)

	### crawls the list of all etfs and adds them to the tracking list
	def autoupdate(self):
		etfs = bfapi.get_dict_of_all_etfs()
		isins = etfs.values()
		for item in isins:
			self.track(item)
			
	### some pretty printing		
	def pretty(self):
		zebra = data.data_handler("assets.json","w")
		assets = zebra.load()[0]["isins"]
		for item in assets:
			print(item)
	
	### returns a list of all ISINs on the tracking list
	def get_list(self):
		zebra = data.data_handler("assets.json")
		zebra = zebra.load()[0]
		isins = zebra["isins"]
		return isins
	
class bear():
	def __init__(self):
		self.logger = logging.getLogger("bear")

	def eat(self):
		isins = trackinglist().get_list()
		self.logger.info("downloading data")
		quotes = bfapi.get(isins)
		self.logger.info("%i records downloaded",len(quotes))
		self.logger.info("save data")
		monkey = data.data_handler("data.json","a")
		monkey.save(quotes)

		
		
	

