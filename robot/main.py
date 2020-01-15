import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
import random

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='!')


def getChannelKey(channel_name):
    return int(os.getenv(channel_name))


@client.event
async def on_ready():
    print("Bot is connected")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "nuub" in [y.name.lower() for y in message.author.roles]:
        await message.guild.get_member(message.author.id).edit(nick=str(message.clean_content))
        role = discord.utils.get((message.author).guild.roles, name="Nuub")
        await (message.author).remove_roles(role)
        await message.channel.purge(limit=100)

    await client.process_commands(message)


@client.command()
async def ping(ctx):
    await ctx.send(f"Latency: {round(client.latency * 1000)}ms")


@client.command()
async def ziad(ctx):
    await ctx.send("```kobti```")


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]

    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command(aliases=['snap'])
@commands.has_role("ADMIN")
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)


@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')
    # await member.send("Welcome, Please change your nickname to your real name!!!!")
    channel = client.get_channel(getChannelKey("WELCOME_CHANNEL"))
    await channel.send('Welcome to the UWindsor Robotics & Tech Discord ' + ('<@' + str(member.id) + '>') + '!!!')
    await channel.send("Please enter your **REAL NAME** (FIRST LAST)!!");

    role = discord.utils.get(member.guild.roles, name="Nuub")
    await member.add_roles(role)

    # print()


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')


client.run(token)
