import discord
import random
import json

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
