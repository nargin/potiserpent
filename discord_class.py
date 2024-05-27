import discord
import json
import os

from admin import admin_panel
from riot import RiotAPI
from utils import time

class DiscordClient(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.riot = RiotAPI(os.getenv("RIOT_API_KEY"))

	async def on_ready(self):
		print(f"[{time()}] Logged on {self.user} as {self.user.name}")
		
	async def on_message(self, message):
		if message.author == self.user or message.author.bot:
			return
		print(f"[{time()}] Message on {message.guild.name} in {message.channel} from {message.author}: {message.content}")
		
		if message.content.startswith("!masteries") or message.content.startswith("!m"):
			await self.riot.get_masteries(message)
		
		elif message.content.startswith("!lm"):
			await self.riot.get_last_match(message)

		elif message.content.startswith("ap") and message.author.id == 289456071637204992:
			await admin_panel(message)

		elif self.user.mentioned_in(message):
			await message.channel.send("Hello !")

		elif message.content.startswith("!pt help"):
			await message.channel.send("TODO 123")
		
		elif message.content.startswith("!pro"):
			await self.riot.get_lolpros_game(message)