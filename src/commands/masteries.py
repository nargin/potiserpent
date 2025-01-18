import discord
import random
import json

async def get_masteries(self, message):
	if len(message.content.split(" ")) != 2:
		await message.reply("Invalid command usage")
		return
	name, tagLine = message.content.split(" ")[1].split("#")

	summoner = self.get_summoner_by_name(name, tagLine)
	if "puuid" not in summoner:
		await message.reply("Summoner not found")
		return
	puuid = summoner["puuid"]
	masteries = self.get_masteries_by_puuid(puuid)


	max_points = 0
	for champions in masteries:
		max_points += champions["championPoints"]

	embed = discord.Embed(
		title=f"Top 3 Masteries - {name}#{tagLine}",
		description="Champion mastery progression",
		color=discord.Color.dark_grey()
	)

	if masteries:
		top_champion = self.champions[str(masteries[0]['championId'])]
		embed.set_thumbnail(url=self.get_champion_image(top_champion))

	for mastery in masteries:
		champion_name = self.champions[str(mastery['championId'])]
		points = mastery['championPoints']
		level = mastery['championLevel']
		
		percentage = (points / max_points) * 100
		blocks = int(percentage / 10)
		progress_bar = f"{'🟦' * blocks}{'⬜' * (10 - blocks)} {percentage:.1f}%"

		formatted_points = "{:,}".format(points)

		embed.add_field(
			name=champion_name,
			value=f"Points: {formatted_points}\nLevel: {level}\n{progress_bar}",
			inline=False
		)

	await message.reply(embed=embed)