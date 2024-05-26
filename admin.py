import discord

async def admin_panel(message):
	to_say = message.content.split("ap")[1].strip()
	await message.delete()
	
	if to_say.startswith("role"):
		# if to_say.startswith("role add"):
		# 	role_name = to_say.split("role add ")[1].strip()
		# 	role = discord.utils.get(message.guild.roles, name=role_name)
		# 	await message.author.add_roles(role)
		# 	await message.author.send(f"Role {role_name} added to {message.author}")
		# elif to_say.startswith("role remove"):
		# 	role_name = to_say.split("role remove ")[1].strip()
		# 	role = discord.utils.get(message.guild.roles, name=role_name)
		# 	await message.author.remove_roles(role)
		# 	await message.author.send(f"Role {role_name} removed from {message.author}")
		# else:
		roles = [role.name for role in message.guild.roles]
		roles_weight = [role.position for role in message.guild.roles]
		roles.remove("@everyone")
		roles = sorted(roles)
		embed = discord.Embed(
			title="Roles",
			description="Roles available on this server",
			color=discord.Color.red()
		)
		for role in roles:
			embed.add_field(
				name=role,
				value=f"Position: {roles_weight[roles.index(role)]}",
				inline=False
			)
		await message.author.send(embed=embed)
	else:
		await message.channel.send(to_say)