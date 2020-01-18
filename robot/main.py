import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
import random

from uwu import *

import time

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='!')

silenced_dict = dict()

client.remove_command("help")

commands_dict = {
    "ping": "`!ping`\n\tReturns latency in milliseconds",
    "8ball": "`!8ball <question>`\nReturns an answer to your question",
    "clear": "`!clear <num>`\nDeletes the amount of messages specified (**ADMIN ONLY**)",
    "uwu": "`!uwu <sentence>`\nConverts given sentence into UwU",
    "silence": "`!silence @user <num of minutes>m`\nPrevents user from talking in channels for a certain period of time (**ADMIN ONLY**)",
    "help": "`!help <command>` prints details of specified command and if none are specified, displays all commands"

}


def getChannelKey(channel_name):
    return int(os.getenv(channel_name))


def getCurrTime():
    return time.clock_gettime(time.CLOCK_REALTIME)


@client.event
async def on_ready():
    print("Bot is connected")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "silenced" in [y.name.lower() for y in message.author.roles]:
        if ((getCurrTime() - silenced_dict[message.author.nick][1]) / 60 >= silenced_dict[message.author.nick][0]):
            role = discord.utils.get(message.author.guild.roles, name="Silenced")
            await (message.author).remove_roles(role)
        else:
            msg = await (message.channel).fetch_message(message.id)
            await msg.delete()

    if "nuub" in [y.name.lower() for y in message.author.roles]:
        await message.guild.get_member(message.author.id).edit(nick=str(message.clean_content))
        role = discord.utils.get((message.author).guild.roles, name="Nuub")
        await (message.author).remove_roles(role)
        await message.channel.purge(limit=100)

    if "nuub" not in [y.name.lower() for y in message.author.roles] and "silenced" not in [y.name.lower() for y in
                                                                                           message.author.roles]:
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
    channel = client.get_channel(getChannelKey("WELCOME_CHANNEL"))
    await channel.send('Welcome to the UWindsor Robotics & Tech Discord ' + ('<@' + str(member.id) + '>') + '!!!')
    await channel.send("Please enter your **REAL NAME** (FIRST LAST)!!");

    role = discord.utils.get(member.guild.roles, name="Nuub")
    await member.add_roles(role)


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')


@client.command()
async def uwu(ctx, *, message):
    uwu = receive(message)
    await ctx.send(uwu)


@client.command()
async def silence(ctx, user: discord.Member, waitTime='5m'):
    role = discord.utils.get(user.guild.roles, name="Silenced")
    await user.add_roles(role)
    currTime = time.clock_gettime(time.CLOCK_REALTIME)

    silenced_dict[user.display_name] = (int(waitTime.split("m")[0]), currTime)


@client.command()
async def out(ctx):
    await ctx.send(silenced_dict)


@client.command()
async def help(ctx, *, command=None):
    embed = discord.Embed(title="HELP", colour=0xff1333)
    if command is None:
        for i in commands_dict:
            embed.add_field(name=i, value=commands_dict[i], inline=False)
    elif command in commands_dict:
        embed.add_field(name=command, value=commands_dict[command], inline=False)
    else:
        await ctx.send("This is not an existing command")
        return
    await ctx.send(embed=embed)


client.run(token)
