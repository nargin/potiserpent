import discord
import json
import os
# from prisma import Prisma

from admin import admin_panel
from riot import RiotAPI
from utils import time, help, MENTION_HELP

class DiscordClient(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.riot = RiotAPI(os.getenv("RIOT_API_KEY"))
		# self.prisma = Prisma()
		# self.prisma.connect()
		

	async def on_ready(self):
		print(f"[{time()}] Logged on {self.user} as {self.user.name}")
		
	async def on_message(self, message):
		if message.author == self.user or message.author.bot:
			return
		if message.channel.type == discord.ChannelType.private:
			print(f"[{time()}] Message from {message.author}: {message.content}")
		else:
			print(f"[{time()}] Message on {message.guild.name} in {message.channel} from {message.author}: {message.content}")
		


		# No parsing needed

		if self.user.mentioned_in(message):
			await discord.Message.delete(message)
			await message.channel.send(MENTION_HELP, delete_after=10, mention_author=True)
			return
		
		elif message.content.startswith("!pt help"):
			await message.channel.send(embed=help())
			return
		
		elif message.content.startswith("ap") and message.author.id == 289456071637204992:
			await admin_panel(message)
			return

		# No need return last command possible

		if message.content.startswith("!alias"):
			await self.command_alias(message)

		elif message.content.startswith("!masteries") or message.content.startswith("!m"):
			await self.riot.get_masteries(message)
		
		elif message.content.startswith("!lm") or message.content.startswith("!lastmatch"):
			await self.riot.get_last_match(message)

		elif message.content.startswith("!pro"):
			await self.riot.get_lolpros_game(message)
	
	async def command_alias(self, message):
		# !alias add <alias> <summoner_name>
		# !alias remove <alias>
		# !alias list
		# !alias <alias>

		split = message.content.split(" ")
		if len(split) < 2:
			command = "list"
		else:
			command = split[1]
		if command == "add" or command == "set" or command == "a":
			if len(split) != 4:
				await message.channel.send("Invalid syntax. Use `!alias add <alias> <summoner_name>`")
				return
			alias = split[2]
			summoner_name = split[3]
			self.alias[alias] = summoner_name
			await message.channel.send(f"Alias `{alias}` added for `{summoner_name}`")
		
		elif command == "remove" or command == "delete" or command == "del" or command == "rm":
			if len(split) != 3:
				await message.channel.send("Invalid syntax. Use `!alias remove <alias>`")
				return
			alias = split[2]
			if alias in self.alias:
				del self.alias[alias]
				await message.channel.send(f"Alias `{alias}` removed")
			else:
				await message.channel.send(f"Alias `{alias}` not found")
		
		elif command == "list":
			if len(self.alias) == 0:
				await message.channel.send("No alias found")
			else:
				embed = discord.Embed(title="Alias list", color=0x00ff00)
				for alias, summoner_name in self.alias.items():
					embed.add_field(name=alias, value=summoner_name, inline=False)
				await message.channel.send(embed=embed)
		else:
			if command in self.alias:
				summoner_name = self.alias[command]
				await message.channel.send(f"Alias `{command}` is `{summoner_name}`")
			else:
				await message.channel.send(f"Alias `{command}` not found")
