from discord.ext import commands
from random import randint
import async_timeout
import urllib.parse
import discord
import aiohttp
import string
import os

async def download(loop, url, parameters={}):
    # A semi-generic download function, might need some tweaking later on
    async with aiohttp.ClientSession(loop=loop) as session:
        with async_timeout.timeout(10):
            async with session.get(url, params=parameters) as resp:
                return await resp.read()

async def latex_get(loop, equation):
    s = urllib.parse.quote_plus(equation)
    url = "https://chart.googleapis.com/chart?"
    parameters = {
        "cht":"tx", 
        "chl": equation,
        "chf": "bg,s,36393E",
        "chco": "EEEEEE"
    }
    return await download(loop, url, parameters)

def generate_filename(extension=".png"):
    s = ""
    l = len(string.hexdigits) - 1
    for _ in range(12):
        s += string.hexdigits[randint(0, l)]
    return s + extension

class Scrape():
    def __init__(self, bot):
        self.bot = bot
        self.math = []

    @commands.command()
    async def latex(self, *equation : str):
        """ Parses LaTeX markup into a png via Google Charts 
            \\displaystyle is forced for nicer and bigger equations """
        equation = "\\displaystyle " + " ".join(equation)
        if equation == "": return
        res = await latex_get(self.bot.loop, equation)
        filename = generate_filename()
        with open(filename, "wb") as f:
            f.write(res)
        self.math.append(await self.bot.upload(filename))
        os.remove(filename)

    @commands.command()
    async def remove(self):
        """ Removes LaTeX images previously posted in the chat """
        while self.math:
            message = math.pop()
            await self.bot.delete_message(message)

def setup(bot):
    bot.add_cog(Scrape(bot))
