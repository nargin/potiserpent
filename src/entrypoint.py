import os
import discord
from dotenv import load_dotenv

from DiscordClient import DiscordClient

load_dotenv()

def main():
	intents = discord.Intents.default()
	intents.message_content = True

	discord_token = os.getenv("DISCORD_BOT_TOKEN")
	
	client = DiscordClient(intents=intents)
	client.run(discord_token)

if __name__ == "__main__":
	main()