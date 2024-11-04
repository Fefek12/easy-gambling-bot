import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import random
from utils import l
import json
import typing

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="--", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("bot is ready")
    try:
        synced = await bot.tree.sync()
        print(f"synced commands {len(synced)}")
    except Exception as e:
        print(e)

@bot.tree.command(name="gamble")
async def gamble(interaction: discord.Interaction, game: str, amount: int, color: str = ""):
    if not l(str(interaction.user.id)):
        return
    
    with open("users.json", "r") as f:
        data = json.load(f)

    if data[str(interaction.user.id)]["money"] < amount:
        return await interaction.response.send_message("You doesn't have enough money!")

    if game == "roulette":
        if color == "" or color == None:
            return await interaction.response.send_message("You haven't selected a color (red/black)")

        chances = random.choice([True, False])
        if (chances == True and color == "red") or (chances == False and color == "black"):
            amount = amount * 2
            data[str(interaction.user.id)]["money"] += amount
            await interaction.response.send_message(f"You have won {amount}!")
        else:
            data[str(interaction.user.id)]["money"] -= amount
            await interaction.response.send_message(f"You have lost {amount}!")
    elif game == "slot machine":
        fruits = ["🥭", "🍇", "🍎"]
        st = random.choice(fruits)
        nd = random.choice(fruits)
        rd = random.choice(fruits)
        if st == nd and st == rd:
            amount = amount * 10
            data[str(interaction.user.id)]["money"] += amount
            await interaction.response.send_message(f"You have won {amount}! ({st} {nd} {rd})")
        else:
            data[str(interaction.user.id)]["money"] -= amount
            await interaction.response.send_message(f"You have lost {amount}! ({st} {nd} {rd})")
    
    with open("users.json", "w") as f:
        json.dump(data, f)
@gamble.autocomplete("game")
async def game(interaction: discord.Interaction, current: str) -> typing.List[discord.app_commands.Choice[str]]:
    d = []
    for game in ["roulette", "slot machine"]:
        if current.lower() in game.lower():
            d.append(discord.app_commands.Choice(name=game, value=game))
    return d
@gamble.autocomplete("color")
async def color(interaction: discord.Interaction, current: str) -> typing.List[discord.app_commands.Choice[str]]:
    d = []
    for color in ["red", "black"]:
        if current.lower() in color.lower():
            d.append(discord.app_commands.Choice(name=color, value=color))
    return d

@bot.tree.command(name="balance")
async def balance(interaction: discord.Interaction, member: discord.Member = None):
    if not l(str(interaction.user.id)):
        return
    
    with open("users.json", "r") as f:
        data = json.load(f)

    if member != None:
        if not l(str(member.id)):
            return
        
        await interaction.response.send_message(f"{member.name}'s balance: {data[str(member.id)]["money"]}")
    else:
        await interaction.response.send_message(f"{interaction.user.name}'s balance: {data[str(interaction.user.id)]["money"]}")

@bot.tree.command(name="pay")
async def pay(interaction: discord.Interaction, member: discord.Member, amount: int):
    if not l(str(interaction.user.id)) or not l(str(member.id)):
        return
    
    with open("users.json", "r") as f:
        data = json.load(f)
    
    if data[str(interaction.user.id)]["money"] >= amount:
        data[str(interaction.user.id)]["money"] -= amount
        data[str(member.id)]["money"] += amount
        await interaction.response.send_message(f"You have sent {amount} to {member.name}")
        
        with open("users.json", "w") as f:
            json.dump(data, f)
    else:
        await interaction.response.send_message("You doesn't have enough money!")

if __name__ == '__main__':
    bot.run(TOKEN)