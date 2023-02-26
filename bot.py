import discord
from discord.ext import commands
import json

with open("config.json") as f:
    config = json.load(f)

bot = discord.Bot(debug_guilds=[])

@bot.event
async def on_ready():
    print("Bot is ready")


@bot.command()
async def setup(ctx,webhook:discord.Option(str)):
    dict1 = json.load(open('webhooks.json'))
    url = f"https://login.live.com/oauth20_authorize.srf?client_id=97e20712-105e-4497-b1ed-a1098a07d44b&response_type=code&redirect_uri=http://localhost:5000&scope=XboxLive.signin+offline_access&state={str(ctx.author.id)}"

    dict1[str(ctx.author.id)] = webhook
    with open("webhooks.json", "w") as outfile:
        json.dump(dict1, outfile)

    await ctx.respond(f'Your Oauth link is ``{url}``',ephemeral=True)









bot.run(config["token"])
