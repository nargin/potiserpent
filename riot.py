import requests
import discord
import random

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

	def get_champions_id(self):
		url = "https://ddragon.leagueoflegends.com/cdn/14.10.1/data/en_US/champion.json"
		champions_json = self.get_request(url, "")
		champions: dict = {}
		for champion in champions_json["data"]:
			champions[champions_json["data"][champion]["key"]] = champion
		return champions

	def get_current_version_ddragon(self):
		url = "https://ddragon.leagueoflegends.com/api/versions.json"
		return self.get_request(url, "")

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
		if len(message.content.split(" ")) != 2:
			await message.channel.send("Invalid command usage")
			return
		name, tagLine = message.content.split(" ")[1].split("#")

		summoner = self.get_summoner_by_name(name, tagLine)
		if "puuid" not in summoner:
			await message.channel.send("Summoner not found")
			return
		puuid = summoner["puuid"]
		masteries = self.get_masteries_by_puuid(puuid)
		embed = discord.Embed(
			title="Top 3 Masteries",
			description="Top 3 masteries of the summoner",
			color=random.choice([discord.Color.blue(), discord.Color.red(), discord.Color.green(), discord.Color.orange()])
		)
		for mastery in masteries:
			embed.add_field(
				name=self.champions[str(mastery['championId'])],
				value=f"Points: {mastery['championPoints']}\nLevel: {mastery['championLevel']}",
				inline=False
		)
		await message.channel.send(embed=embed)

	async def get_last_match(self, message):
		if len(message.content.split(" ")) != 2:
			await message.channel.send("Invalid command usage")
			return
		name, tagLine = message.content.split(" ")[1].split("#")
		summoner = self.get_summoner_by_name(name, tagLine)
		puuid = summoner["puuid"]
		match_id = self.get_last_match_by_puuid(puuid)
		last_match = self.get_match_by_id(match_id[0])
		embed = discord.Embed(
			title="Last match",
			description="Last match of the summoner",
			color=random.choice([discord.Color.blue(), discord.Color.red(), discord.Color.green(), discord.Color.orange()])
		)
		print(last_match["info"]["participants"])
		for player in last_match["info"]["participants"]:
			champion = self.champions[str(player["championId"])]
			# if player["puuid"] == puuid:
				# embed.add_field(
					# add image of champon for puuid_player
			embed.add_field(
				name=champion,
				value=f"KDA: {player['kills']}/{player['deaths']}/{player['assists']}",
				inline=False
			)
		await message.channel.send(embed=embed)
	
	# skill shot hit and dodged