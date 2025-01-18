import discord
import json
import os

from Riot import RiotAPI
from utils import time, help

class DiscordClient(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.riot = RiotAPI(os.getenv("RIOT_API_KEY"))
		self.alias = {}

	async def on_ready(self):
		print(f"[{time()}] Logged on {self.user} as {self.user.name}")
		
	async def on_message(self, message):
		if message.author == self.user or message.author.bot:
			return

		if (self.user.mentioned_in(message) and message.mention_everyone is False) \
			or message.content.startswith("!pt help"):
			await message.reply(embed=help())
			return

		elif message.content.startswith("!masteries") or message.content.startswith("!m"):
			await self.riot.get_masteries(message)
		
		elif message.content.startswith("!lm") or message.content.startswith("!lastmatch"):
			await self.riot.get_last_match(message)

		elif message.content.startswith("!pro"):
			await self.riot.get_lolpros_game(message)