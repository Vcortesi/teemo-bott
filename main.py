import discord
from requests.api import request
import os
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.ext import commands

#path = "C://Users/Vince/AppData/Local/Programs/Python/chromedriver.exe" 
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")


script = " "
bot = commands.Bot(command_prefix='!')

# onReady def
@bot.event
async def on_ready():
    print('Captain Teemo on duty!')

@bot.command()
async def commands(ctx):
    async with ctx.typing():
        embed = discord.Embed(title = "Command List", description = "Here are the commands you can use:",color = discord.Colour.blue())
        embed.add_field(name = "!commands", value = "View commands", inline = False)
        embed.add_field(name = "!aram <champion>", value = "Provides Build info for Aram", inline = False)
        embed.add_field(name = "!ranked <champion>", value = "Provides Build info for Ranked", inline = False)
        embed.add_field(name = "!data <summoner name>", value = "Provides info for summoner", inline = False)
        embed.add_field(name = "!tft <summoner name>", value = "Provides info for tft", inline = False)
        embed.add_field(name = "!patchnotes", value = "Provides patch notes link", inline = False)
        
        await ctx.send(embed=embed)

@bot.command()
async def aram(ctx, *args):
    async with ctx.typing():
        await ctx.send(randomScript())
        champion = args[0]
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get('https://u.gg/lol/champions/aram/'+champion+'/-aram')
        driver.set_window_size(1920, 1080)
        element0 = driver.find_element_by_class_name('champion-image').get_attribute("src")
        element1 = driver.find_element_by_class_name('content-section_content.recommended-build_runes')
        element2 = driver.find_element_by_class_name('content-section.content-section_no-padding.recommended-build_items.media-query.media-query_DESKTOP_MEDIUM__DESKTOP_LARGE')
        element3 = driver.find_element_by_class_name('content-section_content.skill-path-block')

        await ctx.send(element0)
        
        element1.screenshot("screenshot.png")
        await ctx.send(file=discord.File('screenshot.png'))
        os.remove('screenshot.png')
        
        element2.screenshot("screenshot.png")
        await ctx.send(file=discord.File('screenshot.png'))
        os.remove('screenshot.png')

        element3.screenshot("screenshot.png")
        await ctx.send(file=discord.File('screenshot.png'))
        os.remove('screenshot.png')

        driver.quit()

@bot.command()
async def ranked(ctx, *args):
    async with ctx.typing():
        await ctx.send(randomScript())
        champion = args[0]
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get('https://u.gg/lol/champions/'+champion+'/build')
        driver.set_window_size(1920, 1080)
        element0 = driver.find_element_by_class_name('champion-image').get_attribute("src")
        element1 = driver.find_element_by_class_name('content-section_content.recommended-build_runes')
        element2 = driver.find_element_by_class_name('content-section.content-section_no-padding.recommended-build_items.media-query.media-query_DESKTOP_MEDIUM__DESKTOP_LARGE')
        element3 = driver.find_element_by_class_name('content-section.toughest-matchups.undefined')
        element4 = driver.find_element_by_class_name('content-section_content.skill-path-block')

        await ctx.send(element0)

        element1.screenshot("screenshot.png")
        await ctx.send(file=discord.File('screenshot.png'))
        os.remove('screenshot.png')

        element2.screenshot("screenshot.png")
        await ctx.send(file=discord.File('screenshot.png'))
        os.remove('screenshot.png')

        element3.screenshot("screenshot.png")
        await ctx.send(file=discord.File('screenshot.png'))
        os.remove('screenshot.png')

        element4.screenshot("screenshot.png")
        await ctx.send(file=discord.File('screenshot.png'))
        os.remove('screenshot.png')

        driver.quit()

@bot.command()
async def data(ctx, args):
    async with ctx.typing():
        sumName = args
        responseJSON = requestSummonerData(sumName)
        ID = responseJSON['id']
        responseJSON2 = requestRankedData(ID)

        embed = discord.Embed(title = "Teemo Data Command", description = "Here is your data on: " + str(sumName),color = discord.Colour.green())
        embed.add_field(name = "Summoner Name:", value = responseJSON2[0]['summonerName'], inline = False)
        embed.add_field(name = "Rank: ", value = responseJSON2[0]['tier'] +" "+ responseJSON2[0]['rank'], inline = False)
        embed.add_field(name = "LP: ", value = str(responseJSON2[0]['leaguePoints']), inline = False)
        embed.add_field(name = "Wins:", value = str(responseJSON2[0]['wins']), inline = False)
        embed.add_field(name = "Losses:", value = str(responseJSON2[0]['losses']), inline = False)
    
        await ctx.send(embed=embed)

@bot.command()
async def tft(ctx, args):
    async with ctx.typing():
        index = 0
        sumName = args
        responseJSON = requestSummonerData(sumName)
        ID = responseJSON['id']
        print(ID)
        responseJSON2 = requestTftData(ID)

        if(responseJSON2[0]['queueType']) == "RANKED_TFT":
            index = 0
        else:
            index = 1

        embed = discord.Embed(title = "Teemo Tft Data Command", description = "Here is your Tft data on: " + str(sumName),color = discord.Colour.teal())
        embed.add_field(name = "Summoner Name:", value = responseJSON2[index]['summonerName'], inline = False)
        embed.add_field(name = "Rank: ", value = responseJSON2[index]['tier'] +" "+ responseJSON2[index]['rank'], inline = False)
        embed.add_field(name = "LP: ", value = str(responseJSON2[index]['leaguePoints']), inline = False)
        embed.add_field(name = "Wins:", value = str(responseJSON2[index]['wins']), inline = False)
        embed.add_field(name = "Losses:", value = str(responseJSON2[index]['losses']), inline = False)

        await ctx.send(embed=embed)


@bot.command()
async def patchnotes(ctx,*args):
        async with ctx.typing():
                embed = discord.Embed(title = " ", description = "**[Patch Notes](https://www.leagueoflegends.com/en-us/news/tags/patch-notes/)**",color = discord.Colour.red())
                await ctx.send(embed=embed)


def randomScript():
    randNum = random.randrange(1, 5)
    if(randNum == 1):
        script = "Yes, sir!"
    if(randNum == 2):
        script = "I'll scout ahead!"
    if(randNum == 3):
        script = "Reporting in."
    if(randNum == 4):
        script =  "Swiftly!"
    if(randNum == 5):
        script = "Never underestimate the power of the Scout's code."
    return script

def requestSummonerData(summonerName):
    URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+summonerName+"?api_key="+os.environ.get('API')
    response = requests.get(URL)
    return response.json()

def requestRankedData(ID):
    URL = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/"+ID+"?api_key="+os.environ.get('API')
    response = requests.get(URL)
    return response.json()

def requestTftData(ID):
    URL = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/"+ID+"?api_key="+os.environ.get('API')
    response = requests.get(URL)
    return response.json()

bot.run(os.environ.get('TOKEN'))