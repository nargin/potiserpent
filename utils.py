import datetime
import discord

MENTION_HELP = "Hello! I'm a bot created by Robin. Type `!pt help` to see the list of available commands."

def time():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def help():
	embed = discord.Embed(
		title="Help",
		description="List of available commands",
		color=discord.Color.red()
	)
	embed.add_field(
		name="!masteries or !m <name>#<tagLine> (<count>/<champion>)",
		value="Get top 3 masteries of the summoner",
		inline=False
	)
	embed.add_field(
		name="!lm <name>#<tagLine>",
		value="Get last match of the summoner",
		inline=False
	)
	embed.add_field(
		name="!pro <name>#<tagLine>",
		value="Get the game of the summoner",
		inline=False
	)
	return embed