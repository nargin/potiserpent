import requests
import discord
import json
import io
from commands.lolpro import *
from commands.masteries import *
from commands.last_match import *

from utils import time

class RiotAPI:
	def __init__(self, api_key):
		self.api_key = api_key
		self.test_request()
		self.champions = self.get_champions_id()

	def test_request(self):
		url = "https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations"
		response = requests.get(url, headers={"X-Riot-Token": self.api_key})
		if response.status_code == 200:
			print(f"[{time()}] Riot API key is valid")
		else:
			raise ValueError("[{time()}] Something went wrong with the Riot API")

	def get_request(self, url, endpoint):
		header = {
			"X-Riot-Token": self.api_key
		}
		response = requests.get(url + endpoint, headers=header)
		return response.json()

	# GET Method :

	def get_current_version_ddragon(self):
		url = "https://ddragon.leagueoflegends.com/api/versions.json"
		return self.get_request(url, "")

	def get_champions_id(self):
		version = self.get_current_version_ddragon()[0]
		url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
		champions_json = self.get_request(url, "")
		champions: dict = {}
		for champion in champions_json["data"]:
			champions[champions_json["data"][champion]["key"]] = champion
		return champions

	def get_summoner_by_name(self, name, tagLine):
		url = "https://europe.api.riotgames.com/"
		endpoint = "riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}".format(gameName=name, tagLine=tagLine)
		return self.get_request(url, endpoint)
	
	def get_summoner_by_puuid(self, puuid):
		url = "https://europe.api.riotgames.com/"
		endpoint = "riot/account/v1/accounts/by-puuid/{puuid}".format(puuid=puuid)
		return self.get_request(url, endpoint)
	
	def get_summoner_id_by_puuid(self, puuid):
		url = "https://euw1.api.riotgames.com/"
		endpoint = "lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}".format(encryptedPUUID=puuid)
		return self.get_request(url, endpoint)
	
	def get_masteries_by_puuid(self, puuid, count=3, champion=None):
		url = "https://euw1.api.riotgames.com/"
		if champion is None:
			endpoint = "/lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}/top?{count}".format(encryptedPUUID=puuid, count=count)
		else:
			championId = self.champions[champion]
			endpoint = "/lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}/by-champion/{championId}".format(encryptedPUUID=puuid, championId=championId)
		return self.get_request(url, endpoint)
	
	def get_last_match_by_puuid(self, puuid):
		url = "https://europe.api.riotgames.com/"
		endpoint = "/lol/match/v5/matches/by-puuid/{encryptedPUUID}/ids?start=0&count=1".format(encryptedPUUID=puuid)
		match_id = self.get_request(url, endpoint)
		return self.get_request(url, endpoint)
	
	def get_match_by_id(self, match_id):
		url = "https://europe.api.riotgames.com/"
		endpoint = "/lol/match/v5/matches/{matchId}".format(matchId=match_id)
		return self.get_request(url, endpoint)

	def get_champion_image(self, champion):
		version = self.get_current_version_ddragon()[0]
		url = "https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champion}.png".format(version=version, champion=champion)
		return url

	# Display functions :

	async def get_masteries(self, message):
		pass
	
	async def get_last_match(self, message):
		pass
	
	async def get_lolpros_game(self, message):
		pass

	# skill shot hit and dodged

RiotAPI.get_masteries = get_masteries
RiotAPI.get_lolpros_game = get_lolpros_game
RiotAPI.get_last_match = get_last_match