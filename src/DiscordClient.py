import discord
import json
import os

from AdminPanel import admin_panel
from Riot import RiotAPI
from utils import time, help, MENTION_HELP

class DiscordClient(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.riot = RiotAPI(os.getenv("RIOT_API_KEY"))
		self.owner = os.getenv("OWNER_ID")
		self.alias = {}

	async def on_ready(self):
		print(f"[{time()}] Owner ID: {self.owner}")
		print(f"[{time()}] Logged on {self.user} as {self.user.name}")
		
	async def on_message(self, message):
		if message.author == self.user or message.author.bot:
			return

		# if message.channel.type == discord.ChannelType.private:
		# 	print(f"[{time()}] Message from {message.author}: {message.content}")
		# else:
		# 	print(f"[{time()}] Message on {message.guild.name} in {message.channel} from {message.author}: {message.content}")

		if self.user.mentioned_in(message) and message.mention_everyone is False:
			await discord.Message.delete(message)
			await message.channel.send(MENTION_HELP, delete_after=5, mention_author=True)
			return
		
		elif message.content.startswith("!pt help"):
			await message.channel.send(embed=help())
			return
		
		elif message.content.startswith("ap") and str(message.author.id) in self.owner:
			await admin_panel(message)
			return

		elif message.content.startswith("!masteries") or message.content.startswith("!m"):
			await self.riot.get_masteries(message)
		
		elif message.content.startswith("!lm") or message.content.startswith("!lastmatch"):
			await self.riot.get_last_match(message)

		elif message.content.startswith("!pro"):
			await self.riot.get_lolpros_game(message)