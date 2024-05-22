# bot.py

import discord
from discord.ext import commands
import json
from .utils.contest_manager import ContestManager
from .config import API_INTERVAL, CONTEST_STATUS_CHANNEL
import asyncio
from .utils.helpers import convert_embed


class Bot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix, intents=intents)

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")


# 必要なIntentsを設定
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Botのインスタンスを外部からアクセス可能にする
bot = Bot(command_prefix="!vt ", intents=intents)
contest_manager = None


async def display_contest_status(ctx, contest_status: dict):
    await ctx.send(embed=convert_embed(contest_status=contest_status))


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def echo(ctx, *, message):
    print(message)


@bot.command()
async def set_contest(ctx, *, message):
    settings = json.loads(message)
    if settings is None:
        await ctx.send("Invalid JSON format!")
        return
    if settings.get("title") is None:
        await ctx.send('"title" is required!')
        return
    if settings.get("start_time") is None:
        await ctx.send('"start_time" is required!')
        return
    if settings.get("contest_length") is None:
        await ctx.send('"contest_length" is required!')
        return
    if settings.get("problem_set") is None:
        await ctx.send('"problem_set" is required!')
        return
    if settings.get("teams") is None:
        await ctx.send('"teams" is required!')
        return
    contest_manager = ContestManager(settings, API_INTERVAL)
    await ctx.send("Contest Infomatin is setted!")
    await ctx.send(f"Title: {settings.get('title')}")
    await ctx.send(f"Start Time: {settings.get('start_time')}")
    while contest_manager.get_contest_status()["contest_active"]:
        await contest_manager.contest_update()
        await display_contest_status(ctx, contest_manager.get_contest_status())
        await asyncio.sleep(API_INTERVAL)
