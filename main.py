import os
import discord
import yaml
from discord.ext import commands
from discord_components import DiscordComponents
from discord.ext.commands import CommandNotFound
from database import Database

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='-', intents=intents)
config = yaml.safe_load(open("config.yml", 'r', encoding="utf-8"))
db = Database()
DiscordComponents(bot)


@bot.event
async def on_ready():
    """Handles the bot startup"""
    await bot.change_presence(activity=discord.Game(config.get("bot-activity")))
    print('Bot is ready!')


@bot.event
async def on_command_error(ctx, error):
    """Handles unknown commands"""
    if isinstance(error, CommandNotFound):
        if config.get("remove-unknown-commands"):
            await ctx.message.delete()
        embed_conf = config.get("command-not-found-embed")
        if embed_conf.get("enabled"):
            embed = discord.Embed(title=embed_conf.get("title"),
                                  description=embed_conf.get("description"),
                                  color=embed_conf.get("color"))
            embed.set_footer(text=embed_conf.get("footer"))
            await ctx.send(embed=embed, delete_after=10.0)
            return
    raise error


modules = []

for filename in os.listdir('./modules'):
    if filename.endswith('.py'):
        modules.append("modules." + filename[:-3])

if __name__ == '__main__':
    for extension in modules:
        bot.load_extension(extension)

bot.run(config.get("bot-token"))
