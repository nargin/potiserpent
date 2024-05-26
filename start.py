import os
import discord
from dotenv import load_dotenv

from discord_class import DiscordClient

load_dotenv()

if __name__ == "__main__":
	intents = discord.Intents.default()
	intents.message_content = True

	client = DiscordClient(intents=intents)
	client.run(os.getenv("DISCORD_BOT_TOKEN"))