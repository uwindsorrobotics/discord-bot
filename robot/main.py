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

    # print(message.author.name, message.author.discriminator, message.author.id)
    # print(message.channel.id)
    # print(message.author.roles)
    # print(message.author.id)

    await client.process_commands(message)


@client.command()
async def ping(ctx):
    await ctx.send(f"Latency: {round(client.latency * 1000)}ms")


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


@client.command()
async def clear(ctx, amount=2):
    if "admin" in [y.name.lower() for y in ctx.message.author.roles]:
        await ctx.channel.purge(limit=amount)


@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')
    # await member.send("Welcome, Please change your nickname to your real name!!!!")
    channel = client.get_channel(getChannelKey("WELCOME_CHANNEL"))
    await channel.send(
        'Welcome to the UWindsor Robotics & Tech Discord ' + (
                '<@' + str(member.id) + '>') + '!!! Please change your nickname to your real name!!')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')


client.run(token)
