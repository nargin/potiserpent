import discord
import requests
import json

async def get_lolpros_game(self, message):
	content = message.content.split(" ")
	if len(content) != 2:
		await message.channel.send("Invalid command usage")
		return

	name, tagLine = content[1].split("#")
	if not name or not tagLine:
		await message.channel.send("Invalid command usage")
		return

	url = "https://api.lolpros.gg/lol/game?query={name}&tagline={tagLine}".format(name=name, tagLine=tagLine)
	headers = {
		'Accept': 'application/json, text/plain, */*',
		'LPGG-server': 'EUW',
		'Origin': 'https://lolpros.gg',
		'Referer': 'https://lolpros.gg/',
	}

	response = requests.get(url, headers=headers)	
	if (response.text is None) or (response.text == ""):
		await message.channel.send("Player probably not in game")
		return

	if response.status_code >= 400:
		reason = response.json().get("error", "Unknown error")
		await message.channel.send("{status_code} - {reason}".format(status_code=response.status_code, reason=reason))
		return

	game = response.json()
	blueTeam = discord.Embed(
		title="Blue team :blue_circle:",
		color=discord.Color.blue()
	)
	redTeam = discord.Embed(
		title="Red team :red_square:",
		color=discord.Color.red()
	)

	for player in game["participants"]:
		champion = self.champions[str(player["championId"])]
		riotId = player.get("riotId", None)
		lolpros = player.get("lolpros", None)
		if lolpros is not None:
			team = lolpros.get('team', None)
			value = f"Champion: {champion}\n"
			if team is not None:
				team_name = team.get("name", None)
				value += f"Team: {team_name}\n"

			if player["teamId"] == 100:
				blueTeam.add_field(
					name=f":flag_{player['lolpros']['country'].lower()}: - {player['lolpros']['name']}",
					value=value,
					inline=False
				)
			elif player["teamId"] == 200:
				redTeam.add_field(
					name=f":flag_{player['lolpros']['country'].lower()}: - {player['lolpros']['name']}",
					value=value,
					inline=False
				)

		elif (riotId.lower() == (name + "#" + tagLine).lower()):
			champion = self.champions[str(player["championId"])]
			value = f"Champion: {champion}\n"
			summoner_name = player['riotId'].split('#')[0]
			if player["teamId"] == 100:
				blueTeam.add_field(
					name=f":question: - **{summoner_name}**",
					value=value,
					inline=False
				)
				
			elif player["teamId"] == 200:
				redTeam.add_field(
					name=f":question: - **{summoner_name}**",
					value=value,
					inline=False
				)

	if blueTeam.fields != []:
		await message.channel.send(embed=blueTeam)

	if redTeam.fields != []:
		await message.channel.send(embed=redTeam)

	if blueTeam.fields == [] and redTeam.fields == []:
		await message.channel.send("No pros found in this game")
