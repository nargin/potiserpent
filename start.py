import json
import requests
import dotenv
import os
from dotenv import load_dotenv
import discord
import datetime
import random

load_dotenv()

def time():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class DiscordClient(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.riot = RiotAPI(os.getenv("RIOT_API_KEY"))

		if self.riot.api_key is None:
			raise ValueError("No Riot API key found")

	async def on_ready(self):
		print(f"[{time()}] Logged on {self.user} as {self.user.name}")
		
	async def on_message(self, message):
		if message.author == self.user:
			return
		print(f"[{time()}] Message on {message.guild.name} in {message.channel} from {message.author}: {message.content}")
		
		if message.content.startswith("!masteries") or message.content.startswith("!m"):
			if len(message.content.split(" ")) != 2:
				await message.channel.send("Invalid command usage")
				return
			name, tagLine = message.content.split(" ")[1].split("#")
			summoner = self.riot.get_summoner_by_name(name, tagLine)
			puuid = summoner["puuid"]
			masteries = self.riot.get_masteries_by_puuid(puuid, count=5)
			embed = discord.Embed(
				title="Top 5 Masteries",
				description="Top 5 masteries of the summoner",
				color=discord.Color.blue()
			)
			for mastery in masteries:
				embed.add_field(
					name=self.riot.champions[str(mastery['championId'])],
					value=f"Points: {mastery['championPoints']}\nLevel: {mastery['championLevel']}",
					inline=False
				)
			await message.channel.send(embed=embed)
		elif message.content.startswith("!axel"):
			return await message.channel.send("Axel est OMEGA PISSLOW NITROSTUCK {}".format("XD" * random.randint(0, 1000)))
		elif message.content.startswith("ap") and message.author.id == 289456071637204992:
			to_say = message.content.split("ap")[1]
			await message.delete()
			await message.channel.send(to_say)
		elif client.user.mentioned_in(message):
			await message.channel.send("Hello !")


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

	def get_summoner_by_name(self, name, tagLine):
		url = "https://europe.api.riotgames.com/"
		endpoint = "riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}".format(gameName=name, tagLine=tagLine)
		return self.get_request(url, endpoint)
	
	def get_summoner_by_puuid(self, puuid):
		url = "https://europe.api.riotgames.com/"
		endpoint = "riot/account/v1/accounts/by-puuid/{puuid}".format(puuid=puuid)
		return self.get_request(url, endpoint)
	
	def get_masteries_by_puuid(self, puuid, count=-1):
		url = "https://euw1.api.riotgames.com/"
		if count == -1:
			endpoint = "/lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}".format(encryptedPUUID=puuid)
		elif count > 0:
			endpoint = "/lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}/top?{count}".format(encryptedPUUID=puuid, count=count)
		else:
			raise ValueError("Invalid count value")
		return self.get_request(url, endpoint)


if __name__ == "__main__":
	intents = discord.Intents.default()
	intents.message_content = True

	client = DiscordClient(intents=intents)
	client.run(os.getenv("DISCORD_BOT_TOKEN"))