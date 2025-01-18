import datetime
import discord

def time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def help():
    embed = discord.Embed(
        title="📚 League of Legends Bot Commands",
        description="Track summoners, check masteries, and monitor games with these commands:",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )

    # Champion Mastery Commands
    embed.add_field(
        name="🏆 Champion Mastery",
        value=(
            "```\n!masteries <name>#<tag> [count/champion]\n"
            "!m <name>#<tag> [count/champion]```\n"
            "Shows champion masteries for a summoner\n"
            "• Use `count` to see more champions (default: 3)\n"
            "• Specify a `champion` to see mastery for that champion\n"
            "Example: `!m Snake#EUW 5` or `!m Snake#EUW Veigar`"
        ),
        inline=False
    )

    # Match History Commands
    embed.add_field(
        name="🎮 Match History",
        value=(
            "```\n!lm <name>#<tag>```\n"
            "Displays the last match played by the summoner\n"
            "• Shows KDA, champion, and game outcome\n"
            "• Includes match duration and game mode\n"
            "Example: `!lm Snake#EUW`"
        ),
        inline=False
    )

    # Live Game Commands
    embed.add_field(
        name="🔴 Live Game",
        value=(
            "```\n!pro <name>#<tag>```\n"
            "Checks if a summoner is currently in game\n"
            "• Shows current game details if found\n"
            "• Updates in real-time\n"
            "Example: `!pro Snake#EUW`"
        ),
        inline=False
    )

    return embed