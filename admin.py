import discord

async def admin_panel(message):
	to_say = message.content[3:].strip()
	await message.delete()
	
	if to_say.startswith("role"):
		roles = [role.name for role in message.guild.roles]
		roles.remove("@everyone")
		embed = discord.Embed(
			title="Roles",
			description="Roles available on this server",
			color=discord.Color.red()
		)
		for role in roles:
			embed.add_field(
				name=role,
				value="",
				inline=False
			)
		await message.author.send(embed=embed)

	else:
		await message.channel.send(to_say)