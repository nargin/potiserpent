import discord
import json
import os

async def get_last_match(self, message):
	if len(message.content.split(" ")) != 2:
		await message.channel.send("Invalid command usage")
		return
	name, tagLine = message.content.split(" ")[1].split("#")
	summoner = self.get_summoner_by_name(name, tagLine)
	puuid = summoner["puuid"]
	match_id = self.get_last_match_by_puuid(puuid)
	last_match = self.get_match_by_id(match_id[0])
	match_data = json.dumps(last_match, indent=4)
	output_path = os.path.join("/home/robin/potiserpent/", f"{name}_{tagLine}_last_match.json")

	with open(output_path, "w") as json_file:
		json_file.write(match_data)

	await message.channel.send("This command is not implemented yet")