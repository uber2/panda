import logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename ="log_panda.log")
import sys
sys.path.append('../bfapi/')
import data
import bfapi
import pprint

class trackinglist():

	def __init__(self):
		self.logger = logging.getLogger("trackinglist")

	def istracked(self,isin_wkn_ticker):
		"""checks if asset is being tracked"""
		isin = bfapi.asset_exists(isin_wkn_ticker)
		if isin:
			zebra = data.data_handler("assets.json")
			assets = zebra.load()
			self.logger.debug("assets = zebra.load(): %s", assets)
			if len(assets)==0:
				self.logger.debug("list is empty")
				return False
			else:
				assets = assets[0]
				self.logger.info("%s is tracked as %s",isin_wkn_ticker,isin)
				self.logger.debug("assets[0]: %s",assets)
				self.logger.debug("isin: %s in assets[\"isins\"]: %s",isin, isin in assets["isins"])
				return isin in assets["isins"]
		else:
			self.logger.info("asset %s is not listed online. Check asset page",self,isin_wkn_ticker)
	
	def track(self,isin_wkn_ticker):
		"""adds asset to tracking list"""
		self.logger.debug("trying to add %s to tracking list",isin_wkn_ticker)
		isin = bfapi.asset_exists(isin_wkn_ticker)
		self.logger.info("track: isin confirmed as %s",isin)
		if isin: # check if asset has a proper page online
			if not self.istracked(isin): # check if asset is tracked already
				self.logger.info("asset %s is going to be saved as %s",isin_wkn_ticker,isin)
				zebra = data.data_handler("assets.json","w")
				li_assets = zebra.load()
				self.logger.debug("li_assets = zebra.load(): %s",li_assets)
				if len(li_assets)==0:
					list_of_assets = [isin]
				else:
					list_of_assets=li_assets[0]["isins"]
					list_of_assets.append(isin)
					
				self._save_list_of_assets_to_file(list_of_assets)
				self.logger.info("asset %s added to tracking list",isin)
				return 0
			else:
				self.logger.info("assets %s is already tracked",isin)
				return 1
		else:
			self.logger.info("asset %s is not listed online. Check asset page",isin_wkn_ticker)
			return 1
			
	def untrack(self,isin_wkn_ticker):
		"""removes asset from tracking list"""
		isin = bfapi.asset_exists(isin_wkn_ticker)
		if isin:
			if self.istracked(isin):
				zebra = data.data_handler("assets.json","w")
				assets = zebra.load()[0]["isins"]
				self.logger.debug("assets directly after load: %s",assets)
				assets.remove(isin)
				self.logger.debug("removing asset %s",isin)
				self.logger.debug("assets directly after removal: %s",assets)
				self._save_list_of_assets_to_file(assets)
				self.logger.info("assets %s has been removed from the tracking list",isin)
			else:
				self.logger.info("asset has not been tracked in the first place")

	def _save_list_of_assets_to_file(self,isins):
		"""convenience function: does what it says"""
		if not type(isins) is list:
			isins = [isins]
		
		di_assets = {"isins":isins}
		zebra = data.data_handler("assets.json","w")
		zebra.save(di_assets)

	def autoupdate(self):
		"""crawls lists of etfs from Deutsche Boerse and adds them to the tracking list"""
		etfs = bfapi.get_dict_of_all_etfs()
		isins = etfs.values()
		for item in isins:
			self.track(item)
			
	def pretty(self):
		"""some pretty printing"""
		zebra = data.data_handler("assets.json","w")
		assets = zebra.load()[0]["isins"]
		for item in assets:
			print(item)
	
	def get_list(self):
		"""returns a list of all ISINs on the tracking list"""
		zebra = data.data_handler("assets.json")
		zebra = zebra.load()[0]
		isins = zebra["isins"]
		return isins
	
class bear():
	def __init__(self):
		self.logger = logging.getLogger("bear")

	def eat(self):
		"""Wrapper: Loads tracking list, downloads records, and save them"""
		isins = trackinglist().get_list()
		N = len(isins)
		self.logger.info("%i assets in tracking list",N)
		quotes = []
		self.logger.info("downloading data")
		for i in range(1,4):
			self.logger.info("iteration %i",i)
			new_quotes = bfapi.get(isins)
			self.logger.info("iteration %i: %i of %i records downloaded",i, len(new_quotes),len(isins))
			if not len(new_quotes)==0:
				quotes = quotes + new_quotes
			isins = self._get_missing_ISINS(quotes,isins)
		
		self.logger.info("TOTAL: %i records downloaded (%i assets in tracking list).",len(quotes),N)
		self.logger.info("saving data")
		monkey = data.data_handler("data.json","a")
		monkey.save(quotes)

	def _get_missing_ISINS(self,quotes,ISINS):
		"""outputs ISINs which have been skipped during scraping"""
		self.logger.info("checking for skipped assets")
		ISINS = set(ISINS)
		ISINS_downloaded = set()
		for i in range(0,len(quotes)):
			ISINS_downloaded.add(quotes[i]["ISIN"])
		ISINS_missing = list(ISINS.difference(ISINS_downloaded))
		self.logger.info("these assets were skipped:\n %s",pprint.pformat(ISINS_missing))
		return ISINS_missing
		
if __name__ == "__main__":
	panda = bear()
	panda.eat()

