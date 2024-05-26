import discord

async def get_masteries(message):
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

async def get_last_match(message):
	if len(message.content.split(" ")) != 2:
		await message.channel.send("Invalid command usage")
		return
	name, tagLine = message.content.split(" ")[1].split("#")
	summoner = self.riot.get_summoner_by_name(name, tagLine)
	puuid = summoner["puuid"]
	last_match = self.riot.get_last_match_by_puuid(puuid)
	await message.channel.send(f"Last match id: {last_match[0]}")